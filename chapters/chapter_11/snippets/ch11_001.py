# Chapter: 11
# Section: 11.4.1 도구 호출과 함수 실행
# Type: SNIPPET
# Status: SNIPPET_UNTESTED
# Origin: Word paragraph(s) 669–669
# Note: Independent execution NOT guaranteed. Original text preserved below.

from statistics import mean, stdev

def summarize_measurements(values: list[float]) -> dict:
    """반복 측정값의 평균과 표본 표준편차를 계산한다."""
    if len(values) < 2:
        raise ValueError("적어도 두 개의 관측값이 필요합니다.")
    return {
        "count": len(values),
        "mean": mean(values),
        "sample_std": stdev(values),
    }
