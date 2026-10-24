"""Plus-factor evaluation: likelihood ratios, a constellation rule fitted on training seeds,
and held-out evaluation on test seeds. Implements the pre-registered analysis plan.

Usage: python evaluate.py results/measures.csv [--out results/evaluation.md]
"""
from __future__ import annotations

import argparse
import csv
import math
import random
from pathlib import Path
from typing import Dict, List, Optional, Sequence

BOOL_FACTORS = ["CD", "NC", "PC", "PI", "WA", "OP"]
CONT_FACTORS = ["H", "Hrel", "CI", "CI2"]  # thresholded on training seeds; CI2 = second judge
ALL_FACTORS = CONT_FACTORS + BOOL_FACTORS
AGREEMENT = {"A"}
CONFOUNDS = {"B", "C", "D"}
ALPHA = 0.5  # Laplace smoothing, pre-registered


BASELINE = "D"


def load(path: Path) -> List[Dict]:
    with path.open() as f:
        rows = [r for r in csv.DictReader(f) if r.get("status") == "complete" and r.get("split") in ("train", "test")]
    for r in rows:
        for k in ALL_FACTORS + ["seed", "pair_reward_mean"]:
            v = r.get(k, "")
            try:
                r[k] = float(v)
            except (TypeError, ValueError):
                r[k] = float("nan")
    # Hrel: pair mean reward minus the pair's mean reward in condition D on the same seed
    # (pre-registered under measure 1; the matched-pair harm measure).
    base = {(r["split"], r["seed"]): r["pair_reward_mean"] for r in rows if r["condition"] == BASELINE}
    for r in rows:
        b = base.get((r["split"], r["seed"]))
        r["Hrel"] = (r["pair_reward_mean"] - b) if b is not None else float("nan")
    return rows


def choose_threshold(rows: Sequence[Dict], key: str) -> Optional[float]:
    """Threshold on a continuous measure maximising balanced accuracy on the given rows."""
    vals = sorted({r[key] for r in rows if not math.isnan(r[key])})
    if len(vals) < 2:
        return None
    best_t, best_ba = None, -1.0
    for i in range(len(vals) - 1):
        t = (vals[i] + vals[i + 1]) / 2
        ba = balanced_accuracy([(r["condition"] in AGREEMENT, r[key] > t) for r in rows if not math.isnan(r[key])])
        if ba > best_ba:
            best_t, best_ba = t, ba
    return best_t


def balanced_accuracy(pairs: Sequence[tuple]) -> float:
    tp = sum(1 for y, p in pairs if y and p)
    fn = sum(1 for y, p in pairs if y and not p)
    tn = sum(1 for y, p in pairs if not y and not p)
    fp = sum(1 for y, p in pairs if not y and p)
    tpr = tp / (tp + fn) if tp + fn else 0.0
    tnr = tn / (tn + fp) if tn + fp else 0.0
    return (tpr + tnr) / 2


def binarise(rows: Sequence[Dict], thresholds: Dict[str, float]) -> List[Dict]:
    out = []
    for r in rows:
        b = dict(r)
        for k in ALL_FACTORS:
            v = r[k]
            if math.isnan(v):
                b[k + "_b"] = None
            elif k in thresholds:
                b[k + "_b"] = bool(v > thresholds[k])
            else:
                b[k + "_b"] = bool(v >= 0.5)
        out.append(b)
    return out


def likelihood_ratio(rows: Sequence[Dict], key: str, pos: set, neg: set) -> Dict[str, float]:
    p_rows = [r for r in rows if r["condition"] in pos and r[key + "_b"] is not None]
    n_rows = [r for r in rows if r["condition"] in neg and r[key + "_b"] is not None]
    p = (sum(r[key + "_b"] for r in p_rows) + ALPHA) / (len(p_rows) + 2 * ALPHA)
    q = (sum(r[key + "_b"] for r in n_rows) + ALPHA) / (len(n_rows) + 2 * ALPHA)
    return {"P_F_given_C": p, "P_F_given_notC": q, "S": p / q if q > 0 else float("inf"),
            "n_pos": len(p_rows), "n_neg": len(n_rows)}


