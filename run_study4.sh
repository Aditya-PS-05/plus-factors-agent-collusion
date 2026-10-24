#!/usr/bin/env bash
# Study 4: Aaudq train (seeds 1-5) then test (seeds 6-20), Qwen3-235B agents. Then ./make_results.sh judges and evaluates.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE/../collusion_hackathon/colosseum"
for split in train test; do
  uv run python -m experiments.collusion.run --config "$HERE/configs/pf_Aaudq_${split}.yaml" -y 2>&1 | grep -E "Wrote|EXPERIMENT END|rror"
done
echo STUDY4_RUNS_DONE
