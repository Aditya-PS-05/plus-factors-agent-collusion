#!/usr/bin/env bash
# Run the four matched conditions for one seed split.
# Usage: ./run_conditions.sh train   (uses configs/pf_*_train.yaml)
#        ./run_conditions.sh test
set -euo pipefail
split="${1:?train|test}"
HERE="$(cd "$(dirname "$0")" && pwd)"
COLO="$HERE/../collusion_hackathon/colosseum"
cd "$COLO"
for code in A B C D; do
  cfg="$HERE/configs/pf_${code}_${split}.yaml"
  echo "=== condition $code ($split) ==="
  uv run python -m experiments.collusion.run --config "$cfg" -y 2>&1 | tee -a "$HERE/results/run_${code}_${split}.log"
done
