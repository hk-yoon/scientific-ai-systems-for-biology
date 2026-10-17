"""Chapter 8: source-grounded reconstruction with explicit illustrative data.
The growth_model and simulate definitions are taken from intact manuscript text.
Synthetic data / noise / fitting setup below are editorial additions, not recovered.
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import least_squares

def growth_model(t, state, mu_max, Ks, Y):
    X, S = state
    S = max(S, 0.0)
    mu = mu_max * S / (Ks + S)
    return [mu * X, -(1.0 / Y) * mu * X]

def simulate(params, t_eval, initial_state, Y=0.5):
    mu_max, Ks = params
    sol = solve_ivp(growth_model, (float(t_eval[0]), float(t_eval[-1])),
        initial_state, t_eval=t_eval, args=(mu_max, Ks, Y),
        rtol=1e-8, atol=1e-10)
    if not sol.success:
        raise RuntimeError(sol.message)
    return sol.y.T

# Editorial additions: illustrative parameters and reproducible synthetic observations.
t = np.linspace(0.0, 4.0, 9)
initial_state = [0.1, 5.0]
true_params = [0.5, 1.5]
rng = np.random.default_rng(20261016)
obs = simulate(true_params, t, initial_state) + rng.normal(0, 0.001, (len(t), 2))
def residual(params):
    return (simulate(params, t, initial_state) - obs).ravel()
fit = least_squares(residual, x0=[0.4, 1.0], bounds=([0.01, 0.01], [2.0, 10.0]))
print(f'mu_max={fit.x[0]:.6f}, Ks={fit.x[1]:.6f}, RMSE={np.sqrt(np.mean(fit.fun**2)):.6f}')
assert fit.success and np.all(np.isfinite(fit.x))
