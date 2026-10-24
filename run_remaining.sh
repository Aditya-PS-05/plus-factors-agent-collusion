#!/usr/bin/env bash
# Relaunch what the credit cut interrupted: Adecq held-out seeds. Then run ./make_results.sh.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE/../collusion_hackathon/colosseum"
# remove the empty root left by the failed attempt(s) so the new run is the only Adecq_test root
for r in "$HERE"/results/raw/Adecq_test/*/; do [ -z "$(find "$r" -name final_summary.json 2>/dev/null)" ] && rm -rf "$r"; done
uv run python -m experiments.collusion.run --config "$HERE/configs/pf_Adecq_test.yaml" -y 2>&1 | grep -E "Wrote|EXPERIMENT END|rror"
echo "now run: $HERE/make_results.sh"
