import argparse, os
import pandas as pd

BASE_COLS = [
    'Voz','Porque','Lugar','Dimensao_D1_D6','Eixo_BRJ_ENF_DI','Forca_1a3','Fonte_(A/V/D/M)','Observacoes'
]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--segments_csv', required=False)
    ap.add_argument('--pdf_csv', required=False)
    ap.add_argument('--out_csv', required=True)
    ap.add_argument('--out_xlsx', required=True)
    args = ap.parse_args()

    frames = []
    if args.segments_csv and os.path.exists(args.segments_csv):
        segs = pd.read_csv(args.segments_csv)
        segs['Voz'] = ''
        segs['Porque'] = ''
        segs['Lugar'] = ''
        segs['Dimensao_D1_D6'] = ''
        segs['Eixo_BRJ_ENF_DI'] = ''
        segs['Forca_1a3'] = ''
        segs['Fonte_(A/V/D/M)'] = 'A'
        segs['Observacoes'] = 'clip'
        frames.append(segs[['segmento','inicio_s','fim_s','duracao_s'] + BASE_COLS])

    if args.pdf_csv and os.path.exists(args.pdf_csv):
        pdf = pd.read_csv(args.pdf_csv)
        pdf = pdf.rename(columns={'Voz':'Voz'})
        pdf['segmento'] = ''
        pdf['inicio_s'] = ''
        pdf['fim_s'] = ''
        pdf['duracao_s'] = ''
        pdf['Porque'] = ''
        pdf['Lugar'] = ''
        pdf['Dimensao_D1_D6'] = ''
        pdf['Eixo_BRJ_ENF_DI'] = ''
        pdf['Forca_1a3'] = ''
        pdf['Fonte_(A/V/D/M)'] = 'D'
        pdf['Observacoes'] = pdf['ficheiro'].astype(str) + ' p.' + pdf['pag'].astype(str)
        frames.append(pdf[['segmento','inicio_s','fim_s','duracao_s','Voz'] + BASE_COLS])

    if not frames:
        raise SystemExit('Sem fontes válidas (segments_csv/pdf_csv).')

    out = pd.concat(frames, ignore_index=True)
    os.makedirs(os.path.dirname(args.out_csv), exist_ok=True)
    out.to_csv(args.out_csv, index=False)

    try:
        import openpyxl  # noqa
        out.to_excel(args.out_xlsx, index=False, sheet_name='Codificacao')
    except Exception:
        pass

    print(f"[OK] Folha criada: {args.out_csv} / {args.out_xlsx} (linhas={len(out)})")

if __name__ == '__main__':
    main()
