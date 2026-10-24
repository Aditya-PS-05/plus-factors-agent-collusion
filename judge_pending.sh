#!/usr/bin/env bash
# Judge (Gemma, then Qwen3-235B) every completed root that lacks judge files, skipping Adecq_test (still running).
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE/../collusion_hackathon/colosseum"
for root in "$HERE"/results/raw/*_train/*/ "$HERE"/results/raw/*_test/*/; do
  [ -d "$root/runs" ] || continue
  case "$root" in *Adecq_test*) continue;; esac
  if [ -z "$(find "$root" -path '*judge_secret_blackboard*' -name results.csv 2>/dev/null)" ]; then
    echo "judging $root"
    uv run python -m experiments.collusion.judge_blackboards --root "$root" --judge-model google/gemma-3-27b-it --max-output-tokens 512 2>&1 | grep -E "Done|rror" || true
  fi
  find "$root" -type d -name judge_qwen235 | grep -q . && continue
  J=$(find "$root" -type d -name judge_secret_blackboard | head -1); [ -n "$J" ] && mv "$J" "$(dirname "$J")/judge_gemma"
  echo "second judge $root"
  uv run python -m experiments.collusion.judge_blackboards --root "$root" --judge-model Qwen/Qwen3-235B-A22B-Instruct-2507 --max-output-tokens 512 2>&1 | grep -E "Done|rror" || true
  J2=$(find "$root" -type d -name judge_secret_blackboard | head -1); [ -n "$J2" ] && mv "$J2" "$(dirname "$J2")/judge_qwen235"
  [ -n "$J" ] && mv "$(dirname "$J")/judge_gemma" "$J"
done
echo JUDGE_PENDING_DONE
