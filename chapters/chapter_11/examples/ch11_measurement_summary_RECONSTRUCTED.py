"""Chapter 11: formatting-only reconstruction from surviving original code text."""
from statistics import mean, stdev

def summarize_measurements(values: list[float]) -> dict:
    """반복 측정값의 평균과 표본 표준편차를 계산한다."""
    if len(values) < 2:
        raise ValueError("적어도 두 개의 관측값이 필요합니다.")
    return {"count": len(values), "mean": mean(values), "sample_std": stdev(values)}

if __name__ == "__main__":
    result = summarize_measurements([1.0, 2.0, 3.0])
    assert result["count"] == 3 and result["mean"] == 2.0 and result["sample_std"] == 1.0
    print(result)
