#!/usr/bin/env bash
# Build the ROenglishRE pre-renewal overlay for a given client, same order as
# the project's Tools/ClientGenerator.bat: Renewal -> Pre-Renewal -> every
# Compatibility/<date> up to the client's date (Pre-Renewal subfolder first).
# Usage: build_english_prere.sh <ROenglishRE dir> <output dir> <last compat date>
#   e.g. build_english_prere.sh ROenglishRE english-prere 2021-10-28
set -euo pipefail
R="$1/Translation"; OUT="$2"; LAST="$3"
rm -rf "$OUT"; mkdir -p "$OUT"
cp -a "$R/Renewal/." "$OUT/"
cp -a "$R/Pre-Renewal/." "$OUT/"
# Exact list from ClientGenerator.bat's loop (it skips some folders, e.g. 2020-01-22)
DATES="2017-06-14 2017-12-13 2018-06-20 2019-06-05 2020-09-02 2021-10-28 2022-03-30 2022-04-06
2022-06-02 2022-08-31 2022-09-28 2022-12-07 2023-01-18 2023-08-02 2023-09-20 2024-03-11 2024-04-03
2024-05-02 2024-08-07 2024-10-16 2025-01-22 2025-06-18 2025-09-02 2025-12-17"
for d in $DATES; do
  [[ "$d" > "$LAST" ]] && break
  src="$R/Compatibility/$d"; [ -d "$src/Pre-Renewal" ] && src="$src/Pre-Renewal"
  cp -a "$src/." "$OUT/"; echo "applied $d"
done
