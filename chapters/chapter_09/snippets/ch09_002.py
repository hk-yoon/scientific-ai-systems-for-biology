# Chapter: 9
# Section: 9.4.4 설계 행렬과 요인 수준의 코딩 (Design Matrix and Factor Coding)
# Type: SNIPPET
# Status: SNIPPET_UNTESTED
# Origin: Word paragraph(s) 922–922
# Note: Independent execution NOT guaranteed. Original text preserved below.

import itertools
import numpy as np

factors = np.asarray(list(itertools.product([-1, 1], repeat=3)), dtype=float)
a, b, c = factors.T
X = np.column_stack([np.ones(8), a, b, c, a*b, a*c, b*c, a*b*c])
G = X.T @ X
assert np.array_equal(G, np.eye(8) * 8)
print(G)
