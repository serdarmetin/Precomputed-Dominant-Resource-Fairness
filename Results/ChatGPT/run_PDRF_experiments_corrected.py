#!/usr/bin/env python3
"""Reproduce the eight PDRF experiment configurations" 

The raw output files retain the whitespace-separated integer format used by
Statistics.ipynb. The three-category 'More' counts count users once, using the
first resource coordinate because task-count discrepancies are identical over
all resource coordinates.
"""
from __future__ import annotations

import heapq
import ctypes
from pathlib import Path
import numpy as np

_LIB = ctypes.CDLL('/mnt/data/libdrf_heap.so')
_PTR_I64 = ctypes.POINTER(ctypes.c_int64)
_PTR_F64 = ctypes.POINTER(ctypes.c_double)
_LIB.drf_heap_run.argtypes = [_PTR_I64, _PTR_I64, _PTR_F64, ctypes.c_int, ctypes.c_int, _PTR_I64, _PTR_I64]
_LIB.drf_heap_run.restype = None

N_USERS = 1000
REPETITIONS = 1000
SEED = 20261031
OUT = Path('/mnt/data/PDRF_experiment_results')
OUT.mkdir(exist_ok=True)

CONFIGS = [
    (10, 50_000, 100_000, 1, 10),
    (10, 50_000, 100_000, 1, 20),
    (10, 50_000, 100_000, 10, 20),
    (2, 500_000, 1_000_000, 1, 100),
    (2, 500_000, 1_000_000, 1, 1000),
]


def drf_array_reference(d: np.ndarray, r: np.ndarray, ds: np.ndarray) -> np.ndarray:
    """Original array-selection semantics, retained for equivalence testing."""
    n = len(d)
    shares = np.zeros(n, dtype=np.float64)
    counts = np.zeros(n, dtype=np.int64)
    consumed = np.zeros(len(r), dtype=np.int64)
    while True:
        min_share = np.min(shares)
        candidates = np.flatnonzero(shares == min_share)
        i = candidates[np.argmax(ds[candidates])]
        if (r < consumed + d[i]).any():
            break
        counts[i] += 1
        shares[i] += ds[i]
        consumed += d[i]
    return counts


def drf_heap(d: np.ndarray, r: np.ndarray, ds: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Heap implementation equivalent to min-share / max-ds / first-index tie-break."""
    n = len(d)
    shares = np.zeros(n, dtype=np.float64)
    counts = np.zeros(n, dtype=np.int64)
    consumed = np.zeros(len(r), dtype=np.int64)
    heap = [(0.0, -float(ds[i]), i, 0) for i in range(n)]
    heapq.heapify(heap)
    versions = np.zeros(n, dtype=np.int64)

    while heap:
        share, neg_ds, i, version = heapq.heappop(heap)
        if version != versions[i]:
            continue
        # This is the first selected user's next task; preserve stop-on-infeasible.
        if (r < consumed + d[i]).any():
            break
        counts[i] += 1
        consumed += d[i]
        shares[i] += ds[i]
        versions[i] += 1
        heapq.heappush(heap, (float(shares[i]), -float(ds[i]), i, int(versions[i])))
    return counts, consumed


def pdrf_counts(d: np.ndarray, r: np.ndarray, ds: np.ndarray) -> np.ndarray:
    ds_max = np.max(ds)
    rates = ds_max / ds
    cycle_demands = np.sum(rates[:, None] * d, axis=0)
    cycle_iterations = np.min(r / cycle_demands)
    return np.floor(rates * cycle_iterations).astype(np.int64)


def summarize(drf_counts: np.ndarray, pdrf_counts: np.ndarray, heuristic_better: int | None = None) -> list[int]:
    # Each user's task-count discrepancy is repeated over resources in the
    # original allocation matrices. The first coordinate counts each user once.
    difference = drf_counts - pdrf_counts
    col = difference
    row = [
        int(np.count_nonzero(col == 1)),
        int(np.count_nonzero(col == 2)),
        int(np.count_nonzero(col > 2)),
        int(col.max()),
        int(np.count_nonzero(col > 0)),
        int(np.count_nonzero(col == -1)),
        int(np.count_nonzero(col == -2)),
        int(np.count_nonzero(col < -2)),
        int(abs(col.min())),
        int(np.count_nonzero(col < 0)),
    ]
    if heuristic_better is not None:
        row.append(int(heuristic_better))
    return row


def one_trial(rng: np.random.Generator, config: tuple[int, int, int, int, int], use_heuristic: bool) -> list[int]:
    m, r_low, r_high_inclusive, d_low, d_high_inclusive = config
    r = rng.integers(r_low, r_high_inclusive + 1, size=m, dtype=np.int64)
    d = rng.integers(d_low, d_high_inclusive + 1, size=(N_USERS, m), dtype=np.int64)
    ds = (d / r).max(axis=1)

    drf_counts = np.empty(N_USERS, dtype=np.int64)
    c_drf = np.empty(m, dtype=np.int64)
    _LIB.drf_heap_run(
        d.ctypes.data_as(_PTR_I64), r.ctypes.data_as(_PTR_I64),
        ds.ctypes.data_as(_PTR_F64), N_USERS, m,
        drf_counts.ctypes.data_as(_PTR_I64), c_drf.ctypes.data_as(_PTR_I64)
    )
    p_counts = pdrf_counts(d, r, ds)
    c_pdrf = np.sum(p_counts[:, None] * d, axis=0)

    if use_heuristic:
        # Match the original np.argsort(s_pdrf) one-pass heuristic exactly.
        s_pdrf = ds * p_counts
        for i in np.argsort(s_pdrf):
            if (r - c_pdrf >= d[i]).all():
                p_counts[i] += 1
                c_pdrf += d[i]
        return summarize(drf_counts, p_counts, int((c_pdrf - c_drf > 0).all()))
    return summarize(drf_counts, p_counts)


def verify_heap_equivalence() -> None:
    rng = np.random.default_rng(7919)
    for _ in range(20):
        m = int(rng.integers(2, 6))
        d = rng.integers(1, 10, size=(30, m), dtype=np.int64)
        r = rng.integers(100, 250, size=m, dtype=np.int64)
        ds = (d / r).max(axis=1)
        expected = drf_array_reference(d, r, ds)
        actual, _ = drf_heap(d, r, ds)
        if not np.array_equal(expected, actual):
            raise RuntimeError('Heap DRF differs from the original array-selection implementation.')


def main() -> None:
    verify_heap_equivalence()
    seed_sequence = np.random.SeedSequence(SEED)
    child_seeds = iter(seed_sequence.spawn(len(CONFIGS) * 2))
    for config in CONFIGS:
        m, rlo, rhi, dlo, dhi = config
        stem = f'results_{N_USERS}_{m}_{rlo}_{rhi}_{dlo}_{dhi}'
        for heuristic in (False, True):
            label = stem + ('_heuristic' if heuristic else '')
            rng = np.random.default_rng(next(child_seeds))
            path = OUT / label
            with path.open('w', encoding='ascii') as f:
                for _ in range(REPETITIONS):
                    row = one_trial(rng, config, heuristic)
                    f.write(' '.join(map(str, row)) + '\n')
            data = np.loadtxt(path, dtype=np.int64)
            print(f'Completed {label}: shape={data.shape}')
            print('  mean:', np.average(data, axis=0))
            print('  std: ', np.std(data, axis=0))
            print('  max: ', np.max(data, axis=0))


if __name__ == '__main__':
    main()