def bootstrap_S(rows: Sequence[Dict], key: str, pos: set, neg: set, B: int = 2000, seed: int = 0):
    rng = random.Random(seed)
    seeds = sorted({int(r["seed"]) for r in rows if not math.isnan(r["seed"])})
    if not seeds:
        return (float("nan"), float("nan"))
    vals = []
    for _ in range(B):
        pick = [rng.choice(seeds) for _ in seeds]
        sub = [r for s in pick for r in rows if int(r["seed"]) == s]
        vals.append(likelihood_ratio(sub, key, pos, neg)["S"])
    vals.sort()
    return (vals[int(0.05 * B)], vals[int(0.95 * B) - 1])


def constellation_score(row: Dict, lrs: Dict[str, Dict[str, float]], factors: Sequence[str]) -> float:
    """Naive-Bayes log odds contributed by the observed factors."""
    s = 0.0
    for k in factors:
        b = row.get(k + "_b")
        if b is None:
            continue
        p, q = lrs[k]["P_F_given_C"], lrs[k]["P_F_given_notC"]
        s += math.log(p / q) if b else math.log((1 - p) / (1 - q))
    return s


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("measures", type=Path)
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--factors", nargs="*", default=None, help="subset for the constellation")
    ap.add_argument("--agreement", nargs="*", default=["A"], help="condition codes that count as agreement")
    ap.add_argument("--exclude", nargs="*", default=[], help="condition codes to drop entirely")
    ap.add_argument("--include", nargs="*", default=None, help="keep only these condition codes")
    ap.add_argument("--baseline", default="D", help="condition used as the matched baseline for Hrel")
    args = ap.parse_args()
    global AGREEMENT, CONFOUNDS, BASELINE
    BASELINE = args.baseline
    rows = [r for r in load(args.measures) if r["condition"] not in set(args.exclude)]
    if args.include:
        rows = [r for r in rows if r["condition"] in set(args.include)]
    AGREEMENT = set(args.agreement)
    CONFOUNDS = {r["condition"] for r in rows} - AGREEMENT
    P0 = print
    train = [r for r in rows if r["split"] == "train"]
    test = [r for r in rows if r["split"] == "test"]
    lines: List[str] = []
    P = lines.append
    P(f"# Plus-factor evaluation\n")
    P(f"Runs: {len(rows)} complete ({len(train)} train, {len(test)} test). "
      f"Agreement={sorted(AGREEMENT)} confounds={sorted(CONFOUNDS)}. Conditions: " + ", ".join(f"{c}={sum(1 for r in rows if r['condition']==c)}" for c in sorted({r['condition'] for r in rows})) + "\n")

    # Positive / negative controls on training seeds
    def mean(xs):
        xs = [x for x in xs if not math.isnan(x)]
        return sum(xs) / len(xs) if xs else float("nan")
    P("## Controls (training seeds)\n")
    conds = sorted({r["condition"] for r in rows}, key=lambda c: (len(c), c))
    for c in conds:
        hs = [r["H"] for r in train if r["condition"] == c]
        hr = [r["Hrel"] for r in train if r["condition"] == c]
        ci = [r["CI"] for r in train if r["condition"] == c]
        P(f"- Condition {c}: mean coalition advantage {mean(hs):+.2f}, pair reward vs D same seed {mean(hr):+.2f}, "
          f"judge mean {mean(ci):.2f}, over {len(hs)} runs")
    P("")

    # Thresholds for continuous factors, chosen on train only
    thresholds = {}
    for k in CONT_FACTORS:
        t = choose_threshold(train, k)
        if t is not None:
            thresholds[k] = t
    P("## Thresholds (chosen on training seeds only)\n")
    for k, t in thresholds.items():
        P(f"- {k} > {t:.3f}")
    P("")
    btrain = binarise(train, thresholds)
    btest = binarise(test, thresholds)

    # Likelihood ratios
    P(f"## Likelihood ratios S = P[F given {'+'.join(sorted(AGREEMENT))}] / P[F given {'+'.join(sorted(CONFOUNDS))}] on training seeds\n")
    P("| Factor | P[F given agreement] | P[F given confound] | S | 90% bootstrap | " + " | ".join(f"vs {c}" for c in sorted(CONFOUNDS)) + " |")
    P("|---" * (5 + len(CONFOUNDS)) + "|")
    lrs: Dict[str, Dict[str, float]] = {}
    for k in ALL_FACTORS:
        lr = likelihood_ratio(btrain, k, AGREEMENT, CONFOUNDS)
        if lr["n_pos"] == 0:
            continue
        lrs[k] = lr
        lo, hi = bootstrap_S(btrain, k, AGREEMENT, CONFOUNDS)
        per = [likelihood_ratio(btrain, k, AGREEMENT, {c})["S"] for c in sorted(CONFOUNDS)]
        P(f"| {k} | {lr['P_F_given_C']:.2f} | {lr['P_F_given_notC']:.2f} | {lr['S']:.2f} | [{lo:.2f}, {hi:.2f}] | "
          + " | ".join(f"{s:.2f}" for s in per) + " |")
    P("")

    # Decision rules evaluated on held-out seeds
    factors = args.factors or [k for k in lrs if k != "CI2" and not math.isnan(lrs[k]["S"])]
    P(f"## Held-out evaluation (test seeds), constellation over {factors}\n")
    # threshold on constellation log-odds chosen on train
    tr_scores = [(r["condition"] in AGREEMENT, constellation_score(r, lrs, factors)) for r in btrain]
    cands = sorted({s for _, s in tr_scores})
    best_t, best_ba = 0.0, -1
    for i in range(len(cands) - 1):
        t = (cands[i] + cands[i + 1]) / 2
        ba = balanced_accuracy([(y, s > t) for y, s in tr_scores])
        if ba > best_ba:
            best_t, best_ba = t, ba
    P(f"Constellation threshold (log-odds) chosen on train: {best_t:.3f} (train balanced accuracy {best_ba:.2f})\n")
    P("| Rule | Balanced acc. [90% seed bootstrap] | TPR on agreement | " + " | ".join(f"FPR on {c}" for c in sorted(CONFOUNDS)) + " |")
    P("|---" * (3 + len(CONFOUNDS)) + "|")

    def ba_interval(pred, B=2000, seed=0):
        rng = random.Random(seed)
        seeds_t = sorted({int(r["seed"]) for r in btest})
        vals = []
        for _ in range(B):
            pick = [rng.choice(seeds_t) for _ in seeds_t]
            sub = [r for sd in pick for r in btest if int(r["seed"]) == sd]
            vals.append(balanced_accuracy([(r["condition"] in AGREEMENT, pred(r)) for r in sub]))
        vals.sort()
        return vals[int(0.05 * B)], vals[int(0.95 * B) - 1]

    def report(name, pred):
        pairs = [(r["condition"] in AGREEMENT, pred(r)) for r in btest]
        ba = balanced_accuracy(pairs)
        lo, hi = ba_interval(pred)
        tpr = mean([float(p) for (y, p), r in zip(pairs, btest) if r["condition"] in AGREEMENT])
        fprs = [mean([float(p) for (y, p), r in zip(pairs, btest) if r["condition"] == c]) for c in sorted(CONFOUNDS)]
        P(f"| {name} | {ba:.2f} [{lo:.2f}, {hi:.2f}] | {tpr:.2f} | " + " | ".join(f"{x:.2f}" for x in fprs) + " |")

    if btest:
        report("Harm alone (H)", lambda r: bool(r.get("H_b")))
        for k in factors:
            if k != "H":
                report(f"{k} alone", lambda r, k=k: bool(r.get(k + "_b")))
        report("Constellation", lambda r: constellation_score(r, lrs, factors) > best_t)
    else:
        P("| (no test runs yet) |" + " |" * (2 + len(CONFOUNDS)))
    P("")
    text = "\n".join(lines)
    print(text)
    if args.out:
        args.out.write_text(text)


if __name__ == "__main__":
    main()
