"""Figures for the report. Figure 1: per-condition pair reward relative to D (matched seeds) and
coalition advantage, as strip plots with seed-wise points and means. Figure 2: factor rates by condition.

Usage: python figures.py results/measures.csv --out results/figures
"""
from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

FACTORS = ["CD", "NC", "PC", "PI", "WA", "OP"]
LABEL = {"A": "A: pair+private ch.", "B": "B: pair, no ch.", "C": "C: open ch., no pair", "D": "D: neither",
         "Adec": "Adec: pair+ch.+deceive", "Bdec": "Bdec: pair+deceive, no ch.", "E": "E: private ch., no prompt",
         "A6": "A6: pair+private ch.", "B6": "B6: pair, no ch.", "C6": "C6: open ch., no pair", "D6": "D6: neither", "E6": "E6: private ch., no prompt"}


def load(path, baseline="D"):
    rows = [r for r in csv.DictReader(open(path)) if r["status"] == "complete" and r["split"] in ("train", "test")]
    for r in rows:
        for k in ["H", "CI", "pair_reward_mean", "others_reward_mean", "seed"] + FACTORS:
            try:
                r[k] = float(r[k])
            except (TypeError, ValueError):
                r[k] = float("nan")
    base = {(r["split"], r["seed"]): r["pair_reward_mean"] for r in rows if r["condition"] == baseline}
    for r in rows:
        b = base.get((r["split"], r["seed"]))
        r["Hrel"] = r["pair_reward_mean"] - b if b is not None else float("nan")
    return rows


def strip(ax, rows, key, conds, title, ylabel):
    for i, c in enumerate(conds):
        ys = [r[key] for r in rows if r["condition"] == c and not math.isnan(r[key])]
        tr = [r[key] for r in rows if r["condition"] == c and r["split"] == "train" and not math.isnan(r[key])]
        te = [r[key] for r in rows if r["condition"] == c and r["split"] == "test" and not math.isnan(r[key])]
        ax.scatter([i - 0.08] * len(tr), tr, s=28, color="#1f77b4", alpha=0.8, label="train seeds" if i == 0 else None)
        ax.scatter([i + 0.08] * len(te), te, s=28, color="#ff7f0e", alpha=0.8, marker="s", label="test seeds" if i == 0 else None)
        if ys:
            m = sum(ys) / len(ys)
            ax.hlines(m, i - 0.25, i + 0.25, color="black", lw=2)
    ax.axhline(0, color="grey", lw=0.8, ls="--")
    ax.set_xticks(range(len(conds)))
    ax.set_xticklabels([LABEL.get(c, c) for c in conds], rotation=20, ha="right", fontsize=8)
    ax.set_title(title, fontsize=10)
    ax.set_ylabel(ylabel)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("measures", type=Path)
    ap.add_argument("--out", type=Path, required=True); ap.add_argument("--conds", nargs="*", default=None); ap.add_argument("--baseline", default="D")
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    rows = load(args.measures, args.baseline)
    conds = [c for c in (args.conds or ["A", "Adec", "B", "Bdec", "C", "D"]) if any(r["condition"] == c for r in rows)]
    BASE = args.baseline

    fig, axes = plt.subplots(1, 2, figsize=(9, 3.6))
    strip(axes[0], rows, "H", conds, "Coalition advantage (pair mean reward minus others')", "reward units")
    strip(axes[1], [r for r in rows if r["condition"] != BASE], "Hrel", [c for c in conds if c != BASE],
          f"Pair reward relative to condition {BASE}, same seed", "reward units")
    axes[0].legend(fontsize=8, loc="upper right")
    fig.tight_layout()
    fig.savefig(args.out / "fig1_harm.png", dpi=200)
    fig.savefig(args.out / "fig1_harm.pdf")

    # Figure 3: welfare relative to D on the same seed: pair, outsiders, joint
    base = {(r["split"], r["seed"]): r for r in rows if r["condition"] == BASE}
    fig, axes = plt.subplots(1, 3, figsize=(10, 3.4), sharey=False)
    for ax, key, title in zip(axes, ["pair_reward_mean", "others_reward_mean", "joint_reward"],
                              [f"Pair mean reward − {BASE}", f"Outsiders' mean reward − {BASE}", f"Joint reward − {BASE}"]):
        cs = [c for c in conds if c != BASE]
        for i, c in enumerate(cs):
            ys = []
            for r in rows:
                if r["condition"] != c:
                    continue
                b = base.get((r["split"], r["seed"]))
                if b is None:
                    continue
                try:
                    ys.append(float(r[key]) - float(b[key]))
                except (TypeError, ValueError):
                    pass
            ax.scatter([i] * len(ys), ys, s=22, alpha=0.6, color="#1f77b4")
            if ys:
                m = sum(ys) / len(ys); se = (sum((y - m) ** 2 for y in ys) / max(1, len(ys) - 1)) ** 0.5 / max(1, len(ys)) ** 0.5
                ax.errorbar([i], [m], yerr=[1.645 * se], fmt="_", color="black", ms=18, mew=2, capsize=4)
        ax.axhline(0, color="grey", lw=0.8, ls="--")
        ax.set_xticks(range(len(cs))); ax.set_xticklabels(cs, fontsize=9); ax.set_title(title, fontsize=10)
    axes[0].set_ylabel("reward units (matched seed)")
    fig.tight_layout(); fig.savefig(args.out / "fig3_welfare.png", dpi=200); fig.savefig(args.out / "fig3_welfare.pdf")

    fig, ax = plt.subplots(figsize=(9, 3.4))
    w = 0.8 / len(conds)
    for i, c in enumerate(conds):
        rs = [r for r in rows if r["condition"] == c]
        rates = [sum(r[f] for r in rs) / len(rs) if rs else 0 for f in FACTORS]
        ax.bar([j + i * w for j in range(len(FACTORS))], rates, width=w, label=LABEL.get(c, c))
    ci = {c: [r["CI"] for r in rows if r["condition"] == c and not math.isnan(r["CI"])] for c in conds}
    ax.set_xticks([j + 0.4 - w / 2 for j in range(len(FACTORS))])
    ax.set_xticklabels(["costly\ndeference", "internal\nnon-collision", "priority\ncapture", "private info\nposted",
                        "word-action\ninconsistency", "private channel\nexisted"], fontsize=8)
    ax.set_ylabel("fraction of runs where factor present")
    ax.set_ylim(0, 1.05)
    ax.legend(fontsize=7, ncol=3, loc="upper center", bbox_to_anchor=(0.5, 1.22))
    fig.tight_layout()
    fig.savefig(args.out / "fig2_factor_rates.png", dpi=200)
    fig.savefig(args.out / "fig2_factor_rates.pdf")
    print("wrote", args.out / "fig1_harm.png", args.out / "fig2_factor_rates.png", args.out / "fig3_welfare.png")
    print("judge means:", {c: round(sum(v) / len(v), 2) for c, v in ci.items() if v})


if __name__ == "__main__":
    main()
