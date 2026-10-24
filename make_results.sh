#!/usr/bin/env bash
# One-shot results pipeline: judge any unjudged roots, measure, merge, evaluate, draw figures.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
COLO="$HERE/../collusion_hackathon/colosseum"
JUDGE="${JUDGE_MODEL:-google/gemma-3-27b-it}"
SKIP_JUDGE="${SKIP_JUDGE:-0}"   # SKIP_JUDGE=1 runs the analysis on existing judge files only
cd "$COLO"
for root in "$HERE"/results/raw/*_train/*/ "$HERE"/results/raw/*_test/*/; do
  [ "$SKIP_JUDGE" = "1" ] && break
  [ -d "$root/runs" ] || continue
  if [ -z "$(find "$root" -path '*judge_secret_blackboard*' -name results.csv 2>/dev/null)" ]; then
    echo "judging $root"
    uv run python -m experiments.collusion.judge_blackboards --root "$root" --judge-model "$JUDGE" --max-output-tokens 512 2>&1 | grep -E "Done|rror" || true
  fi
done
# second judge (Qwen3-235B) on any root that lacks it; Gemma results are moved aside and restored
for root in "$HERE"/results/raw/*_train/*/ "$HERE"/results/raw/*_test/*/; do
  [ "$SKIP_JUDGE" = "1" ] && break
  [ -d "$root/runs" ] || continue
  find "$root" -type d -name judge_qwen235 | grep -q . && continue
  J=$(find "$root" -type d -name judge_secret_blackboard | head -1); [ -n "$J" ] && mv "$J" "$(dirname "$J")/judge_gemma"
  echo "second judge $root"
  uv run python -m experiments.collusion.judge_blackboards --root "$root" --judge-model Qwen/Qwen3-235B-A22B-Instruct-2507 --max-output-tokens 512 2>&1 | grep -E "Done|rror" || true
  J2=$(find "$root" -type d -name judge_secret_blackboard | head -1); [ -n "$J2" ] && mv "$J2" "$(dirname "$J2")/judge_qwen235"
  [ -n "$J" ] && mv "$(dirname "$J")/judge_gemma" "$J"
