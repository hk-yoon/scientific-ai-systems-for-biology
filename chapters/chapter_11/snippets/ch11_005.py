# Chapter: 11
# Section: 11.10.2 기본 Agent와 도구 인터페이스
# Type: SNIPPET
# Status: SNIPPET_UNTESTED
# Origin: Word paragraph(s) 2668–2668
# Note: Independent execution NOT guaranteed. Original text preserved below.

import statistics

def summarize_measurements(values, unit="relative"):
    return {
        "mean": statistics.mean(values),
        "sample_std": statistics.stdev(values),
        "count": len(values),
        "unit": unit,
    }
