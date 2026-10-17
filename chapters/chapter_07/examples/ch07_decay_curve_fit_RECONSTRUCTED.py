"""Chapter 7: source-grounded reconstruction of the truncated curve_fit example.
Reconstructed from original manuscript context, not recovered original source.
Requires numpy/scipy; matplotlib is not necessary for numerical execution.
"""
import numpy as np
from scipy.optimize import curve_fit

time = np.array([0, 1, 2, 3, 4, 5], dtype=float)
C_obs = np.array([10.0, 8.3, 6.8, 5.6, 4.5, 3.7])
def decay_solution(t, k, C0):
    return C0 * np.exp(-k * t)
params, covariance = curve_fit(decay_solution, time, C_obs, p0=[0.2, 10.0])
k_est, C0_est = params
rmse = float(np.sqrt(np.mean((decay_solution(time, *params) - C_obs)**2)))
print(f'k={k_est:.6f}, C0={C0_est:.6f}, RMSE={rmse:.6f}')
assert k_est > 0 and C0_est > 0 and np.isfinite(rmse)
