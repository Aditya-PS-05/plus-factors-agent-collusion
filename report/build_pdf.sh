#!/usr/bin/env bash
# Build the report PDF from report.md (+ appendices) with pandoc and xelatex.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE"
python3 - <<'PY'
from pathlib import Path
s = Path("report.md").read_text()
s = s.replace("[CHANGELOG]", Path("../CHANGELOG.md").read_text().replace("# Changelog for the pre-registration", "").strip())
g = Path("tables_generated.md").read_text()
import re as _re
tab1 = _re.search(r"(Table 1\..*?)\n\n(\| Factor.*?)\n\n", g, _re.S)
tab2 = _re.search(r"(Table 2\..*?)\n\n(\| Rule.*?)(?:\n\n|\Z)", g, _re.S)
s = s.replace("[TABLE1]", tab1.group(2) + "\n\n" + tab1.group(1) + "\n")
s = s.replace("[TABLE2]", tab2.group(2).rstrip() + "\n\n" + tab2.group(1) + "\n")
# Appendix C (transcripts) is inserted before Appendix D so the appendices read A, B, C, D
if Path("appendix_transcripts.md").exists():
    t = Path("appendix_transcripts.md").read_text().strip() + "\n\n"
    s = s.replace("## Appendix D:", t + "## Appendix D:", 1)
Path("_full.md").write_text(s)
PY
pandoc _full.md -o report.pdf --pdf-engine=xelatex \
  -V geometry:margin=1.9cm -V fontsize=10pt -V mainfont="DejaVu Serif" -V monofont="DejaVu Sans Mono" \
  -V colorlinks=true -V linkcolor=blue -V urlcolor=blue --resource-path=.:../results/figures \
  --metadata title="" 2>&1 | grep -v "^\[WARNING\] Missing character" || true
pdfinfo report.pdf | grep -E "Pages|File size" || true
