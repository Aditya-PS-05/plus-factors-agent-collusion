"""Merge Colosseum LLM-judge ratings into the measures table as the CI factor.

Colosseum's judge writes runs/<model>/judge_secret_blackboard/results.csv under each experiment
root with judge_mean_rating (mean of the three shipped rubrics, 0 to 5). For runs without a pair
channel the judge reads every blackboard and averages, which is the pre-registered fallback.

Usage: python judge_merge.py results/measures.csv results/raw --out results/measures.csv
"""
from __future__ import annotations

import argparse
import csv
import glob
from pathlib import Path


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("measures", type=Path)
    ap.add_argument("raw_root", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--judge-dir", default="judge_secret_blackboard", help="judge output folder name")
    ap.add_argument("--column", default="CI", help="measures column to fill")
    args = ap.parse_args()
    ratings = {}
    # Key = (experiment root, run_id). The judge CSV sits at <root>/runs/<model>/<judge_dir>/results.csv and a
    # run at <root>/runs/<model>/<sweep>/<run_id>; run ids repeat across studies, roots do not.
    for f in glob.glob(str(args.raw_root / "**" / args.judge_dir / "results.csv"), recursive=True):
        root = str(Path(f).resolve().parents[3])
        with open(f) as fh:
            for r in csv.DictReader(fh):
                if str(r.get("status", "")).startswith("judged") and r.get("judge_mean_rating") not in (None, ""):
                    ratings[(root, r["run_id"])] = float(r["judge_mean_rating"])
    with args.measures.open() as fh:
        rows = list(csv.DictReader(fh))
        fields = list(rows[0].keys()) if rows else []
    if args.column not in fields:
        fields.append(args.column)
        for r in rows:
            r[args.column] = "nan"
    hit = 0
    for r in rows:
        rd = Path(r["run_dir"]).resolve()
        rid = (str(rd.parents[3]), rd.name)
        if rid in ratings:
            r[args.column] = ratings[rid]
            hit += 1
    with args.out.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    print(f"merged judge ratings for {hit}/{len(rows)} runs -> {args.out}")


if __name__ == "__main__":
    main()
