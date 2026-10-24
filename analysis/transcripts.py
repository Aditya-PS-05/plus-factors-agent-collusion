"""Extract example transcripts (the pair's posts, with board membership) for the report appendix.
Usage: python transcripts.py results/measures.csv --picks A:1 B:10 Adec:1 D:1 --out report/appendix_transcripts.md"""
from __future__ import annotations
import argparse, csv, json
from pathlib import Path


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("measures", type=Path); ap.add_argument("--picks", nargs="+", required=True)
    ap.add_argument("--out", type=Path, required=True); ap.add_argument("--maxlen", type=int, default=420)
    a = ap.parse_args()
    rows = {(r["condition"], int(float(r["seed"]))): r for r in csv.DictReader(open(a.measures)) if r["split"] in ("train", "test")}
    L = ["## Appendix C: Example transcripts\n", "The scored pair's posts in order, with the members of the board each post went to. Posts are truncated. Private costs posted by agents are their own.\n"]
    for pick in a.picks:
        c, s = pick.split(":"); r = rows[(c, int(s))]; d = Path(r["run_dir"])
        fs = json.load(open(d / "final_summary.json")); m = json.load(open(d / "metrics.json"))
        pair = [x["agent_name"] for x in m["agents"] if x["role"] == "colluder"]
        L.append(f"### Condition {c}, seed {s} (pair: {', '.join(pair)})\n")
        L.append("Final claims and rewards: " + "; ".join(f"{k}{'*' if k in pair else ''} → {(v or 'skip').split('::')[-1]} ({fs['agent_rewards'][k]:+.1f})" for k, v in fs["assignment"].items()) + ". Coalition advantage " + f"{float(r['H']):+.1f}" + f", judge {float(r['CI']):.1f}/5.\n")
        for bb in json.load(open(d / "blackboards.json")):
            for e in bb["events"]:
                if e["kind"] == "communication" and e["agent"] in pair:
                    txt = e["payload"].get("content", "").replace("\n", " ")
                    L.append(f"- **{e['agent']}** → board {bb['blackboard_id']} {bb['participants']}: {txt[:a.maxlen]}{'…' if len(txt) > a.maxlen else ''}")
        L.append("")
    a.out.write_text("\n".join(L) + "\n"); print("wrote", a.out, len(L), "lines")


if __name__ == "__main__":
    main()
