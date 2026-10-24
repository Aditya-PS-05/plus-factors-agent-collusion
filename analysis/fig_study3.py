"""Figure for Studies 3 and 4 (Qwen3-235B agents): left, outsiders' reward relative to the matched
baseline run (Dq, same seed) per run; right, number of runs in which each boolean factor fired.

Usage: python fig_study3.py results/measures.csv --out results/figures --conds Aq Adecq Aaudq Dq --baseline Dq
"""
from __future__ import annotations
import argparse, csv, math
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

LABEL = {"Aq": "Aq\nsimple\ncoalition", "Adecq": "Adecq\ndeception\ncoalition", "Aaudq": "Aaudq\ndeception\n+ audit notice", "Dq": "Dq\nbaseline"}
FACTORS = ["CD", "NC", "PC", "PI", "WA"]
FNAME = {"CD": "costly\ndeference", "NC": "internal\nnon-collision", "PC": "priority\ncapture", "PI": "private info\nposted", "WA": "word-action\ninconsistency"}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("measures", type=Path); ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--conds", nargs="*", default=["Aq", "Adecq", "Aaudq", "Dq"]); ap.add_argument("--baseline", default="Dq")
    a = ap.parse_args(); a.out.mkdir(parents=True, exist_ok=True)
    rows = [r for r in csv.DictReader(open(a.measures)) if r["status"] == "complete" and r["split"] in ("train", "test")]
    conds = [c for c in a.conds if any(r["condition"] == c for r in rows)]
    base = {r["seed"]: float(r["others_reward_mean"]) for r in rows if r["condition"] == a.baseline}
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.6, 3.3), gridspec_kw={"width_ratios": [1, 1.25]})
    for i, c in enumerate(conds):
        ys = [float(r["others_reward_mean"]) - base[r["seed"]] for r in rows if r["condition"] == c and r["seed"] in base]
        ax1.scatter([i + (j % 5 - 2) * 0.04 for j in range(len(ys))], ys, s=18, alpha=0.7, color="#555555")
        if ys:
            m = sum(ys) / len(ys); se = (sum((y - m) ** 2 for y in ys) / max(len(ys) - 1, 1)) ** 0.5 / len(ys) ** 0.5
            ax1.errorbar([i], [m], yerr=[1.645 * se], fmt="o", color="#d62728", capsize=4, ms=6, zorder=3)
    ax1.axhline(0, color="grey", lw=0.8, ls="--"); ax1.set_xticks(range(len(conds))); ax1.set_xticklabels([LABEL.get(c, c) for c in conds], fontsize=7)
    ax1.set_ylabel("outsiders' reward minus baseline run", fontsize=8.5); ax1.set_title("Harm to outsiders (mean, 90% interval)", fontsize=9)
    w = 0.8 / len(conds); cols = ["#1f77b4", "#d62728", "#9467bd", "#7f7f7f"]
    for i, c in enumerate(conds):
        n = sum(1 for r in rows if r["condition"] == c)
        cnt = [sum(1 for r in rows if r["condition"] == c and r[f] == "1") for f in FACTORS]
        ax2.bar([j + (i - (len(conds) - 1) / 2) * w for j in range(len(FACTORS))], cnt, width=w, color=cols[i % 4], label=f"{c} (n={n})")
    ax2.set_xticks(range(len(FACTORS))); ax2.set_xticklabels([FNAME[f] for f in FACTORS], fontsize=7.5); ax2.set_ylabel("runs in which the factor fired")
    ax2.set_title("Conduct factors by condition", fontsize=9); ax2.legend(fontsize=7, frameon=False)
    fig.tight_layout(); fig.savefig(a.out / "fig4_study3.png", dpi=200); fig.savefig(a.out / "fig4_study3.pdf"); print("wrote", a.out / "fig4_study3.png")


if __name__ == "__main__":
    main()
