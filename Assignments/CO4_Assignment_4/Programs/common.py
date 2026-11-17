"""Shared reproducible sampling and evaluation utilities for ITA06 Assignment 4."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'Datasets'
OUTPUT = ROOT / 'Outputs'
GRAPH = ROOT / 'Graphs'
RESULT = ROOT / 'Results'
DIAGRAM = ROOT / 'Diagrams'
SEEDS = (17, 29, 41)
KS = (1, 3, 5, 7, 9, 15, 25)

def draw_q2(n, seed):
    """Two informative values, one thousand times the other's numerical scale."""
    rng = np.random.default_rng(int(seed))
    a, b = rng.normal(size=(2, n))
    score = 1.20*np.sin(1.35*a) + 0.85*b + 0.35*a*b
    y = (score > 0).astype(int)
    y[rng.random(n) < 0.06] ^= 1
    return np.column_stack((1000*a, b)), y

def q2_split(seed):
    X, y = draw_q2(1000, seed)
    ix = np.arange(1000)
    tr, other = train_test_split(ix, train_size=0.6, random_state=seed+202, stratify=y)
    va, te = train_test_split(other, test_size=0.5, random_state=seed+203, stratify=y[other])
    return X, y, {'train':tr, 'validation':va, 'test':te}

def add_irrelevant(X, seed, count):
    if not count: return X.copy()
    # Identical nested first-random-features across dimensions and evaluations.
    rng = np.random.default_rng(seed+1005)
    extra = rng.normal(size=(len(X), 50))
    return np.column_stack((X, extra[:, :count]))

def inverse_square(d):
    d = np.asarray(d, dtype=float)
    return 1.0/np.maximum(d, 1e-12)**2

def knn(k, vote='uniform', algorithm='brute'):
    return KNeighborsClassifier(n_neighbors=int(k), weights=(inverse_square if vote=='distance' else 'uniform'),
                                algorithm=algorithm, n_jobs=1)

def write_json(filename, data):
    def convert(obj):
        if isinstance(obj, np.generic): return obj.item()
        if isinstance(obj, np.ndarray): return obj.tolist()
        if isinstance(obj, Path): return str(obj)
        raise TypeError(type(obj))
    (RESULT / filename).write_text(json.dumps(data, indent=2, default=convert), encoding='utf8')

def save_table(filename, records):
    pd.DataFrame(records).to_csv(RESULT / filename, index=False)

def fixed_scale(X, ix):
    s = StandardScaler().fit(X[ix['train']])
    return s.transform(X), s
