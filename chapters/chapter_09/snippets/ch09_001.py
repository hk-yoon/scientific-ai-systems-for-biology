# Chapter: 9
# Section: 9.2.5 무작위화(Randomization)
# Type: SNIPPET
# Status: SNIPPET_UNTESTED
# Origin: Word paragraph(s) 365–365
# Note: Independent execution NOT guaranteed. Original text preserved below.

import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
design = pd.DataFrame({
    "run_id": [1, 2, 3, 4, 5, 6],
    "temperature": [30, 30, 35, 35, 40, 40],
    "pH": [6.5, 7.5, 6.5, 7.5, 6.5, 7.5],
})
run_order = rng.permutation(len(design))
randomized_design = (
    design.iloc[run_order]
    .reset_index(drop=True))
randomized_design.insert(
    0,
    "execution_order",
    np.arange(1, len(design) + 1))
print(randomized_design)
