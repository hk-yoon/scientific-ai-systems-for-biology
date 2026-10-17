"""Chapter 10.10: reproducible, CPU-only 1D Bayesian optimization lab.
Run: python bo_sequential.py
Requires: numpy, scipy, scikit-learn, matplotlib
The objective is SYNTHETIC, not a biological experiment.
"""
from pathlib import Path
import csv
import numpy as np
from scipy.stats import norm
from scipy.optimize import minimize_scalar
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import ConstantKernel, Matern
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

SEED = 2026
LOWER, UPPER = 0.0, 1.0
INITIAL_X = np.array([0.05, 0.25, 0.50, 0.75, 0.95])
NOISE_SD = 0.08
BO_STEPS = 12
N_CANDIDATES = 1001
OUTPUT_DIR = Path(__file__).resolve().parent / 'results'


def latent_response(x):
    """Synthetic smooth response (higher is better)."""
    x = np.asarray(x, dtype=float)
    return 0.9 * np.exp(-((x - 0.72) / 0.15) ** 2) + 0.25 * np.sin(8 * x) + 0.35


def observe(x, rng):
    """Return noisy observations; the latent function remains hidden from BO."""
    return latent_response(x) + rng.normal(0.0, NOISE_SD, size=np.asarray(x).shape)


def fit_gp(x, y):
    kernel = ConstantKernel(1.0, (0.1, 10.0)) * Matern(
        length_scale=0.2, length_scale_bounds=(0.03, 2.0), nu=2.5
    )
    gp = GaussianProcessRegressor(
        kernel=kernel, alpha=NOISE_SD**2,
        normalize_y=False, n_restarts_optimizer=2, random_state=SEED,
    )
    gp.fit(np.asarray(x).reshape(-1, 1), np.asarray(y))
    return gp


def acquisition_values(mu, sd, incumbent, xi=0.01, kappa=1.5):
    """Latent-function PI/EI/UCB. Incumbent is a GP posterior-mean proxy.
    In noisy BO, classical PI/EI with a plug-in incumbent is approximate,
    NOT noisy EI / an exact treatment of uncertainty in the incumbent.
    """
    sd = np.asarray(sd)
    mu = np.asarray(mu)
    gain = mu - incumbent - xi
    z = np.divide(gain, sd, out=np.zeros_like(gain), where=sd > 1e-12)
    pi = np.where(sd > 1e-12, norm.cdf(z), (gain > 0).astype(float))
    ei = np.where(sd > 1e-12, gain * norm.cdf(z) + sd * norm.pdf(z), np.maximum(gain, 0))
    ei = np.maximum(ei, 0.0)
    ucb = mu + kappa * sd
    return pi, ei, ucb


def propose(gp, observed_x, candidates, method='ei'):
    mu, sd = gp.predict(candidates.reshape(-1, 1), return_std=True)
    # We use the highest posterior mean among evaluated designs as a simple,
    # explicit plug-in incumbent, avoiding selection by noisy max observation.
    incumbent = float(np.max(gp.predict(np.asarray(observed_x).reshape(-1, 1))))
    pi, ei, ucb = acquisition_values(mu, sd, incumbent)
    acquisition = {'pi': pi, 'ei': ei, 'ucb': ucb}[method].copy()
    # No duplicate designs for this teaching lab. Replication is discussed separately.
    too_close = np.min(np.abs(candidates[:, None] - np.asarray(observed_x)[None, :]), axis=1) < 1e-4
    acquisition[too_close] = -np.inf
    index = int(np.argmax(acquisition))
    return float(candidates[index]), (mu, sd, pi, ei, ucb), float(acquisition[index])


def plot_state(gp, x, y, candidates, filename):
    mu, sd = gp.predict(candidates.reshape(-1, 1), return_std=True)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(candidates, latent_response(candidates), '--', label='latent synthetic function')
    ax.plot(candidates, mu, label='GP posterior mean')
    ax.fill_between(candidates, mu - 1.96 * sd, mu + 1.96 * sd, alpha=0.2,
                    label='approx. 95% latent credible band')
    ax.scatter(x, y, marker='o', label='noisy observations')
    ax.set(xlabel='coded experimental variable x', ylabel='response', title='BO surrogate model')
    ax.legend(loc='best', fontsize=8)
    fig.tight_layout()
    fig.savefig(filename, dpi=150)
    plt.close(fig)


def run_bo():
    rng = np.random.default_rng(SEED)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    candidates = np.linspace(LOWER, UPPER, N_CANDIDATES)
    x = INITIAL_X.copy()
    y = observe(x, rng)
    history = []
    for step in range(1, BO_STEPS + 1):
        gp = fit_gp(x, y)
        next_x, _, acq = propose(gp, x, candidates, method='ei')
        next_y = float(observe(np.array([next_x]), rng)[0])
        x = np.append(x, next_x)
        y = np.append(y, next_y)
        row = dict(step=step, x=next_x, observed_y=next_y,
                   best_observed=float(np.max(y)), acquisition=acq)
        history.append(row)
        print(f"step={step:02d}, x={next_x:.3f}, y={next_y:.3f}, best observed={np.max(y):.3f}")
    final_gp = fit_gp(x, y)
    mu, sd = final_gp.predict(candidates.reshape(-1, 1), return_std=True)
    best_idx = int(np.argmax(mu))
    recommended_x = float(candidates[best_idx])
    plot_state(final_gp, x, y, candidates, OUTPUT_DIR / 'gp_final.png')
    with (OUTPUT_DIR / 'history.csv').open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['step', 'x', 'observed_y', 'best_observed', 'acquisition'])
        writer.writeheader()
        writer.writerows(history)
    print(f"recommended x (posterior mean): {recommended_x:.3f}")
    print(f"best observed y (noisy): {np.max(y):.3f}")
    print(f"outputs: {OUTPUT_DIR}")
    return history, recommended_x, x, y


if __name__ == '__main__':
    run_bo()
