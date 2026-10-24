"""Agreement between the two judge models and per-condition means.
Usage: python judge_robustness.py results/measures.csv --out results/judge_robustness.md"""
from __future__ import annotations
import argparse, csv, math, statistics as st
from pathlib import Path


def rank(xs):
    order = sorted(range(len(xs)), key=lambda i: xs[i]); r = [0.0] * len(xs); i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        for k in range(i, j + 1):
            r[order[k]] = (i + j) / 2 + 1
        i = j + 1
    return r


def spearman(x, y):
    rx, ry = rank(x), rank(y); mx, my = st.mean(rx), st.mean(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = math.sqrt(sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry))
    return num / den if den else float("nan")


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("measures", type=Path); ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    rows = [r for r in csv.DictReader(open(a.measures)) if r["split"] in ("train", "test") and r["status"] == "complete"]
    both = [r for r in rows if r.get("CI2") not in (None, "", "nan") and r.get("CI") not in (None, "", "nan")]
    L = ["# Judge robustness: Gemma 3 27B (CI) vs Qwen3-235B-Instruct (CI2)\n"]
    if not both:
        L.append("No runs with both judges yet."); a.out.write_text("\n".join(L)); print("\n".join(L)); return
    x = [float(r["CI"]) for r in both]; y = [float(r["CI2"]) for r in both]
    L.append(f"Runs judged by both: {len(both)}. Spearman rank correlation of mean ratings: {spearman(x, y):.2f}.\n")
    L.append("| cond | n | Gemma mean | Qwen-235B mean | Gemma − Qwen |"); L.append("|---|---|---|---|---|")
    conds = sorted({r["condition"] for r in both}, key=lambda c: (len(c), c))
    for c in conds:
        rs = [r for r in both if r["condition"] == c]
        g = st.mean(float(r["CI"]) for r in rs); q = st.mean(float(r["CI2"]) for r in rs)
        L.append(f"| {c} | {len(rs)} | {g:.2f} | {q:.2f} | {g - q:+.2f} |")
    # ordering of conditions by each judge
    L.append("\nCondition ordering by Gemma: " + " > ".join(sorted(conds, key=lambda c: -st.mean(float(r["CI"]) for r in both if r["condition"] == c))))
    L.append("Condition ordering by Qwen-235B: " + " > ".join(sorted(conds, key=lambda c: -st.mean(float(r["CI2"]) for r in both if r["condition"] == c))))
    a.out.write_text("\n".join(L) + "\n"); print("\n".join(L))


if __name__ == "__main__":
    main()
