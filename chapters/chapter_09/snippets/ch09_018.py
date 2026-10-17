# Chapter: 9
# Section: 9.7 Python 실습 — 기본 반응표면 모델과 시각화
# Type: SNIPPET
# Status: SNIPPET_UNTESTED
# Origin: Word paragraph(s) 2520–2520
# Note: Independent execution NOT guaranteed. Original text preserved below.

import numpy as np

def response_surface(x1, x2):
    return (
        20.0
        - 2.0 * x1**2
        - 3.0 * x2**2
        + 2.0 * x1 * x2
    )

print(response_surface(0, 0))
print(response_surface(1, 1))
print(response_surface(-1, -1))
