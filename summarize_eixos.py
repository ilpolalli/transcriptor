import argparse, os
import pandas as pd

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--coding_csv', required=True)
    ap.add_argument('--out_dir', required=True)
    args = ap.parse_args()

    df = pd.read_csv(args.coding_csv)
    os.makedirs(args.out_dir, exist_ok=True)

    # filtragem mínima: só linhas com Vezes preenchidas
    base = df.copy()
    base['Forca_1a3'] = pd.to_numeric(base.get('Forca_1a3', 1), errors='coerce').fillna(1).astype(int)

    # pivots
    eixo = (base.groupby('Eixo_BRJ_ENF_DI')['Forca_1a3']
            .sum().sort_values(ascending=False).reset_index())
    d_dim = (base.groupby('Dimensao_D1_D6')['Forca_1a3']
             .sum().sort_values(ascending=False).reset_index())

    eixo.to_csv(os.path.join(args.out_dir, 'sum_eixo.csv'), index=False)
    d_dim.to_csv(os.path.join(args.out_dir, 'sum_D1_D6.csv'), index=False)
    print('[OK] Análises guardadas em', args.out_dir)

if __name__ == '__main__':
    main()
