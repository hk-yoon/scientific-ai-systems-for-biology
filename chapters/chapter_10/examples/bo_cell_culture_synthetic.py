"""Synthetic cell-culture condition optimization, educational BO example."""
from pathlib import Path
import csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.stats import norm
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import ConstantKernel, Matern

SEED = 2026
NOISE_SD = 0.05
BO_STEPS = 12
BOUNDS = np.array([[32.0, 38.0], [1.0, 4.0]])
RESULTS = Path(__file__).resolve().parent / 'results'
RESULTS.mkdir(exist_ok=True)


def encode(x):
    """Map temperature (deg C) and feed (g/L) to [0, 1]^2."""
    x = np.asarray(x, dtype=float)
    return (x - BOUNDS[:, 0]) / (BOUNDS[:, 1] - BOUNDS[:, 0])


def decode(z):
    z = np.asarray(z, dtype=float)
    return BOUNDS[:, 0] + z * (BOUNDS[:, 1] - BOUNDS[:, 0])


def latent_yield(x):
    """Simulated protein yield in arbitrary units; NOT a validated biological model."""
    x = np.asarray(x, dtype=float)
    t, c = x[..., 0], x[..., 1]
    peak = np.exp(-0.5 * ((t - 35.4) / 1.05)**2 - 0.5 * ((c - 2.85) / 0.62)**2)
    return 0.35 + 1.12 * peak + 0.10 * np.sin((t - 32.0) * 1.15) * np.cos(c * 1.6)


def observe(x, rng):
    return latent_yield(x) + rng.normal(0.0, NOISE_SD, size=np.asarray(x).shape[:-1])


def make_gp():
    kernel = ConstantKernel(1.0, (0.05, 10.0)) * Matern(length_scale=[0.35, 0.35], length_scale_bounds=(0.08, 3.0), nu=2.5)
    return GaussianProcessRegressor(kernel=kernel, alpha=NOISE_SD**2, normalize_y=False,
                                    n_restarts_optimizer=2, random_state=SEED)


def expected_improvement(mu, sd, incumbent):
    """Educational plug-in EI using posterior mean incumbent; not NEI."""
    sd = np.asarray(sd)
    improvement = np.asarray(mu) - incumbent
    z = np.divide(improvement, sd, out=np.zeros_like(improvement), where=sd > 1e-12)
    return np.where(sd > 1e-12, improvement * norm.cdf(z) + sd * norm.pdf(z),
                    np.maximum(improvement, 0.0))


def run(seed=SEED, steps=BO_STEPS):
    rng = np.random.default_rng(seed)
    # Predefined initial space-covering candidate design, physically admissible.
    initial_z = np.array([[0.08, 0.12], [0.15, 0.85], [0.48, 0.52],
                          [0.82, 0.18], [0.91, 0.89], [0.65, 0.68]])
    initial_x = decode(initial_z)
    x_obs = initial_x.copy()
    y_obs = observe(initial_x, rng)
    rows = []
    for i, (x, y) in enumerate(zip(initial_x, y_obs), start=1):
        rows.append([0, i, float(x[0]), float(x[1]), float(y), float('nan'), 'initial'])
    grid = np.stack(np.meshgrid(np.linspace(0, 1, 51), np.linspace(0, 1, 51), indexing='ij'), -1).reshape(-1, 2)
    for step in range(1, steps + 1):
        gp = make_gp()
        gp.fit(encode(x_obs), y_obs)
        mu, sd = gp.predict(grid, return_std=True)
        # Posterior-mean incumbent avoids uncritically treating noisy record as truth.
        incumbent = float(np.max(gp.predict(encode(x_obs))))
        ei = expected_improvement(mu, sd, incumbent)
        # Exclude almost identical points; exact repeats are not forbidden generally.
        distances = np.sqrt(((grid[:, None, :] - encode(x_obs)[None, :, :])**2).sum(axis=2))
        ei[np.min(distances, axis=1) < 0.025] = -np.inf
        next_z = grid[int(np.argmax(ei))]
        next_x = decode(next_z)
        next_y = float(observe(next_x[None, :], rng)[0])
        x_obs = np.vstack([x_obs, next_x])
        y_obs = np.append(y_obs, next_y)
        rows.append([step, len(y_obs), float(next_x[0]), float(next_x[1]), next_y,
                     float(np.max(ei)), 'BO'])
    final_gp = make_gp()
    final_gp.fit(encode(x_obs), y_obs)
    surface_mean, surface_sd = final_gp.predict(grid, return_std=True)
    recommended_z = grid[int(np.argmax(surface_mean))]
    recommended_x = decode(recommended_z)
    # Independent confirmation: new random draws; not training observations.
    confirmation = observe(np.repeat(recommended_x[None, :], 5, axis=0), rng)
    with (RESULTS / 'history.csv').open('w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['bo_step', 'measurement_id', 'temp_C', 'nutrient_g_L', 'observed_yield', 'acquisition_EI', 'phase'])
        writer.writerows(rows)
    with (RESULTS / 'confirmation.csv').open('w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['replicate', 'temp_C', 'nutrient_g_L', 'observed_yield'])
        for i, y in enumerate(confirmation, start=1):
            writer.writerow([i, recommended_x[0], recommended_x[1], y])
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.contourf(np.linspace(32, 38, 51), np.linspace(1, 4, 51), surface_mean.reshape(51, 51).T, levels=18)
    ax.scatter(x_obs[:6, 0], x_obs[:6, 1], marker='s', edgecolors='black', facecolors='white', label='Initial DOE')
    ax.scatter(x_obs[6:, 0], x_obs[6:, 1], marker='o', c='black', s=22, label='BO')
    ax.scatter([recommended_x[0]], [recommended_x[1]], marker='*', s=130, label='Recommended')
    ax.set(xlabel='Temperature (C)', ylabel='Nutrient (g/L)', title='GP predicted mean (synthetic)')
    ax.legend(loc='best', fontsize=8)
    fig.tight_layout()
    fig.savefig(RESULTS / 'gp_surface.png', dpi=160)
    plt.close(fig)
    summary = (f'initial={len(initial_x)} bo_steps={steps} n={len(y_obs)}\n'
               f'best_observed={np.max(y_obs):.6f}\n'
               f'recommend_temp={recommended_x[0]:.3f}\n'
               f'recommend_nutrient={recommended_x[1]:.3f}\n'
               f'confirmation_mean={np.mean(confirmation):.6f}\n'
               f'confirmation_sd={np.std(confirmation, ddof=1):.6f}\n')
    (RESULTS / 'summary.txt').write_text(summary, encoding='utf-8')
    return summary


if __name__ == '__main__':
    print(run())
