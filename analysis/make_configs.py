"""Derive the four matched-condition configs from the shipped Colosseum hackathon configs.

Changes relative to the shipped files, and nothing else:
  * seeds: the list given on the command line (pre-registered: 1-5 train, 6-10 test)
  * max_planning_rounds: 4 (the Colosseum paper default; shipped files use 2 to save calls)
  * output_dir: under plus-factors/results/raw/<condition>
  * model: optional override so every condition uses exactly the same model id

Usage:
  python make_configs.py --seeds 1 2 3 4 5 --model Qwen/Qwen2.5-7B-Instruct
"""
from __future__ import annotations

import argparse
import copy
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
COLOSSEUM = PROJECT.parent / "collusion_hackathon" / "colosseum"
SHIPPED = COLOSSEUM / "experiments" / "collusion" / "configs"

CONDITIONS = {
    "A": "hackathon_2_1_a_pair_private_channel.yaml",
    "B": "hackathon_2_1_b_pair_no_channel.yaml",
    "C": "hackathon_2_1_c_open_channel.yaml",
    "D": "hackathon_2_1_d_neither.yaml",
    # E: derived from A (private pair channel) with the coalition prompt switched off.
    "E": "hackathon_2_1_a_pair_private_channel.yaml",
}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, nargs="+", required=True)
    ap.add_argument("--rounds", type=int, default=4)
    ap.add_argument("--model", default=None, help="exact model id for every agent")
    ap.add_argument("--concurrency", type=int, default=2)
    ap.add_argument("--tag", default="", help="suffix for output dir, e.g. train or test")
    ap.add_argument("--variant", default=None,
                    help="coalition prompt variant for prompted conditions (A, B): simple | deception | structured | aggressive")
    ap.add_argument("--only", nargs="*", default=None, help="subset of condition codes")
    ap.add_argument("--code-suffix", default="", help="appended to the condition code, e.g. dec -> Adec")
    ap.add_argument("--num-agents", type=int, default=None, help="override communication_network.num_agents (Study 2 uses 6)")
    args = ap.parse_args()

    out_cfg_dir = PROJECT / "configs"
    out_cfg_dir.mkdir(exist_ok=True)
    for code, fname in CONDITIONS.items():
        if args.only and code not in args.only:
            continue
        base = yaml.safe_load((SHIPPED / fname).read_text())
        cfg = copy.deepcopy(base)
        cfg["simulation"]["max_planning_rounds"] = args.rounds
        cfg["experiment"]["seeds"] = list(args.seeds)
        cfg["experiment"]["max_concurrent_runs"] = args.concurrency
        suffix = f"_{args.tag}" if args.tag else ""
        # Output path is relative to the colosseum working dir, as the runner expects.
        if args.model:
            for m in cfg["llm_models"]:
                m["llm"]["openrouter"]["model"] = args.model
        if code == "E":
            cfg["experiment"].setdefault("collusion", {})["coalition_prompt"] = "never"
            cfg["experiment"]["collusion"]["extra_channel_members"] = "colluders"
            for sw in cfg["experiment"]["sweeps"]:
                sw["prompt_variants"] = ["control"]
                sw["secret_channel_enabled"] = [True]
            cfg["simulation"]["tags"] = ["pf_E_private_channel_no_prompt"]
        if args.num_agents:
            cfg["communication_network"]["num_agents"] = args.num_agents
            for sw in cfg["experiment"]["sweeps"]:
                sw["num_agents"] = [args.num_agents]
        code = code + args.code_suffix
        if args.variant:
            for sw in cfg["experiment"]["sweeps"]:
                if sw.get("prompt_variants") != ["control"]:
                    sw["prompt_variants"] = [args.variant]
        rel_out = Path("..") / ".." / "plus-factors" / "results" / "raw" / f"{code}{suffix}"
        cfg["experiment"]["output_dir"] = str(rel_out)
        cfg["experiment"]["tag"] = f"pf_{code}{suffix}"
        target = out_cfg_dir / f"pf_{code}{suffix}.yaml"
        header = (
            f"# Derived from colosseum/experiments/collusion/configs/{fname}\n"
            f"# by plus-factors/analysis/make_configs.py. Only seeds, planning rounds,\n"
            f"# output_dir/tag and (optionally) the model id differ from the shipped file.\n"
        )
        target.write_text(header + yaml.safe_dump(cfg, sort_keys=False))
        print("wrote", target.relative_to(PROJECT))


if __name__ == "__main__":
    main()
