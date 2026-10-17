# Chapter: 9
# Section: 9.10 Python 실습 — RSM 기반 실험 최적화의 통합 구현
# Type: SNIPPET
# Status: SNIPPET_UNTESTED
# Origin: Word paragraph(s) 4135–4135
# Note: Independent execution NOT guaranteed. Original text preserved below.

def decode_conditions(x):
    A, B, C = x
    return {
        "temperature_C": 35.0 + 5.0*A,
        "pH": 7.0 + B,
        "glucose_g_L": 10.0 + 5.0*C
    }
print("Biomass optimum:")
print(decode_conditions(x_constrained))
print("\nMulti-response optimum:")
print(decode_conditions(x_multi))
