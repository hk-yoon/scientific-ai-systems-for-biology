# Chapter: 9
# Section: 9.7 Python 실습 — 기본 반응표면 모델과 시각화
# Type: SNIPPET
# Status: SNIPPET_UNTESTED
# Origin: Word paragraph(s) 2531–2531
# Note: Independent execution NOT guaranteed. Original text preserved below.

def encode_temperature(T):
    return (T - 35.0) / 5.0

def encode_ph(pH):
    return (pH - 7.0) / 1.0

def decode_temperature(x1):
    return 35.0 + 5.0 * x1

def decode_ph(x2):
    return 7.0 + x2

T = 37.5
pH = 7.5
x1 = encode_temperature(T)
x2 = encode_ph(pH)
print("Coded values:", x1, x2)
print("Predicted response:", response_surface(x1, x2))
