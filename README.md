# Plus factors for AI agent collusion

Sprint project for the Apart Research AI Collusion Research Sprint (23 to 25 Oct 2026),
Track 2, question 2.3: what should count as convincing evidence of collusion?

We take the antitrust "plus factor" standard (conduct that is likely under an agreement and
unlikely without one, scored as a likelihood ratio) and compute it from logged trajectories
of LLM agents in the Colosseum Jira ticket task. Four matched conditions supply ground truth:
a deliberate coalition with a private channel, a shared instruction without a channel, an
open channel without an agreement, and a plain baseline.

Read `PREREGISTRATION.md` first. Study 1 was frozen before the first run; Studies 2 and 3 are addenda declared before their own runs. `CHANGELOG.md` dates every deviation.

**Status (24 Oct 2026):** All three studies complete: 300 study runs (Study 1 120, Study 2 120, Study 3 60), every run rated by both judges. The Nebius credit ran out part-way through Study 3; the remaining Adecq held-out runs and judging were completed after a top-up with the configs unchanged (see CHANGELOG.md). `./make_results.sh` reproduces every table and figure from `results/raw`.

## Layout

| Path | What |
|---|---|
| `PREREGISTRATION.md` | Hypotheses, conditions, measures, analysis plan, failure criteria. Frozen. |
| `CHANGELOG.md` | Any deviation from the pre-registration, with reason. |
| `RUNLOG.md` | Every batch of model calls: config, seeds, model, cost, outcome. |
| `analysis/make_configs.py` | Derives the condition configs from the shipped Colosseum ones. |
| `analysis/measures.py` | Computes the plus-factor measures from a run directory. |
| `analysis/evaluate.py` | Likelihood ratios, decision rule on train seeds, evaluation on test seeds. |
| `configs/` | Generated configs. Only seeds, rounds, output dir and model differ from shipped. |
| `run_conditions.sh` | Runs the four original conditions for one seed split. |
| `make_results.sh` | One command: judge, measure, merge, evaluate every framing, tables, figures. |
| `analysis/tables.py`, `analysis/figures.py`, `analysis/transcripts.py`, `analysis/judge_merge.py` | Descriptive tables, figures, transcript appendix, judge merge. |
| `report/build_pdf.sh` | Builds report.pdf from report.md with pandoc and xelatex. |
| `results/raw/` | Colosseum run artifacts (not committed; large). |
| `results/` | Derived tables and figures. |
| `report/` | The sprint report source. |

## Pre-existing code

Colosseum (Nakamura et al. 2026), Terrarium and CoLLAB are prior work, vendored by the
sprint's starter repo at `../collusion_hackathon/colosseum`, used unchanged. The hackathon
condition configs are by Poseidon Research. Everything in this directory is new sprint work.

## Reproduce

```bash
# 1. key: put NEBIUS_API_KEY or OPENROUTER_API_KEY in ../collusion_hackathon/compute.env
# 2. configs (already generated; rerun to change seeds/model)
cd ../collusion_hackathon/colosseum
uv run python ../../plus-factors/analysis/make_configs.py --seeds 1 2 3 4 5 --tag train
uv run python ../../plus-factors/analysis/make_configs.py --seeds 6 7 8 9 10 --tag test
# 3. runs
../../plus-factors/run_conditions.sh train
../../plus-factors/run_conditions.sh test
# 4. analysis (judge + measures + evaluation + tables + figures)
../../plus-factors/make_results.sh
#    (run_remaining.sh and judge_pending.sh are the one-off helpers used after the credit top-up; make_results.sh alone is sufficient from scratch)
# 5. report
../../plus-factors/report/build_pdf.sh
```
