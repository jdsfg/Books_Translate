#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
translate_book.py — 书库英→中翻译流水线状态机
设计要点（用户 2026-07-19 要求）：
  1) 检查点精确到「块」而非「本」：checkpoint.json 记录每个 block 的状态，
     崩溃/重启后从最后一个 done 块之后续译，不必重翻整本。
  2) 每块落盘：每译完一个 block 立即写入 .zh.md（按块序重组）+ 独立块文件
     .translate/<book>/blocks/<id>.md，进程被 kill 也只丢当前块。
  3) 失败块单独重试队列：校验失败或被标记的 block 进入 retry_queue，
     `retry` 模式只处理这些，不重翻全本。
  4) 指数退避：with_backoff() 对块处理（翻译/校验/可选 API 调用）做指数退避重试。

translator = AI agent（默认 manual 模式：next 输出块上下文，agent 翻译后 commit）。
可选 auto 模式：设置环境变量 TB_API_URL / TB_API_KEY 后由脚本调用 LLM API
（同样走退避 + 重试队列）。
"""
import argparse, json, os, sys, re, time, hashlib
from pathlib import Path

# ---------- 路径 ----------
SRC_DEFAULT_DIR = r"D:\HuaweiMoveData\Users\淡水海边\Desktop\Postgraduate\项目\MySelf\Archive\成稿存档"
WORK_ROOT = Path(r"D:\HuaweiMoveData\Users\淡水海边\Desktop\Postgraduate\项目\MySelf\Archive\书库抓取工具\translate")
BLOCK_CHARS = 3500          # 每个源块目标字符数（按段落累加切分，不切断句子）
MAX_BACKOFF = 60.0
BACKOFF_BASE = 2.0
MAX_RETRIES = 5

# ---------- 工具 ----------
def sha(text):
    return hashlib.sha1(text.encode('utf-8')).hexdigest()[:12]

def with_backoff(func, *args, max_retries=MAX_RETRIES, base=BACKOFF_BASE, max_wait=MAX_BACKOFF, **kw):
    """指数退避包装：异常时等待 base*2**attempt 秒后重试，封顶 max_wait。"""
    last = None
    for attempt in range(max_retries + 1):
        try:
            return func(*args, **kw)
        except Exception as e:
            last = e
            if attempt >= max_retries:
                break
            wait = min(base * (2 ** attempt), max_wait)
            print(f"  [backoff] attempt {attempt+1} failed: {e}; retry in {wait:.1f}s", file=sys.stderr)
            time.sleep(wait)
    raise last

# ---------- 解析源 MD ----------
H2_RE = re.compile(r'^##\s+(.*)$')

def parse_source(path):
    """返回 (intro_text, chapters:[(en_title, body_text), ...])。

    兼容两种引言形态：
      A) 显式 `## 导读` 章节；
      B) 无 `## 导读`，引言散文位于「目录之后、第一个 `## Chapter` 之前」。
    """
    text = Path(path).read_text(encoding='utf-8')
    lines = text.splitlines()
    # 定位第一个 `## ` 标题
    first_h2 = len(lines)
    for idx, line in enumerate(lines):
        if H2_RE.match(line or ''):
            first_h2 = idx
            break
    pre = lines[:first_h2]
    # 从 pre 中抽取引言散文：丢弃 `>` 元数据、`**目录**` 及其后的 TOC 列表项
    intro_parts, in_toc = [], False
    for l in pre:
        if l.startswith('>'):
            continue
        if '**目录**' in l:
            in_toc = True
            continue
        if in_toc:
            s = l.strip()
            if s.startswith('- ') or s == '' or s == '---':
                continue
            in_toc = False
            intro_parts.append(l)
        else:
            intro_parts.append(l)
    intro = '\n'.join(intro_parts).strip()
    intro = re.sub(r'^---\s*', '', intro).strip()
    # 解析 `## ` 章节
    sections = []
    cur_title, cur_body = None, []
    for line in lines[first_h2:]:
        m = H2_RE.match(line or '')
        if m:
            if cur_title is not None:
                sections.append((cur_title, '\n'.join(cur_body).strip()))
            cur_title = m.group(1).strip()
            cur_body = []
        else:
            cur_body.append(line)
    if cur_title is not None:
        sections.append((cur_title, '\n'.join(cur_body).strip()))
    chapters = []
    for title, body in sections:
        if title.strip() == '导读':
            intro = (intro + '\n\n' + body).strip() if intro else body
        else:
            chapters.append((title, body))
    return intro, chapters

# ---------- 分块（两种策略，新书用 heading-aware，旧 checkpoint 回退用 legacy） ----------
H34_RE = re.compile(r'^#{3,4}\s')

def split_blocks(body, size=BLOCK_CHARS):
    """【新书默认】先按 ##/###/#### 标题边界切段，段内再按段落累加切到 ~size。

    优先在子小节边界切，避免把 ###/#### 小节从中间劈开（保护上下文连贯与术语注入命中）。
    单个段超长时，才在该段内按空行继续切。
    """
    lines = body.split('\n')
    segs, cur = [], []
    for line in lines:
        if (H2_RE.match(line or '') or H34_RE.match(line or '')) and cur:
            segs.append('\n'.join(cur)); cur = []
        cur.append(line)
    if cur:
        segs.append('\n'.join(cur))
    blocks, buf, cnt = [], [], 0
    for seg in segs:
        seg_len = len(seg)
        if cnt + seg_len > size and buf:
            blocks.append('\n\n'.join(buf)); buf, cnt = [], 0
        if seg_len > size:
            for sub in seg.split('\n\n'):
                if cnt + len(sub) > size and buf:
                    blocks.append('\n\n'.join(buf)); buf, cnt = [], 0
                buf.append(sub); cnt += len(sub) + 2
        else:
            buf.append(seg); cnt += seg_len + 2
    if buf:
        blocks.append('\n\n'.join(buf))
    return blocks

def split_blocks_legacy(body, size=BLOCK_CHARS):
    """【旧版】纯按段落累加切分，不切断段落。供已 init 的旧 checkpoint 回退重建源文。"""
    paras = [p for p in body.split('\n') if p.strip() != '']
    blocks, buf, cnt = [], [], 0
    for p in paras:
        if cnt + len(p) > size and buf:
            blocks.append('\n\n'.join(buf))
            buf, cnt = [], 0
        buf.append(p)
        cnt += len(p) + 2
    if buf:
        blocks.append('\n\n'.join(buf))
    return blocks

def rebuild_block_src_legacy(src_path):
    """旧版重建：返回 [(bid, en_title, src), ...]，用于旧 checkpoint（无 src 字段）回退取源文。"""
    intro, chapters = parse_source(src_path)
    out = []
    if intro.strip():
        out.append(('intro', '导读', intro))
    for ci, (en_title, body) in enumerate(chapters, 1):
        for si, sb in enumerate(split_blocks_legacy(body), 1):
            out.append((f"c{ci:02d}_b{si:02d}", en_title, sb))
    return out

# ---------- Book 状态机 ----------
class Book:
    def __init__(self, src_path):
        self.src = Path(src_path)
        self.stem = self.src.stem
        self.work = WORK_ROOT / self.stem
        self.work.mkdir(parents=True, exist_ok=True)
        (self.work / 'blocks').mkdir(exist_ok=True)
        self.cp_path = self.work / 'checkpoint.json'
        self.zh_path = self.src.parent / (self.stem + '.zh.md')
        self.state = None

    def load(self):
        if self.cp_path.exists():
            self.state = json.loads(self.cp_path.read_text(encoding='utf-8'))
        return self.state

    def save(self):
        self.cp_path.write_text(json.dumps(self.state, ensure_ascii=False, indent=2), encoding='utf-8')

    def init(self):
        intro, chapters = parse_source(self.src)
        blocks, order = [], 0
        if intro.strip():
            ibs = split_blocks(intro)
            if len(ibs) == 1:
                blocks.append(self._mk('intro', '导读', ibs[0], order)); order += 1
            else:
                for si, sb in enumerate(ibs, 1):
                    blocks.append(self._mk(f"intro_b{si:02d}", '导读', sb, order)); order += 1
        titles = {}
        for ci, (en_title, body) in enumerate(chapters, 1):
            for si, sb in enumerate(split_blocks(body), 1):
                bid = f"c{ci:02d}_b{si:02d}"
                blocks.append(self._mk(bid, en_title, sb, order)); order += 1
            titles[f"c{ci:02d}"] = {'en': en_title, 'zh': ''}
        self.state = {
            'book': self.stem, 'src': str(self.src),
            'created': time.strftime('%Y-%m-%d %H:%M'),
            'block_chars': BLOCK_CHARS, 'titles': titles,
            'blocks': blocks, 'retry_queue': [],
        }
        self.save()
        self.zh_path.write_text(f"> 翻译中：{self.stem}\n\n", encoding='utf-8')
        return len(blocks)

    def _mk(self, bid, en_title, src, order):
        return {'id': bid, 'en_title': en_title, 'order': order, 'src_chars': len(src),
                'status': 'pending', 'src_sha': sha(src), 'src': src,
                'out_chars': 0, 'out_sha': '', 'note': ''}

    def next_pending(self):
        for b in sorted(self.state['blocks'], key=lambda x: x['order']):
            if b['status'] != 'done':
                return b
        return None

    def src_of(self, bid):
        b = self._find(bid)
        if b is None:
            return ''
        if b.get('src'):
            return b['src']
        # 旧 checkpoint 无 src 字段：用 legacy 重建按 id 匹配（与 init 时同构）
        for bid2, _, s in rebuild_block_src_legacy(self.src):
            if bid2 == bid:
                return s
        return ''

    def commit(self, bid, text):
        b = self._find(bid)
        if b is None:
            raise KeyError(bid)
        text = text.strip()
        if len(text) < 20:
            raise ValueError(f"block {bid} too short ({len(text)} chars) — refused, use `fail` to queue")
        (self.work / 'blocks' / f"{bid}.md").write_text(text, encoding='utf-8')
        b['status'] = 'done'
        b['out_chars'] = len(text)
        b['out_sha'] = sha(text)
        self.state['retry_queue'] = [x for x in self.state['retry_queue'] if x != bid]
        self.save()
        self.assemble()
        return b

    def fail(self, bid, reason=''):
        b = self._find(bid)
        if b is None:
            raise KeyError(bid)
        b['status'] = 'failed'
        b['note'] = reason
        if bid not in self.state['retry_queue']:
            self.state['retry_queue'].append(bid)
        self.save()

    def assemble(self):
        """按章节顺序重组 .zh.md（含目录与已锁中文标题）。"""
        texts = {}
        for b in self.state['blocks']:
            if b['status'] == 'done':
                p = self.work / 'blocks' / f"{b['id']}.md"
                texts[b['id']] = p.read_text(encoding='utf-8') if p.exists() else ''
        chapters = {}
        intro_text = None
        intro_ids = [b for b in self.state['blocks']
                     if (b['id'] == 'intro' or b['id'].startswith('intro_b')) and b['status'] == 'done']
        if intro_ids:
            intro_text = '\n\n'.join(texts.get(b['id'], '') for b in sorted(intro_ids, key=lambda x: x['order']))
        for b in self.state['blocks']:
            if b['id'] == 'intro' or b['id'].startswith('intro_b'):
                continue
            m = re.match(r'^(c\d{2})_b\d{2}$', b['id'])
            ch = m.group(1) if m else 'c00'
            chapters.setdefault(ch, []).append((b['order'], b['id'], texts.get(b['id'], '')))
        out = [f"> 本文件为《{self.stem}》中文译本（AI 翻译，个人学习用，请勿外传）。\n",
               "\n**目录**\n"]
        if intro_text is not None and intro_text.strip():
            out.append("- 导读")
        for ch in sorted(chapters):
            zh = self._zh_title(ch)
            out.append(f"- {zh}")
        out.append("\n---\n")
        if intro_text is not None and intro_text.strip():
            out.append("## 导读\n\n" + intro_text + "\n")
        for ch in sorted(chapters):
            out.append(f"\n## {self._zh_title(ch)}\n")
            for _, bid, t in sorted(chapters[ch]):
                out.append(t + "\n")
        self.zh_path.write_text('\n'.join(out), encoding='utf-8')

    def _zh_title(self, ch):
        return self.state['titles'].get(ch, {}).get('zh') or self.state['titles'].get(ch, {}).get('en', ch)

    def lock_titles(self, mapping):
        for k, v in mapping.items():
            if k in self.state['titles']:
                self.state['titles'][k]['zh'] = v
        self.save()
        self.assemble()

    def _find(self, bid):
        for b in self.state['blocks']:
            if b['id'] == bid:
                return b
        return None

    def status(self):
        total = len(self.state['blocks'])
        done = sum(1 for b in self.state['blocks'] if b['status'] == 'done')
        failed = sum(1 for b in self.state['blocks'] if b['status'] == 'failed')
        pending = total - done - failed
        pct = done / total * 100 if total else 0
        return total, done, pending, failed, pct

# ---------- 可选 auto 翻译（LLM API） ----------
def translate_api(prompt):
    import requests
    url = os.environ.get('TB_API_URL')
    key = os.environ.get('TB_API_KEY')
    if not url or not key:
        raise RuntimeError("TB_API_URL / TB_API_KEY 未设置，无法 auto 模式")
    r = requests.post(url, headers={'Authorization': f'Bearer {key}'},
                      json={'prompt': prompt}, timeout=120)
    r.raise_for_status()
    return r.json().get('text', '')

# ---------- CLI ----------
def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd')
    p = sub.add_parser('init');    p.add_argument('src')
    p = sub.add_parser('status');  p.add_argument('src')
    p = sub.add_parser('next');    p.add_argument('src'); p.add_argument('--ctx', action='store_true')
    p = sub.add_parser('commit');  p.add_argument('src'); p.add_argument('bid'); p.add_argument('--file', default=None)
    p = sub.add_parser('fail');    p.add_argument('src'); p.add_argument('bid'); p.add_argument('reason', nargs='?', default='')
    p = sub.add_parser('retry');   p.add_argument('src'); p.add_argument('--auto', action='store_true')
    p = sub.add_parser('titles');  p.add_argument('src')
    p = sub.add_parser('lock-titles'); p.add_argument('src'); p.add_argument('json_file')
    p = sub.add_parser('assemble'); p.add_argument('src')
    p = sub.add_parser('verify');  p.add_argument('src'); p.add_argument('--force-arabic', action='store_true')
    p.add_argument('--glossary', default=None); p.add_argument('--strict', action='store_true')
    args = ap.parse_args()
    if not args.cmd:
        ap.print_help(); return
    book = Book(args.src)
    if args.cmd == 'init':
        n = book.init()
        print(f"[init] {book.stem}: {n} blocks. checkpoint={book.cp_path}")
    elif args.cmd == 'status':
        book.load()
        t, d, pe, f, pct = book.status()
        print(f"[status] {book.stem}: total={t} done={d} pending={pe} failed={f} ({pct:.1f}%)")
        print(f"  zh={book.zh_path}")
    elif args.cmd == 'next':
        book.load()
        b = book.next_pending()
        if not b:
            print("[next] all blocks done.")
            return
        src = book.src_of(b['id'])
        print(f"=== BLOCK {b['id']} | en_title: {b['en_title']} | src_chars={b['src_chars']} ===")
        print("--- SOURCE ---")
        print(src)
        if args.ctx:
            print("--- PRIOR CONTEXT (last done block tail) ---")
            done = [x for x in book.state['blocks'] if x['status'] == 'done' and x['order'] < b['order']]
            if done:
                pb = done[-1]
                p = book.work / 'blocks' / f"{pb['id']}.md"
                if p.exists():
                    print('\n'.join(p.read_text(encoding='utf-8').splitlines()[-8:]))
        print("=== END BLOCK (translate above, then: python translate_book.py commit <src> " + b['id'] + ") ===")
    elif args.cmd == 'commit':
        book.load()
        if not args.file:
            # 防呆：工具调用时 stdin 是常开管道，sys.stdin.read() 会一直等 EOF → 永久阻塞超时卡死。
            # 因此彻底废弃 stdin 路径，强制 caller 用 --file 从文件读译文。
            print("[commit] ERROR: 必须提供 --file <译文文件>（已废弃 stdin 输入以避免阻塞超时）。"
                  "用法：commit <src> <bid> --file <译文文件>", file=sys.stderr)
            sys.exit(2)
        text = Path(args.file).read_text(encoding='utf-8')
        b = book.commit(args.bid, text)
        print(f"[commit] {args.bid}: done, out_chars={b['out_chars']}, zh={book.zh_path}")
    elif args.cmd == 'fail':
        book.load()
        book.fail(args.bid, args.reason)
        print(f"[fail] {args.bid} -> retry_queue. reason={args.reason}")
    elif args.cmd == 'retry':
        book.load()
        q = book.state['retry_queue']
        if not q:
            print("[retry] queue empty.")
            return
        print(f"[retry] {len(q)} blocks: {q}")
        if args.auto:
            for bid in list(q):
                b = book._find(bid)
                src = book.src_of(bid)
                prompt = f"翻译为通顺中文（科普风格）：\n{src}"
                try:
                    text = with_backoff(translate_api, prompt)
                    book.commit(bid, text)
                    print(f"  [ok] {bid}")
                except Exception as e:
                    print(f"  [still-fail] {bid}: {e}")
        else:
            print("  manual 模式：逐块 `next --ctx` 重译后 `commit`。")
    elif args.cmd == 'titles':
        book.load()
        for k, v in book.state['titles'].items():
            print(f"{k}\t{v['en']}\t{v['zh']}")
    elif args.cmd == 'lock-titles':
        book.load()
        mapping = json.loads(Path(args.json_file).read_text(encoding='utf-8'))
        book.lock_titles(mapping)
        print(f"[lock-titles] updated {len(mapping)} titles; zh reassembled.")
    elif args.cmd == 'assemble':
        book.load()
        book.assemble()
        print(f"[assemble] {book.zh_path}")
    elif args.cmd == 'verify':
        book.load()
        import importlib.util as _iu
        _vp = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'translate', 'verify_translation.py')
        _spec = _iu.spec_from_file_location('verify_translation', _vp)
        _vt = _iu.module_from_spec(_spec); _spec.loader.exec_module(_vt)
        e, w = _vt.verify_book(args.src, args.force_arabic, args.glossary, args.strict)
        sys.exit(1 if e else 0)

if __name__ == '__main__':
    main()
