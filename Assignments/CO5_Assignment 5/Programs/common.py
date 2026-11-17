"""Shared utilities and consistent paths for ITA06 Assignment 5 (CO5)."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / 'Datasets'
OUT = ROOT / 'Outputs'
GRAPHS = ROOT / 'Graphs'
DIAGRAMS = ROOT / 'Diagrams'
for _p in [DATA, OUT, GRAPHS, DIAGRAMS]: _p.mkdir(parents=True, exist_ok=True)

def to_builtin(obj):
    if isinstance(obj, (np.integer,)): return int(obj)
    if isinstance(obj, (np.floating,)): return float(obj)
    if isinstance(obj, np.ndarray): return obj.tolist()
    if isinstance(obj, (pd.Timestamp,)): return obj.isoformat()
    if isinstance(obj, pd.DataFrame): return obj.to_dict(orient='records')
    if isinstance(obj, pd.Series): return obj.to_dict()
    if isinstance(obj, Path): return str(obj)
    raise TypeError(f'Cannot JSON serialize {type(obj)!r}')

def save_json(num, data):
    (OUT / f'Q{num}_results.json').write_text(json.dumps(data, indent=2, default=to_builtin), encoding='utf-8')

def read_prod(name='Production_Cleaned_1000.csv'):
    return pd.read_csv(DATA/name, parse_dates=['Date'], float_precision='round_trip')

def clean_production(raw, *, strict_key=True):
    """Remove exact duplicates; normalize; impute missing with machine/group medians."""
    df = raw.copy()
    initial = len(df)
    df = df.drop_duplicates().copy()
    n_dup = initial - len(df)
    df['Date'] = pd.to_datetime(df['Date'], errors='raise')
    old_line = df['Line'].copy()
    df['Line'] = df['Line'].astype(str).str.strip().str.upper()
    n_line = int((old_line != df['Line']).sum())
    for c in ['Output_Units', 'Defects']:
        df[c] = pd.to_numeric(df[c], errors='coerce')
    miss_out = int(df['Output_Units'].isna().sum())
    miss_def = int(df['Defects'].isna().sum())
    out_machine_med = df.groupby('Machine_ID')['Output_Units'].transform('median')
    df['Output_Units'] = df['Output_Units'].fillna(out_machine_med).fillna(df['Output_Units'].median()).round().astype('int32')
    if 'Shift' in df.columns:
        def_group_med = df.groupby(['Machine_ID', 'Shift'])['Defects'].transform('median')
    else:
        def_group_med = df.groupby('Machine_ID')['Defects'].transform('median')
    df['Defects'] = df['Defects'].fillna(def_group_med).fillna(df['Defects'].median()).round().astype('int32')
    if (df['Output_Units'] <= 0).any(): raise ValueError('Output_Units must be positive')
    if (df['Defects'] < 0).any(): raise ValueError('Defects must be nonnegative')
    df['Defect_Rate'] = df['Defects'] / df['Output_Units']
    keys = ['Machine_ID', 'Date'] + (['Shift'] if 'Shift' in df.columns else [])
    conflicts = int(df.duplicated(keys).sum())
    if strict_key and conflicts: raise ValueError(f'Duplicate production keys after cleaning: {conflicts}')
    log = dict(raw_rows=initial, duplicate_rows_removed=n_dup, line_values_standardised=n_line,
               output_values_filled=miss_out, defect_values_filled=miss_def, cleaned_rows=len(df),
               conflicting_keys=conflicts)
    return df.reset_index(drop=True), log
