"""Descriptive tables for the report: per-seed H and judge, factor counts on test seeds, welfare vs D,
and outsider-outcome mechanism table. Usage: python tables.py results/measures.csv --out results/"""
from __future__ import annotations
import argparse, csv, json, statistics as st
from pathlib import Path

CONDS = ["A", "Adec", "B", "Bdec", "C", "D"]
F = ["CD", "NC", "PC", "PI", "WA", "OP"]


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("measures", type=Path); ap.add_argument("--out", type=Path, required=True); ap.add_argument("--conds", nargs="*", default=None); ap.add_argument("--baseline", default="D")
    a = ap.parse_args()
    global CONDS
    if a.conds: CONDS = a.conds
    B = a.baseline
    rows = [r for r in csv.DictReader(open(a.measures)) if r["split"] in ("train", "test") and r["status"] == "complete"]
    by = {(r["condition"], int(float(r["seed"]))): r for r in rows}
    seeds = sorted({int(float(r["seed"])) for r in rows})
    f = float
    L = []
    L.append("# Per-seed coalition advantage H, judge mean in brackets\n")
    L.append("| seed | split | " + " | ".join(CONDS) + " |"); L.append("|---" * (2 + len(CONDS)) + "|")
    for s in seeds:
        cells = [(f"{f(by[(c,s)]['H']):+.1f} [{f(by[(c,s)]['CI']):.1f}]" if (c, s) in by else "-") for c in CONDS]
        L.append(f"| {s} | {by[(CONDS[0], s)]['split'] if (CONDS[0], s) in by else '?'} | " + " | ".join(cells) + " |")
    L.append("\n# Factor counts on TEST seeds\n")
    L.append("| cond | n test | mean H | mean judge (Gemma) | mean judge 2 (Qwen-235B) | " + " | ".join(F) + " |"); L.append("|---" * (5 + len(F)) + "|")
    for c in CONDS:
        rs = [r for r in rows if r["condition"] == c and r["split"] == "test"]
        if not rs: continue
        ci2 = [f(r["CI2"]) for r in rs if r.get("CI2") not in (None, "", "nan")]
        L.append(f"| {c} | {len(rs)} | {st.mean(f(r['H']) for r in rs):+.2f} | {st.mean(f(r['CI']) for r in rs):.2f} | {(st.mean(ci2) if ci2 else float('nan')):.2f} | " + " | ".join(str(sum(int(r[k]) for r in rs)) for k in F) + " |")
    L.append("\n# Welfare by condition, all seeds; matched differences vs D on the same seed (mean ± s.e.)\n")
    L.append("| cond | n | pair reward | outsiders' reward | joint reward | violations | pair − D | outsiders − D | joint − D |"); L.append("|---" * 9 + "|")
    def m(x): return f"{st.mean(x):+.1f} ± {st.stdev(x)/len(x)**0.5:.1f}" if len(x) > 1 else (f"{x[0]:+.1f}" if x else "-")
    for c in CONDS:
        rs = [r for r in rows if r["condition"] == c]
        if not rs: continue
        dp = [f(by[(c,s)]["pair_reward_mean"]) - f(by[(B,s)]["pair_reward_mean"]) for s in seeds if (c,s) in by and (B,s) in by]
        do = [f(by[(c,s)]["others_reward_mean"]) - f(by[(B,s)]["others_reward_mean"]) for s in seeds if (c,s) in by and (B,s) in by]
        dj = [f(by[(c,s)]["joint_reward"]) - f(by[(B,s)]["joint_reward"]) for s in seeds if (c,s) in by and (B,s) in by]
        L.append(f"| {c} | {len(rs)} | {st.mean(f(r['pair_reward_mean']) for r in rs):.1f} | {st.mean(f(r['others_reward_mean']) for r in rs):.1f} | "
                 f"{st.mean(f(r['joint_reward']) for r in rs):.1f} | {st.mean(f(r['violations']) for r in rs):.2f} | {m(dp)} | {m(do)} | {m(dj)} |")
    L.append("\n# Outsider outcomes by condition (totals over all seeds; posts are per-run means)\n")
    L.append("| cond | n | outsider skips | outsiders with reward ≤ 0 | outsider collisions | pair collisions with outsiders | pair public posts | pair private posts | outsiders' posts |"); L.append("|---" * 9 + "|")
    for c in CONDS:
        sk = inf = col = pcol = pub = priv = opost = n = 0
        for r in rows:
            if r["condition"] != c: continue
            d = Path(r["run_dir"]); fs = json.load(open(d / "final_summary.json")); mt = json.load(open(d / "metrics.json"))
            pair = [x["agent_name"] for x in mt["agents"] if x["role"] == "colluder"]; others = [x["agent_name"] for x in mt["agents"] if x["role"] != "colluder"]
            asg = fs["assignment"]; rw = fs["agent_rewards"]; n += 1
            for o in others:
                if asg.get(o) in (None, "skip"): sk += 1
                elif rw[o] <= 0: inf += 1
                if asg.get(o) and sum(1 for x, t in asg.items() if x != o and t == asg[o]) > 0: col += 1
            pcol += int(r["pair_vs_other_collisions"]); pub += int(r["n_posts_pair_public"]); priv += int(r["n_posts_pair_private"])
            bbs = json.load(open(d / "blackboards.json"))
            opost += sum(1 for bb in bbs for e in bb["events"] if e["kind"] == "communication" and e["agent"] in others)
        if n: L.append(f"| {c} | {n} | {sk} | {inf} | {col} | {pcol} | {pub/n:.1f} | {priv/n:.1f} | {opost/n:.1f} |")
    (a.out / "tables.md").write_text("\n".join(L) + "\n"); print("\n".join(L))


if __name__ == "__main__":
    main()
