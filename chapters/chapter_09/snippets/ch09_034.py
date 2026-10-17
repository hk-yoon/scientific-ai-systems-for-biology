# Chapter: 9
# Section: 9.10 Python 실습 — RSM 기반 실험 최적화의 통합 구현
# Type: SNIPPET
# Status: SNIPPET_UNTESTED
# Origin: Word paragraph(s) 4104–4104
# Note: Independent execution NOT guaranteed. Original text preserved below.

def predict_viability(x):
    A, B, C = x
    return (
        96.0
        - 2.0*(A - 0.05)**2
        - 2.0*(B + 0.15)**2
        - 1.5*(C + 0.1)**2
        - 0.8*A*C
    )
def predict_byproduct(x):
    A, B, C = x
    return (
        1.5
        + 0.65*C
        + 0.35*A**2
        + 0.30*B**2
    )
