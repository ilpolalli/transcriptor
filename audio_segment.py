import argparse, os
import numpy as np
import pandas as pd
import librosa

def segment_audio(audio_path: str, top_db: float = 32.0):
    y, sr = librosa.load(audio_path, sr=16000, mono=True)
    intervals = librosa.effects.split(y, top_db=top_db, frame_length=2048, hop_length=512)
    rows = []
    for i, (s, e) in enumerate(intervals, 1):
        st = s / sr
        et = e / sr
        rows.append({"segmento": i, "inicio_s": round(st,3), "fim_s": round(et,3), "duracao_s": round(et-st,3)})
    return pd.DataFrame(rows), y, sr, intervals

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--audio', required=True)
    ap.add_argument('--out_csv', required=True)
    ap.add_argument('--top_db', type=float, default=32.0)
    ap.add_argument('--min_dur', type=float, default=0.0, help='filtra segmentos abaixo desta duração (s)')
    args = ap.parse_args()

    df, y, sr, intervals = segment_audio(args.audio, top_db=args.top_db)
    if args.min_dur > 0:
        df = df[df['duracao_s'] >= args.min_dur].copy()
    os.makedirs(os.path.dirname(args.out_csv), exist_ok=True)
    df.to_csv(args.out_csv, index=False)
    print(f"[OK] {len(df)} segmentos guardados em {args.out_csv}")

if __name__ == '__main__':
    main()
