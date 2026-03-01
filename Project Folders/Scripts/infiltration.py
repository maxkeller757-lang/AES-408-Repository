"""Simple script to compute and plot Green-Ampt infiltration behaviour.

Parameters are hard-coded based on the homework problem, but can be
modified or turned into command-line arguments if desired.

Usage:
    python infiltration.py

The script calculates the ponding volume (F_p) and time to ponding (t_p),
and then produces a plot of infiltration rate f versus cumulative
infiltration volume F.  The figure is shown interactively and also saved
as ``infiltration.png`` in the current working directory.
"""

import numpy as np
import matplotlib.pyplot as plt


def compute_infiltration(Ks, theta_s, theta_i, psi, rain_intensity,
                         F_max=1.0, n_points=500):
    """Return (F, f, F_p, t_p) arrays/values.

    The infiltration rate is taken as the rainfall intensity until ponding
    occurs so that the f(F) curve is continuous at F_p.  Once the wetting
    front has formed the Green–Ampt expression is used.  For the homework
    values the rain intensity happens to exceed K_s, hence the pre-ponding
    rate (i) will be larger than K_s and dominate the early portion of the
    plot.

    Parameters
    ----------
    Ks : float
        Saturated hydraulic conductivity (in/hr).
    theta_s : float
        Saturated volumetric water content.
    theta_i : float
        Initial volumetric water content.
    psi : float
        Suction head at wetting front (in, should be negative).
    rain_intensity : float
        Rainfall intensity (in/hr).
    F_max : float, optional
        Maximum infiltration volume to compute (inches).
    n_points : int, optional
        Number of points used to sample the F axis.
    """
    delta_theta = theta_s - theta_i
    # ponding volume equation rearranged from f(t) formula
    F_p = (delta_theta * psi) / (1 - rain_intensity / Ks)
    t_p = F_p / Ks

    # build F array and compute f; use rain_intensity until F_p for continuity
    F = np.linspace(0, F_max, n_points)
    f = np.zeros_like(F)
    for idx, Fi in enumerate(F):
        if Fi <= F_p:
            f[idx] = rain_intensity
        else:
            f[idx] = Ks * (1 - (delta_theta * psi) / Fi)
    return F, f, F_p, t_p


def plot_infiltration(F, f, F_p, Ks, rain_intensity=None):
    """Generate the figure and save it to a file.  The plot is also shown.

    If ``rain_intensity`` is provided, a horizontal line is drawn so that the
    reader can see the constant pre-ponding rate explicitly.
    """
    plt.figure(figsize=(6, 4))
    plt.plot(F, f, label="Infiltration rate")
    plt.axvline(F_p, color="red", linestyle="--", label="F_p (ponding)")
    plt.axhline(Ks, color="green", linestyle=":", label="K_s")
    if rain_intensity is not None:
        plt.axhline(rain_intensity, color="orange", linestyle="-.",
                    label="rain intensity")
    plt.xlabel("Infiltration volume F (in)")
    plt.ylabel("Infiltration rate f (in/hr)")
    plt.title("Infiltration rate vs. volume")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    output_name = "infiltration.png"
    plt.savefig(output_name, dpi=150)
    print(f"Plot saved to {output_name}")
    plt.show()


if __name__ == "__main__":
    # problem parameters
    Ks = 0.53  # in/hr
    theta_s = 0.518
    theta_i = 0.215
    psi = -9.37  # in
    rain_intensity = 6.5  # in/hr

    F, f, F_p, t_p = compute_infiltration(Ks, theta_s, theta_i, psi,
                                          rain_intensity)
    print(f"Delta theta: {theta_s - theta_i:.3f}")
    print(f"Ponding volume F_p: {F_p:.3f} in")
    print(f"Time to ponding t_p: {t_p:.3f} hr ({t_p*60:.1f} min)")

    plot_infiltration(F, f, F_p, Ks, rain_intensity=rain_intensity)
