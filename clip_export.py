import argparse, os
import numpy as np
import pandas as pd
import soundfile as sf
import librosa

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--audio', required=True)
    ap.add_argument('--segments_csv', required=True)
    ap.add_argument('--out_dir', required=True)
    args = ap.parse_args()

    y, sr = librosa.load(args.audio, sr=16000, mono=True)
    segs = pd.read_csv(args.segments_csv)
    os.makedirs(args.out_dir, exist_ok=True)

    for _, r in segs.iterrows():
        i = int(r['segmento'])
        s = int(r['inicio_s'] * sr)
        e = int(r['fim_s'] * sr)
        clip = y[s:e]
        name = f"clip_{i:03d}_{r['inicio_s']:.2f}-{r['fim_s']:.2f}s.wav"
        outp = os.path.join(args.out_dir, name)
        sf.write(outp, clip, sr)
    print(f"[OK] {len(segs)} clips exportados em {args.out_dir}")

if __name__ == '__main__':
    main()
