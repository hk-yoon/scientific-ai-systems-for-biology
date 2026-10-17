# Chapter: 9
# Section: 9.8.9 Python을 이용한 RSM Design Matrix 생성
# Type: SNIPPET
# Status: SNIPPET_UNTESTED
# Origin: Word paragraph(s) 3139–3139
# Note: Independent execution NOT guaranteed. Original text preserved below.

rng = np.random.default_rng(42)
def randomize_runs(df, rng):
    order = rng.permutation(len(df))
    result = (
        df.iloc[order]
        .reset_index(drop=True)
        .copy()
    )
    result.insert(
        0,
        "execution_order",
        np.arange(1, len(result) + 1)
    )
    return result
ccd_run_plan = randomize_runs(
    ccd_actual, rng)
bbd_run_plan = randomize_runs(
    bbd_actual, rng)
print("CCD randomized run plan:")
print(ccd_run_plan)
print("\nBBD randomized run plan:")
print(bbd_run_plan)
