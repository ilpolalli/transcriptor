# Pipeline Conselho das Crianças — Sessão 1.2 (Codex-ready)

Este repositório é um **esqueleto operacional** pensado para ser usado com o **OpenAI Codex** (agente de engenharia na cloud) ou localmente.
O objetivo é **automatizar**: segmentação de áudio, export de clips, extração de texto de PDFs, criação de folha de codificação, e síntese por **Eixos** e **D1–D6**.

## Estrutura
- `src/audio_segment.py` — segmenta áudio e gera CSV com timeline.
- `src/clip_export.py` — exporta clips .wav a partir do timeline.
- `src/pdf_extract.py` — extrai textos curtos de PDFs (Vozes, Balões, Folhas/Flores, Títulos).
- `src/coding_sheet.py` — gera folha de codificação (CSV/XLSX) pronta a preencher.
- `src/summarize_eixos.py` — agrega resultados por Eixos e D1–D6 (tabelas .csv).
- `src/manifest.py` — cria manifest de fontes para trilho de auditoria.
- `scripts/run_full_pipeline.sh` — exemplo de orquestração em bash.

## Instalação (local)
```bash
python -m venv .venv && source .venv/bin/activate  # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt
```

## Exemplos de uso
```bash
# 1) Segmentar áudio (gera segments.csv)
python src/audio_segment.py   --audio "data/1_Partilha da voz.mp3"   --out_csv "out/segments.csv"   --top_db 32 --min_dur 2.0

# 2) Exportar clips .wav para out/clips/
python src/clip_export.py   --audio "data/1_Partilha da voz.mp3"   --segments_csv "out/segments.csv"   --out_dir "out/clips"

# 3) Extrair vozes de PDFs (gera out/pdf_excerpts.csv)
python src/pdf_extract.py --pdf_glob "data/*.pdf" --out_csv "out/pdf_excerpts.csv"

# 4) Criar folha de codificação (XLSX + CSV)
python src/coding_sheet.py   --segments_csv "out/segments.csv"   --pdf_csv "out/pdf_excerpts.csv"   --out_csv "out/coding_sheet.csv"   --out_xlsx "out/coding_sheet.xlsx"

# 5) Agregar por Eixos e D1–D6 (precisa coding_sheet com códigos preenchidos)
python src/summarize_eixos.py --coding_csv "out/coding_sheet.csv" --out_dir "out/analytics"
```

## Privacidade
- **Anonimizar** IDs e remover PII. Não subir áudio bruto ao repositório público.
- Usar o Codex em ambientes com **acesso controlado**, sem dados sensíveis por defeito.
