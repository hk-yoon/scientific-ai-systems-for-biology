# Chapter: 9
# Section: 9.5 Python 실습 — 부분요인설계와 Alias Structure
# Type: SNIPPET
# Status: SNIPPET_UNTESTED
# Origin: Word paragraph(s) 1532–1532
# Note: Independent execution NOT guaranteed. Original text preserved below.

import itertools
import numpy as np
import pandas as pd

# Base factors A and B
runs = list(
    itertools.product([-1, 1], repeat=2))
design = pd.DataFrame(
    runs,
    columns=["A", "B"])
# Generator: C = AB
design["C"] = design["A"] * design["B"]
# Interaction columns
design["AB"] = design["A"] * design["B"]
design["AC"] = design["A"] * design["C"]
design["BC"] = design["B"] * design["C"]
design["ABC"] = (
    design["A"] * design["B"] * design["C"])
print(design)
