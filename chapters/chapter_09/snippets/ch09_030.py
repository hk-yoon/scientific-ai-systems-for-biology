# Chapter: 9
# Section: 9.9 Python 실습 — CCD 데이터에서 반응표면 구축과 검증
# Type: SNIPPET
# Status: SNIPPET_UNTESTED
# Origin: Word paragraph(s) 3521–3521
# Note: Independent execution NOT guaranteed. Original text preserved below.

from scipy import stats

group_mean = data.groupby(
    "point_id")["response"].transform("mean")
SS_PE = np.sum(
    (data["response"] - group_mean)**2)
SSE = np.sum(model.resid**2)
SS_LOF = SSE - SS_PE
n = len(data)
m = data["point_id"].nunique()
p = len(model.params)
df_PE = n - m
df_LOF = m - p
MS_PE = SS_PE / df_PE
MS_LOF = SS_LOF / df_LOF
F_LOF = MS_LOF / MS_PE
p_LOF = stats.f.sf(
    F_LOF,
    df_LOF,
    df_PE)
print(f"Pure Error SS: {SS_PE:.5f}")
print(f"Lack-of-Fit SS: {SS_LOF:.5f}")
print(f"Pure Error df: {df_PE}")
print(f"Lack-of-Fit df: {df_LOF}")
print(f"Lack-of-Fit p-value: {p_LOF:.5f}")
