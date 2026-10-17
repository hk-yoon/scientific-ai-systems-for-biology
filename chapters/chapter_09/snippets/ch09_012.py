# Chapter: 9
# Section: 9.6 Python 실습 — 회귀, ANOVA, 잔차 및 Lack-of-Fit 검증
# Type: SNIPPET
# Status: SNIPPET_UNTESTED
# Origin: Word paragraph(s) 2055–2055
# Note: Independent execution NOT guaranteed. Original text preserved below.

import itertools
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
# Four factorial corner points
corner_points = list(
    itertools.product([-1.0, 1.0], repeat=2))
# Add one center point
design_points = corner_points + [(0.0, 0.0)]
n_replicates = 5
rows = []
for point_id, (A, B) in enumerate(design_points, start=1):
    for replicate in range(1, n_replicates + 1):
        rows.append({
            "point_id": point_id,
            "replicate": replicate,
            "A": A,
            "B": B
        })
data = pd.DataFrame(rows)
A = data["A"].to_numpy()
B = data["B"].to_numpy()
# Synthetic response with curvature
true_response = (
    15
    + 2.0 * A
    + 1.0 * B
    + 1.5 * A * B
    - 3.0 * A**2
    - 2.0 * B**2)
noise = rng.normal(
    loc=0.0,
    scale=0.4,
    size=len(data))
data["response"] = true_response + noise
# Randomize execution order
order = rng.permutation(len(data))
data = data.iloc[order].reset_index(drop=True)
data.insert(
    0,
    "execution_order",
    np.arange(1, len(data) + 1))
