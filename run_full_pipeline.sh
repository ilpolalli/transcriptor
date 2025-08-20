#!/usr/bin/env bash
set -e

AUDIO="data/1_Partilha da voz.mp3"
OUT="out"

mkdir -p "$OUT" "$OUT/clips"

python src/audio_segment.py --audio "$AUDIO" --out_csv "$OUT/segments.csv" --top_db 32 --min_dur 2.0
python src/clip_export.py --audio "$AUDIO" --segments_csv "$OUT/segments.csv" --out_dir "$OUT/clips"
python src/pdf_extract.py --pdf_glob "data/*.pdf" --out_csv "$OUT/pdf_excerpts.csv"
python src/coding_sheet.py --segments_csv "$OUT/segments.csv" --pdf_csv "$OUT/pdf_excerpts.csv" --out_csv "$OUT/coding_sheet.csv" --out_xlsx "$OUT/coding_sheet.xlsx"
