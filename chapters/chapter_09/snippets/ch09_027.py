# Chapter: 9
# Section: 9.8.9 Python을 이용한 RSM Design Matrix 생성
# Type: SNIPPET
# Status: SNIPPET_UNTESTED
# Origin: Word paragraph(s) 3128–3128
# Note: Independent execution NOT guaranteed. Original text preserved below.

def decode_design(df):
    result = df.copy()
    result["temperature_C"] = (
        35.0 + 5.0 * result["A"]
    )
    result["pH_actual"] = (
        7.0 + result["B"]
    )
    result["glucose_g_L"] = (
        10.0 + 5.0 * result["C"]
    )
    return result
ccd_actual = decode_design(ccd)
bbd_actual = decode_design(bbd)
print("CCD actual conditions:")
print(
    ccd_actual[
        ["temperature_C", "pH_actual", "glucose_g_L"]
    ])
print("\nBBD actual conditions:")
print(
    bbd_actual[
        ["temperature_C", "pH_actual", "glucose_g_L"]
    ])
