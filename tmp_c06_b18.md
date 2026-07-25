**答案：**


    #!/usr/bin/env python3
    """比较两个 eval 结果 JSON 并输出 markdown 报告；回归时非零退出。"""
    import argparse
    import json
    import statistics
    import sys
    from collections import defaultdict
    from pathlib import Path

    def aggregate(eval_results_path: Path) -> dict[str, float]:
        """返回跨所有案例的每维度平均分。"""
        with eval_results_path.open() as f:
            data = json.load(f)
        by_dim = defaultdict(list)
        for case in data["cases"]:
            for dim, score in case["scores"].items():
                if isinstance(score, (int, float)):
                    by_dim[dim].append(score)
        return {dim: statistics.mean(scores) for dim, scores in by_dim.items()}

    def main() -> int:
        parser = argparse.ArgumentParser()
        parser.add_argument("--candidate", type=Path, required=True)
        parser.add_argument("--baseline", type=Path, required=True)
        parser.add_argument("--threshold-summary-drop", type=float, default=0.1)
        parser.add_argument("--threshold-dimension-floor", type=float, default=2.5)
        parser.add_argument("--output", type=Path, default=Path("comparison_report.md"))
        args = parser.parse_args()

        candidate = aggregate(args.candidate)
        baseline = aggregate(args.baseline)

        rows = []
        failures: list[str] = []
        for dim in sorted(set(candidate) | set(baseline)):
            b = baseline.get(dim)
            c = candidate.get(dim)
            delta = (c - b) if (b is not None and c is not None) else None
            rows.append((dim, b, c, delta))
            if delta is not None and -delta > args.threshold_summary_drop:
                failures.append(f"Dimension {dim!r} regressed by {-delta:.3f} (> {args.thre
shold_summary_drop})")                                                                                 if c is not None and c < args.threshold_dimension_floor:
                failures.append(f"Dimension {dim!r} below floor {args.threshold_dimension_f
loor} (candidate {c:.3f})")                                                                
        lines: list[str] = []
        lines.append("## Eval Comparison")
        lines.append("")
        lines.append("| Dimension | Baseline | Candidate | Delta |")
        lines.append("|---|---|---|---|")
        for dim, b, c, delta in rows:
            b_str = f"{b:.3f}" if b is not None else "n/a"
            c_str = f"{c:.3f}" if c is not None else "n/a"
            d_str = f"{delta:+.3f}" if delta is not None else "n/a"
            lines.append(f"| {dim} | {b_str} | {c_str} | {d_str} |")
        lines.append("")
        if failures:
            lines.append("### [FAIL] Gate failures")
            for fail in failures:
                lines.append(f"- {fail}")
        else:
            lines.append("### [PASS] Gate passed")

        args.output.write_text("\n".join(lines))
        print("\n".join(lines))
        return 1 if failures else 0

    if __name__ == "__main__":
        sys.exit(main())


这是最小可行比较。在生产中你会添加：每案例粒度（哪些案例回归了？）、切片级分解（每层分析）、最近 N 次运行的趋势图，以及与 SQLite 存储的集成用于历史上下文。起始脚本足够小可以无仪式维护；扩展随时间累积。

**AI 协作子问题**：你会如何请 LLM 帮助完成这个练习，你会在它的回答中验证什么？
