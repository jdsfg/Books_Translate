#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_translation.py — 译文侧**轻量结构校验**（便宜、可全量跑，不依赖回译）

设计（依据 2026-07-19 Devin 审查 P1-3）：
  - 逐块比对 源↔译 的 ###/#### 标题数、代码围栏 ``` 数、LaTeX $$/$ 数、表格 | 行数、脚注数；
    不一致即报警（结构元素丢失/多出）。
  - **绝不用"长度比"判异常**：EN→ZH 字符比天然 0.2–0.35，同语种比例阈值会误报每一块。
  - 可选 --force-arabic：理科/技术/金融书要求源块阿拉伯数字集在译块中基本一致（中文数词约化会暴露）。
  - 可选 --glossary：术语合规率（译文是否真的采用了约定中文译法）。

用法：
  python verify_translation.py <src.md> [<src2.md> ...]
        [--force-arabic] [--glossary 术语库.md] [--strict] [--report 报告.md]

退出码：有 ERROR → 1；仅 WARNING/无问题 → 0。
"""
import argparse, importlib.util, os, re, sys
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
# translate_book.py 在上级目录（书库抓取工具\），本脚本在 书库抓取工具\translate\
# 用 importlib 按显式路径加载，避免中文长路径下 sys.path 导入失败
TB_PATH = os.path.join(os.path.dirname(HERE), "translate_book.py")
_spec = importlib.util.spec_from_file_location("translate_book", TB_PATH)
tb = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(tb)

STRUCT_KEYS = ['h3', 'h4', 'fences', 'latex_block', 'latex_inline', 'table_rows', 'footnotes']

def count_struct(text):
    h3 = len(re.findall(r'^###\s', text, re.M))
    h4 = len(re.findall(r'^####\s', text, re.M))
    fences = text.count('```')
    latex_block = len(re.findall(r'\$\$', text))
    latex_inline = text.count('$') - 2 * latex_block
    table_rows = 0
    for line in text.splitlines():
        s = line.strip()
        if s.count('|') >= 2 and not re.match(r'^\s*\|?[\s:|-]+\|?\s*$', s):
            table_rows += 1
    footnotes = len(re.findall(r'\[\^', text))
    return dict(h3=h3, h4=h4, fences=fences, latex_block=latex_block,
                latex_inline=latex_inline, table_rows=table_rows, footnotes=footnotes)

def digit_runs(text):
    return re.findall(r'\d[\d,]*(?:\.\d+)?', text)

def norm_digits(runs):
    return set(r.replace(',', '') for r in runs)

def parse_glossary(path):
    """返回 [(en, zh), ...]，zh 用于合规检查。"""
    terms = []
    for line in Path(path).read_text(encoding='utf-8').splitlines():
        s = line.strip()
        if not s or s.startswith('#') or s.startswith('>'):
            continue
        if '|' in s:
            parts = [p.strip() for p in s.split('|')]
            en = parts[0]
            zh = parts[1] if len(parts) > 1 else ''
            if zh:
                terms.append((en, zh))
    return terms

def chap_of(bid):
    if bid == 'intro' or bid.startswith('intro_b'):
        return 'intro'
    m = re.match(r'^(c\d{2})_', bid)
    return m.group(1) if m else 'other'

def verify_book(src, force_arabic=False, glossary=None, strict=False):
    book = tb.Book(src)
    if book.load() is None:
        print(f"[verify] 跳过（未 init）：{book.stem}")
        return 0, 0
    terms = parse_glossary(glossary) if glossary else []
    n_err, n_warn = 0, 0
    print(f"\n=== {book.stem} ===")
    rows = []
    # 第一遍：收集每块源/译结构计数
    data = []
    for b in book.state['blocks']:
        if b['status'] != 'done':
            continue
        bid = b['id']
        p = book.work / 'blocks' / f"{bid}.md"
        if not p.exists():
            rows.append((bid, 'ERROR', '译文文件缺失')); n_err += 1
            continue
        zh = p.read_text(encoding='utf-8')
        src_text = book.src_of(bid)
        data.append((bid, src_text, zh, count_struct(src_text), count_struct(zh)))
    # 章级标题总量（h3/h4），用于把"边界切分伪差"降级。
    # 注意：旧书 legacy 切块会把 ### 标题切在块边界，导致"按块累加的源文标题数"被通胀；
    # 因此章级总量必须从【整章源文】重新统计（parse_source 一次），而不能累加 legacy 每块。
    true_chap = {}
    intro_txt, chaps = tb.parse_source(src)
    true_chap['intro'] = count_struct(intro_txt)
    for i, (tit, body) in enumerate(chaps, 1):
        true_chap[f'c{i:02d}'] = count_struct(body)
    chap_zh = {}
    for bid, st, zh, cs, cz in data:
        c = chap_of(bid)
        chap_zh.setdefault(c, {'h3': 0, 'h4': 0, 'fences': 0})
        chap_zh[c]['h3'] += cz['h3']; chap_zh[c]['h4'] += cz['h4']
        chap_zh[c]['fences'] += cz['fences']
    # 第二遍：逐块比对
    for bid, st, zh, cs, cz in data:
        c = chap_of(bid)
        for k in STRUCT_KEYS:
            if k in ('fences', 'latex_inline'):
                if cz[k] % 2 != 0:
                    rows.append((bid, 'WARN', f"{k} 译文奇数({cz[k]})，可能未闭合")); n_warn += 1
            elif k in ('h3', 'h4'):
                if cs[k] != cz[k]:
                    # 整章总量一致 → 块级差异是 legacy 切块把标题从边界劈开所致，伪差不报
                    cmatch = (true_chap.get(c, {}).get(k, 0) == chap_zh.get(c, {}).get(k, 0))
                    if cmatch:
                        # 整章总量一致 → 块级差异是 legacy 切块把标题从边界劈开所致，伪差不报
                        continue
                    rows.append((bid, 'ERROR',
                                 f"{k}: 源={cs[k]} 译={cz[k]} 不一致（本章总量也对不上，疑似真丢失）")); n_err += 1
            else:
                if cs[k] != cz[k]:
                    rows.append((bid, 'ERROR', f"{k}: 源={cs[k]} 译={cz[k]} 不一致")); n_err += 1
        # fences 块级只查奇偶（未闭合）；章级总量在下方单独比对，防整段代码被漏译丢弃
        # 阿拉伯数字集校验
        if force_arabic:
            miss = norm_digits(digit_runs(st)) - norm_digits(digit_runs(zh))
            if miss:
                msg = f"阿拉伯数字缺失(源有译无): {sorted(miss, key=lambda x:(len(x),x))}"
                if strict:
                    rows.append((bid, 'ERROR', msg)); n_err += 1
                else:
                    rows.append((bid, 'WARN', msg)); n_warn += 1
        # 术语合规：只查「源块里实际出现」的词，避免每块都 WARN
        # 用词边界正则匹配，避免子串误报（sample∈example / bit∈orbit / loss∈glossary）
        if terms:
            relevant = [zh_term for en, zh_term in terms
                        if en and zh_term and re.search(r'\b' + re.escape(en) + r'\b', st, re.I)]
            miss = [zh_term for zh_term in relevant if zh_term not in zh]
            if miss:
                rows.append((bid, 'WARN',
                             f"术语未采用约定译法(源含该词): {miss[:5]}{'...' if len(miss)>5 else ''}")); n_warn += 1
    # 章级 fences 总量比对：整段代码被漏译丢弃时（围栏成对消失）块级奇偶查不出，这里兜底
    for c, cnt in true_chap.items():
        src_f = cnt.get('fences', 0)
        zh_f = chap_zh.get(c, {}).get('fences', 0)
        if src_f != zh_f:
            rows.append((c, 'ERROR',
                         f"fences 章级总量: 源={src_f} 译={zh_f} 不一致（疑整段代码块漏译）")); n_err += 1
    for bid, lvl, msg in rows:
        print(f"  [{lvl}] {bid}: {msg}")
    if not rows:
        print("  [OK] 结构/数字/术语 全部一致")
    print(f"  汇总: ERROR={n_err} WARN={n_warn}")
    return n_err, n_warn

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('srcs', nargs='+')
    ap.add_argument('--force-arabic', action='store_true', help='要求源块阿拉伯数字集在译块中一致（理科/技术/金融书）')
    ap.add_argument('--glossary', default=None, help='术语库 .md，做术语合规检查')
    ap.add_argument('--strict', action='store_true', help='数字缺失按 ERROR 计（默认 WARN）')
    ap.add_argument('--report', default=None, help='把汇总写入该 .md')
    args = ap.parse_args()
    tot_err = tot_warn = 0
    for src in args.srcs:
        e, w = verify_book(src, args.force_arabic, args.glossary, args.strict)
        tot_err += e; tot_warn += w
    print(f"\n=== 总计: ERROR={tot_err} WARN={tot_warn} ===")
    if args.report:
        Path(args.report).write_text(
            f"# 译文结构校验报告\n\n总计: ERROR={tot_err} WARN={tot_warn}\n", encoding='utf-8')
    sys.exit(1 if tot_err else 0)

if __name__ == '__main__':
    main()
