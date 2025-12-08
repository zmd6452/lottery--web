import pandas as pd
import numpy as np
import os
from collections import Counter

def parse_magnum(df):
    if 'number' in df.columns:
        col = 'number'
    elif 'results' in df.columns:
        col = 'results'
    else:
        col = df.columns[0]
    nums = df[col].astype(str).str.strip().str.zfill(4)
    return nums.tolist()

def parse_toto(df):
    for c in ['number','num','result']:
        if c in df.columns:
            nums = df[c].astype(str).str.strip().str.zfill(4)
            return nums.tolist()
    dcols = [c for c in df.columns if c.lower().startswith('d') or 'digit' in c.lower()]
    if len(dcols) >=4:
        nums = df[dcols].astype(str).agg(''.join, axis=1)
        nums = nums.str.zfill(4)
        return nums.tolist()
    return parse_magnum(df)

def parse_damacai(df):
    return parse_magnum(df)

def normalize_file(path):
    df = pd.read_csv(path)
    cols = [c.lower() for c in df.columns]
    if any('magnum' in c for c in cols) or 'number' in cols or 'results' in cols:
        return parse_magnum(df)
    elif any('toto' in c for c in cols) or any(c.startswith('d') for c in cols):
        return parse_toto(df)
    else:
        return parse_magnum(df)

def analyze_files(paths, last_n=100):
    all_nums = []
    file_map = {}
    for p in paths:
        if not os.path.exists(p):
            continue
        nums = normalize_file(p)
        file_map[os.path.basename(p)] = nums
        all_nums.extend(nums)
    if len(all_nums) == 0:
        return {'error': 'no numbers found'}
    recent = all_nums[-last_n:]
    pos_counts = [Counter() for _ in range(4)]
    overall = Counter()
    pair_co = Counter()
    for num in recent:
        if len(num) < 4:
            num = num.zfill(4)
        digits = list(num[:4])
        for i,d in enumerate(digits):
            pos_counts[i][d] += 1
            overall[d] += 1
        for i in range(4):
            for j in range(i+1,4):
                pair_co[(digits[i], digits[j])] += 1
    pos_freq = [{k:v for k,v in c.most_common()} for c in pos_counts]
    overall_freq = {k:v for k,v in overall.most_common()}
    pairs = {f"{a}{b}": v for (a,b),v in pair_co.items()}
    return {
        'recent_count': len(recent),
        'position_frequency': pos_freq,
        'overall_frequency': overall_freq,
        'pair_cooccurrence': pairs,
        'files_parsed': {k: len(v) for k,v in file_map.items()}
    }
