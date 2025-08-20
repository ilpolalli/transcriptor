import argparse, glob, os, re
import pandas as pd
import pdfplumber

HEADERS = re.compile(r'^(Folhas|Flores|Vozes|T[íi]tulos|Nome|Data|Sess[aã]o|Torres Vedras)\b', re.I)

def extract_from_pdf(path):
    out = []
    with pdfplumber.open(path) as pdf:
        for pi, page in enumerate(pdf.pages, 1):
            text = page.extract_text() or ''
            for line in [l.strip() for l in text.splitlines()]:
                if 3 <= len(line) <= 140 and not HEADERS.match(line):
                    out.append({'ficheiro': os.path.basename(path), 'pag': pi, 'Voz': line})
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pdf_glob', required=True, help='ex: data/*.pdf')
    ap.add_argument('--out_csv', required=True)
    args = ap.parse_args()

    paths = glob.glob(args.pdf_glob)
    rows = []
    for p in paths:
        rows.extend(extract_from_pdf(p))
    df = pd.DataFrame(rows).drop_duplicates()
    os.makedirs(os.path.dirname(args.out_csv), exist_ok=True)
    df.to_csv(args.out_csv, index=False)
    print(f"[OK] {len(df)} linhas extraídas de {len(paths)} PDFs -> {args.out_csv}")

if __name__ == '__main__':
    main()
