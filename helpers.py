#!/usr/bin/env python

"""
    helpers.py
"""

import torch
import random
import numpy as np
from joblib import Parallel, delayed

from basenet.helpers import to_numpy

# --
# Accuracy helpers

def overlap(x, y):
    return len(set(x).intersection(y))

def precision_at_ks(act, pred, ks=[1, 5, 10]):
    out = {}
    
    for k in ks:
        ps = [overlap(act[i], pred[i][:k]) for i in range(len(act))]
        # print(np.sum(ps))
        out[k] = np.mean(ps) / k
    
    return out

def __filter_and_rank(pred, X_filter, k=10):
    pred_min = pred.min()
    for i in range(pred.shape[0]):
        pred[i][X_filter[i]] = pred_min
    
    return np.argsort(-pred, axis=-1)[:,:k]


def __rank(pred, k=10):
    return np.argsort(-pred, axis=-1)[:,:k]


def fast_topk(preds, X_filter=None, n_jobs=32):
    if X_filter is not None:
        offsets = np.cumsum([p.shape[0] for p in preds])
        offsets -= preds[0].shape[0]
        
        jobs = [delayed(__filter_and_rank)(
            to_numpy(pred),
            to_numpy(X_filter[offset:(offset + pred.shape[0])])
        ) for pred, offset in zip(preds, offsets)]
    else:
        jobs = [delayed(__rank)(to_numpy(pred)) for pred in preds]
    
    top_k = Parallel(n_jobs=n_jobs, backend='threading')(jobs)
    top_k = np.vstack(top_k)
    
    return top_k

