import argparse, glob, os, pandas as pd

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--glob', required=True, help='ex: data/*')
    ap.add_argument('--out_csv', required=True)
    args = ap.parse_args()

    paths = glob.glob(args.glob)
    rows = [{'id': i+1, 'path': p, 'bytes': os.path.getsize(p)} for i, p in enumerate(paths)]
    df = pd.DataFrame(rows)
    os.makedirs(os.path.dirname(args.out_csv), exist_ok=True)
    df.to_csv(args.out_csv, index=False)
    print(f'[OK] Manifest com {len(df)} itens -> {args.out_csv}')

if __name__ == '__main__':
    main()
