# Run log

Every model call batch, with date, config, seeds, model, cost, and outcome.

| Date | Config | Seeds | Rounds | Model | Calls (est.) | Outcome |
|---|---|---|---|---|---|---|
| 2026-10-24 | pf_A_smoke | 1 | 2 | Qwen/Qwen3-30B-A3B-Instruct-2507 (Nebius) | ~20 | pipeline smoke test, not part of the study |
| 2026-10-24 | pf_A_train, pf_B_train, pf_C_train, pf_D_train | 1-5 | 4 | Qwen/Qwen3-30B-A3B-Instruct-2507 (Nebius) | ~4x5x60 | study, training split (A = positive control) |
| 2026-10-24 | judge, A to D train | 1-5 | - | google/gemma-3-27b-it (Nebius), 512 tok | 20x3 | re-judge after gpt-oss parse failures |
| 2026-10-24 | pf_Adec_train, pf_Bdec_train | 1-5 | 4 | Qwen/Qwen3-30B-A3B-Instruct-2507 (Nebius) | ~2x5x60 | extension: deception prompt variant |
| 2026-10-24 | pf_A_test, pf_B_test, pf_C_test, pf_D_test | 6-10 | 4 | Qwen/Qwen3-30B-A3B-Instruct-2507 (Nebius) | ~4x5x60 | study, held-out split |
| 2026-10-24 | pf_Adec_test, pf_Bdec_test | 6-10 | 4 | Qwen/Qwen3-30B-A3B-Instruct-2507 (Nebius) | ~2x5x60 | extension, held-out split |
| 2026-10-24 | all six conditions, test | 11-20 | 4 | Qwen/Qwen3-30B-A3B-Instruct-2507 (Nebius) | ~6x10x60 | held-out extension |
| 2026-10-24 | pf_A6/B6/C6/D6/E6 and pf_E, train+test | 1-20 | 4 | Qwen/Qwen3-30B-A3B-Instruct-2507 (Nebius) | ~6x20x90 | Study 2, contest setting |
| 2026-10-24 | pf_Aq/Adecq/Dq | 1-20 | 4 | Qwen/Qwen3-235B-A22B-Instruct-2507 (Nebius) | ~3x20x60 | Study 3, model replication |

## 2026-10-24 ~14:40 to 15:10 IST (after credit top-up)
- Adecq_test (seeds 6-20, Qwen3-235B agents): 15 runs, 15 completed, 0 failed. Root results/raw/Adecq_test/20261024-144107.
- Gemma 3 27B judge on C6, D6, E6, E (train+test), Aq, Dq, Adecq (train+test): 150 runs x 3 rubrics.
- Qwen3-235B second judge on the same roots: 150 runs x 3 rubrics.
- make_results.sh full pass; then report_tables.py re-run after the ordering fix (see CHANGELOG).
