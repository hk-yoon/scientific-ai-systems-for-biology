# Chapter: 9
# Section: 9.8.9 Python을 이용한 RSM Design Matrix 생성
# Type: SNIPPET
# Status: SNIPPET_UNTESTED
# Origin: Word paragraph(s) 3073–3073
# Note: Independent execution NOT guaranteed. Original text preserved below.

import itertools
import numpy as np
import pandas as pd

k = 3
n_center = 5
alpha = (2**k)**0.25
# Factorial points
factorial_points = np.array(
    list(itertools.product([-1.0, 1.0], repeat=k)),
    dtype=float)
# Axial points
axial_points = []
for i in range(k):
    for sign in [-1.0, 1.0]:
        point = np.zeros(k)
        point[i] = sign * alpha
        axial_points.append(point)
axial_points = np.array(axial_points)
# Center points
center_points = np.zeros((n_center, k))
# Complete CCD
ccd_points = np.vstack([
    factorial_points,
    axial_points,
    center_points])
