# Chapter: 9
# Section: 9.4.9 Python을 이용한 요인설계 생성과 분석
# Type: SNIPPET
# Status: SNIPPET_UNTESTED
# Origin: Word paragraph(s) 1129–1129
# Note: Independent execution NOT guaranteed. Original text preserved below.

import itertools
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
levels = [-1, 1]
factor_combinations = list(
    itertools.product(levels, repeat=3))
design = pd.DataFrame(
    factor_combinations,
    columns=["A", "B", "C"])
# Actual factor values
design["temperature"] = 35 + 5 * design["A"]
design["pH"] = 7 + design["B"]
design["glucose"] = 10 + 5 * design["C"]
print(design)