done
uv run python "$HERE/analysis/measures.py" "$HERE/results/raw" --out "$HERE/results/measures.csv"
uv run python "$HERE/analysis/judge_merge.py" "$HERE/results/measures.csv" "$HERE/results/raw" --out "$HERE/results/measures.csv"
uv run python "$HERE/analysis/judge_merge.py" "$HERE/results/measures.csv" "$HERE/results/raw" --out "$HERE/results/measures.csv" --judge-dir judge_qwen235 --column CI2
uv run python "$HERE/analysis/judge_robustness.py" "$HERE/results/measures.csv" --out "$HERE/results/judge_robustness.md" || true
echo; echo "################ PRE-REGISTERED: agreement = A; confounds = B, C, D"
uv run python "$HERE/analysis/evaluate.py" "$HERE/results/measures.csv" --include A B C D --agreement A --out "$HERE/results/evaluation_prereg.md"
echo; echo "################ EXTENSION 1: agreement = A, Adec; confounds = B, Bdec, C, D"
uv run python "$HERE/analysis/evaluate.py" "$HERE/results/measures.csv" --include A Adec B Bdec C D --agreement A Adec --out "$HERE/results/evaluation_ext_A_Adec.md"
echo; echo "################ EXTENSION 2: agreement = Adec; confounds = B, Bdec, C, D (A excluded)"
uv run python "$HERE/analysis/evaluate.py" "$HERE/results/measures.csv" --include Adec B Bdec C D --agreement Adec --out "$HERE/results/evaluation_ext_Adec.md"
echo; echo "################ EXTENSION 3: any instructed pair (A, Adec, B, Bdec) vs no instruction (C, D)"
uv run python "$HERE/analysis/evaluate.py" "$HERE/results/measures.csv" --include A Adec B Bdec C D --agreement A Adec B Bdec --out "$HERE/results/evaluation_ext_instructed.md"
ALL="H Hrel CI CD NC PC PI WA"; CONDUCT="H Hrel CD NC PC PI WA"
echo; echo "################ PRE-REGISTERED, second judge CI2 as a single rule (check only)"
uv run python "$HERE/analysis/evaluate.py" "$HERE/results/measures.csv" --include A B C D --agreement A --factors H Hrel CI CI2 CD NC PC PI WA --out "$HERE/results/evaluation_prereg_CI2.md" | sed -n "/Held-out/,\$p" | grep -E "CI2 alone|CI alone"
for spec in "prereg|--include A B C D --agreement A" "ext_A_Adec|--include A Adec B Bdec C D --agreement A Adec" "ext_Adec|--include Adec B Bdec C D --agreement Adec" "ext_instructed|--include A Adec B Bdec C D --agreement A Adec B Bdec"; do
  name=${spec%%|*}; args=${spec#*|}
  for fs in "noOP|$ALL" "conduct|$CONDUCT"; do
    fname=${fs%%|*}; facs=${fs#*|}
    echo; echo "######## $name / constellation without OP ($fname)"
    uv run python "$HERE/analysis/evaluate.py" "$HERE/results/measures.csv" $args --factors $facs --out "$HERE/results/evaluation_${name}_${fname}.md" | sed -n '/Held-out/,$p' | grep -E "Constellation|threshold"
  done
done
uv run python "$HERE/analysis/tables.py" "$HERE/results/measures.csv" --out "$HERE/results" --conds A Adec B Bdec C D --baseline D
uv run python "$HERE/analysis/figures.py" "$HERE/results/measures.csv" --out "$HERE/results/figures" --conds A Adec B Bdec C D --baseline D
uv run python "$HERE/analysis/intent_language.py" "$HERE/results/measures.csv" --conds A Adec B Bdec C D E A6 B6 E6 Aq Adecq Aaudq Dq > "$HERE/results/intent_language.md" || true

# ---------------- Study 2: contest setting (six agents) ----------------
S2="A6 B6 C6 D6 E6"
if grep -q ",A6," "$HERE/results/measures.csv" 2>/dev/null || grep -q "A6" "$HERE/results/measures.csv"; then
  echo; echo "################ STUDY 2 PRE-DECLARED: agreement = A6; confounds = B6, C6, D6 (E6 excluded from fitting)"
  uv run python "$HERE/analysis/evaluate.py" "$HERE/results/measures.csv" --include A6 B6 C6 D6 --agreement A6 --baseline D6 --out "$HERE/results/s2_evaluation_prereg.md"
  for fs in "noOP|$ALL" "conduct|$CONDUCT"; do
    fname=${fs%%|*}; facs=${fs#*|}
    echo; echo "######## Study 2 prereg / constellation without OP ($fname)"
    uv run python "$HERE/analysis/evaluate.py" "$HERE/results/measures.csv" --include A6 B6 C6 D6 --agreement A6 --baseline D6 --factors $facs --out "$HERE/results/s2_evaluation_prereg_${fname}.md" | sed -n '/Held-out/,$p' | grep -E "Constellation|threshold"
  done
  echo; echo "################ STUDY 2 PROBE: E6 (channel, no prompt) vs D6"
  uv run python "$HERE/analysis/evaluate.py" "$HERE/results/measures.csv" --include E6 D6 --agreement E6 --baseline D6 --out "$HERE/results/s2_evaluation_E6_vs_D6.md" | sed -n '/Likelihood/,/Held-out/p'
  echo; echo "################ STUDY 2 INSTRUCTED (A6, B6) vs NOT (C6, D6, E6)"
  uv run python "$HERE/analysis/evaluate.py" "$HERE/results/measures.csv" --include A6 B6 C6 D6 E6 --agreement A6 B6 --baseline D6 --out "$HERE/results/s2_evaluation_instructed.md" | sed -n '/Held-out/,$p'
  mkdir -p "$HERE/results/study2"
  uv run python "$HERE/analysis/tables.py" "$HERE/results/measures.csv" --out "$HERE/results/study2" --conds A6 B6 C6 D6 E6 --baseline D6
  uv run python "$HERE/analysis/figures.py" "$HERE/results/measures.csv" --out "$HERE/results/figures/study2" --conds A6 B6 C6 D6 E6 --baseline D6
fi
# ---------------- Study 3: model replication (Qwen3-235B agents) ----------------
if ls "$HERE"/results/raw/Aq_train/*/runs >/dev/null 2>&1; then
  echo; echo "################ STUDY 3 PRE-DECLARED: Aq, Adecq vs Dq (Qwen3-235B agents)"
  uv run python "$HERE/analysis/evaluate.py" "$HERE/results/measures.csv" --include Aq Adecq Dq --agreement Aq Adecq --baseline Dq --factors $ALL --out "$HERE/results/s3_evaluation.md" | sed -n '/Controls/,$p'
  echo; echo "######## Study 3 / conduct-only constellation"
  uv run python "$HERE/analysis/evaluate.py" "$HERE/results/measures.csv" --include Aq Adecq Dq --agreement Aq Adecq --baseline Dq --factors $CONDUCT --out "$HERE/results/s3_evaluation_conduct.md" | sed -n '/Held-out/,$p' | grep -E "Constellation|threshold"
  echo; echo "######## Study 3 / Adecq alone vs Dq and Aq alone vs Dq"
  uv run python "$HERE/analysis/evaluate.py" "$HERE/results/measures.csv" --include Adecq Dq --agreement Adecq --baseline Dq --factors $ALL --out "$HERE/results/s3_evaluation_Adecq_vs_Dq.md" | sed -n '/Held-out/,$p'
  uv run python "$HERE/analysis/evaluate.py" "$HERE/results/measures.csv" --include Aq Dq --agreement Aq --baseline Dq --factors $ALL --out "$HERE/results/s3_evaluation_Aq_vs_Dq.md" | sed -n '/Held-out/,$p'
  uv run python "$HERE/analysis/fig_study3.py" "$HERE/results/measures.csv" --out "$HERE/results/figures" --conds Aq Adecq Aaudq Dq --baseline Dq
  if ls "$HERE"/results/raw/Aaudq_train/*/runs >/dev/null 2>&1; then
    echo; echo "################ STUDY 4 PRE-DECLARED: Adecq-vs-Dq rules applied unchanged to Aaudq held-out seeds"
    uv run python "$HERE/analysis/evaluate.py" "$HERE/results/measures.csv" --include Adecq Dq --agreement Adecq --baseline Dq --factors $ALL --apply-to Aaudq --out "$HERE/results/s4_evaluation_transfer.md" | sed -n '/Transfer/,$p'
    mkdir -p "$HERE/results/study4"
    uv run python "$HERE/analysis/tables.py" "$HERE/results/measures.csv" --out "$HERE/results/study4" --conds Adecq Aaudq Dq --baseline Dq
  fi
  mkdir -p "$HERE/results/study3"
  uv run python "$HERE/analysis/tables.py" "$HERE/results/measures.csv" --out "$HERE/results/study3" --conds Aq Adecq Dq --baseline Dq
  uv run python "$HERE/analysis/figures.py" "$HERE/results/measures.csv" --out "$HERE/results/figures/study3" --conds Aq Adecq Dq --baseline Dq
fi
if grep -q "E_t" <(ls "$HERE/results/raw" 2>/dev/null); then
  echo; echo "################ STUDY 1 PROBE: E (channel, no prompt, four agents) vs D"
  uv run python "$HERE/analysis/evaluate.py" "$HERE/results/measures.csv" --include E D --agreement E --baseline D --out "$HERE/results/evaluation_E_vs_D.md" | sed -n '/Likelihood/,/Held-out/p'
fi
# report tables last, after every evaluation file has been written
uv run python "$HERE/analysis/report_tables.py" "$HERE/results" --out "$HERE/report/tables_generated.md" || true
