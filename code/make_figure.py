#!/usr/bin/env python3
"""Figures 2-4 of the note (needs matplotlib and numpy; Figure 1 is drawn in TikZ).

    fig_q.pdf       the condition as a function of q, printed constants against Proposition 4.1
    fig_n.pdf       criterion (4.1) as a function of n, and its two parts for q = 2
    fig_region.pdf  criterion (4.1) in the (n, r) plane
"""
import math
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

HERE = os.path.dirname(os.path.abspath(__file__))
FIGS = os.path.join(HERE, "..", "figures")
sys.path.insert(0, HERE)
from verify_ha_audit import ha_printed, restored, exact_criterion, series, prime_powers  # noqa: E402

BLUE, ORANGE = "#2a78d6", "#eb6834"
INK, INK2, MUTED, GRID = "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
FAIL_BG = "#fdf2ed"     # region where the condition fails (opaque: no transparency in the PDF)
# diverging map: blue (criterion holds) - neutral (value 1) - orange (criterion fails)
DIV = LinearSegmentedColormap.from_list(
    "div", ["#104281", "#2a78d6", "#9ec5f4", "#f0efec", "#f5b79c", "#eb6834", "#9c3a12"])

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["cmr10", "DejaVu Serif"],
    "mathtext.fontset": "cm",
    "axes.formatter.use_mathtext": True,
    "axes.unicode_minus": False,
    "font.size": 9,
    "pdf.fonttype": 42,
})


def style(ax, grid=True):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(INK2)
        ax.spines[s].set_linewidth(0.6)
    ax.tick_params(colors=INK2, labelsize=8, width=0.6, length=3)
    if grid:
        ax.grid(axis="y", color=GRID, linewidth=0.6)
    ax.set_axisbelow(True)


def save(fig, name):
    fig.savefig(os.path.join(FIGS, name), bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)


def fig_q():
    """Printed condition and Proposition 4.1 as functions of q, in the three cases of Table 1."""
    cases = ((4, 1, 16, 0.994), (5, 2, 5, 0.884), (10, 2, 2, 0.764))
    qs = prime_powers(64)
    fig, axes = plt.subplots(1, 3, figsize=(6.5, 2.45), sharey=True)
    top = 2.6
    for ax, (m, B, qha, stated) in zip(axes, cases):
        style(ax)
        ax.axhspan(1, top, facecolor=FAIL_BG, edgecolor="none", zorder=0)
        ax.axhline(1, color=INK, linewidth=0.8)
        ax.axvline(qha, color=MUTED, linewidth=0.6, linestyle=(0, (1, 2)))
        for f, col, mk, lab in ((lambda q: ha_printed(q, 1 / m, B)[6], ORANGE, "o", "printed constants"),
                                (lambda q: restored(q, 1 / m, m, B), BLUE, "s", "Proposition 4.1")):
            pts = [(q, f(q)) for q in qs]
            pts = [(q, v) for q, v in pts if v <= top * 1.6]
            ax.plot([p[0] for p in pts], [p[1] for p in pts], color=col, marker=mk, markersize=3.6,
                    linewidth=1.4, markeredgewidth=0, label=lab, clip_on=True)
        ax.plot([qha], [stated], marker="x", color=INK, markersize=6.5, markeredgewidth=1.2,
                linestyle="none", label="value stated in [1]", zorder=5)
        ax.set_ylim(0, top)
        ax.set_xscale("log", base=2)
        ax.set_xlim(1.75, 74)
        ax.set_xticks([2, 4, 8, 16, 32, 64])
        ax.set_xticklabels(["2", "4", "8", "16", "32", "64"])
        ax.minorticks_off()
        ax.set_xlabel(r"$q$", fontsize=9.5, color=INK)
        ax.set_title(rf"$\rho=1/{m}$, $B={B}$", fontsize=9.5, color=INK)
    axes[0].set_ylabel("quantity required to be $<1$", fontsize=9, color=INK)
    axes[0].text(1.9, 1.06, "condition fails", fontsize=7.5, color=INK2, va="bottom")
    axes[2].legend(fontsize=8, frameon=False, loc="upper right", labelcolor=INK, handlelength=1.6)
    fig.tight_layout(w_pad=0.8)
    save(fig, "fig_q.pdf")


def fig_n():
    """Criterion (4.1) as a function of n; right: its two parts for q = 2."""
    fig, axes = plt.subplots(1, 2, figsize=(6.5, 2.75), gridspec_kw=dict(width_ratios=[1, 1.15]))
    ax = axes[0]
    style(ax)
    top = 2.6
    ns = list(range(40, 201))
    ax.axhspan(1, top, facecolor=FAIL_BG, edgecolor="none", zorder=0)
    for q, m, col, lab in ((2, 10, ORANGE, r"$q=2$, $r=\lfloor n/10\rfloor$"),
                           (5, 5, BLUE, r"$q=5$, $r=\lfloor n/5\rfloor$")):
        ax.plot(ns, [min(exact_criterion(q, n, n // m), 10) for n in ns], color=col, linewidth=1.0, label=lab,
                solid_joinstyle="miter")
    ax.axhline(1, color=INK, linewidth=0.8)
    for x in (52, 97):
        ax.axvline(x, color=MUTED, linewidth=0.6, linestyle=(0, (1, 2)))
    ax.set_ylim(0, top)
    ax.set_xlim(40, 200)
    ax.set_xticks([52, 97, 150, 200])
    ax.set_xlabel(r"$n$", fontsize=9.5, color=INK)
    ax.set_ylabel("left side of (4.1)", fontsize=9, color=INK)
    ax.legend(fontsize=8, frameon=False, loc="upper right", labelcolor=INK, handlelength=1.6)

    ax = axes[1]
    style(ax)
    q, lo, hi, top = 2, 44, 80, 1.75
    ns = list(range(lo, hi + 1))
    sig, err = [], []
    for n in ns:
        r = n // 10
        sig.append(series(q, (r + 1) / n, -(-n // (r + 2))) / (q - 1))
        err.append(n * q ** (r - n / 4) / (1 - 2 * q ** (-n / 2)))
        assert abs(sig[-1] + err[-1] - exact_criterion(q, n, r)) < 1e-12
    ax.bar(ns, sig, width=0.72, color=BLUE, edgecolor="none", label=r"$\Sigma_2\,$ term")
    ax.bar(ns, err, width=0.72, bottom=[s + 0.012 for s in sig], color=ORANGE, edgecolor="none",
           label=r"$n\,2^{\,r-n/4}$ term")
    ax.axhline(1, color=INK, linewidth=0.8)
    for n, s, e in zip(ns, sig, err):
        if n >= 52 and s + e >= 1:
            ax.text(n, min(s + e, top) + 0.05, str(n), ha="center", va="bottom", fontsize=8, color=INK)
    for x in range(50, hi + 1, 10):
        ax.axvline(x - 0.5, color=MUTED, linewidth=0.6, linestyle=(0, (1, 2)))
    for x0 in range(40, hi + 1, 10):
        a, b = max(x0, lo), min(x0 + 9, hi)
        if b - a >= 3:
            ax.text((a + b) / 2, top * 0.985, rf"$r={x0 // 10}$", ha="center", va="top", fontsize=8, color=INK2)
    ax.set_ylim(0, top)
    ax.set_xlim(lo - 0.8, hi + 0.8)
    ax.set_xticks([50, 52, 60, 70, 80])
    ax.set_xlabel(r"$n$", fontsize=9.5, color=INK)
    ax.set_title(r"$q=2$, $r=\lfloor n/10\rfloor$", fontsize=9.5, color=INK)
    ax.legend(fontsize=8, frameon=False, loc="upper right", bbox_to_anchor=(1.0, 0.9), labelcolor=INK,
              handlelength=1.2)
    fig.tight_layout(w_pad=1.2)
    save(fig, "fig_n.pdf")


def staircase(ax, ns, rs, **kw):
    """Upper outline of the cells (n, r') with r' <= rs[n]."""
    xs, ys = [], []
    for n, r in zip(ns, rs):
        xs += [n - 0.5, n + 0.5]
        ys += [r + 0.5, r + 0.5]
    ax.plot(xs, ys, **kw)


def fig_region():
    """log2 of the left side of (4.1) over the (n, r) plane, for four values of q."""
    n0, n1, r1 = 8, 120, 34
    panels = ((2, r"$r\leq n/10$", lambda n, q: n // 10, 52),
              (3, r"$r\leq n/10$", lambda n, q: n // 10, 52),
              (5, r"$r\leq n/5$", lambda n, q: n // 5, 97),
              (16, r"$r\leq n/4-\log_q n-1$", lambda n, q: math.floor(n / 4 - math.log(n, q) - 1), 8))
    fig, axes = plt.subplots(2, 2, figsize=(6.5, 4.5), sharex=True, sharey=True)
    ns = list(range(n0, n1 + 1))
    im = None
    for ax, (q, lab, rfun, nha) in zip(axes.flat, panels):
        style(ax, grid=False)
        Z = np.full((r1, n1 - n0 + 1), np.nan)
        rmax = []
        for i, n in enumerate(ns):
            ok, mono = 0, True
            for r in range(1, r1 + 1):
                if 3 * (r + 1) >= n:
                    break
                v = exact_criterion(q, n, r)
                Z[r - 1, i] = math.log2(v) if v > 0 else -60
                if v < 1:
                    assert mono, (q, n, r)      # the left side of (4.1) is nondecreasing in r
                    ok = r
                else:
                    mono = False
            rmax.append(ok)
        ax.set_facecolor("white")
        im = ax.imshow(np.clip(Z, -4, 4), origin="lower", aspect="auto", cmap=DIV, vmin=-4, vmax=4,
                       extent=(n0 - 0.5, n1 + 0.5, 0.5, r1 + 0.5), interpolation="nearest")
        staircase(ax, ns, rmax, color=INK, linewidth=0.9)
        hn = [n for n in ns if n >= nha and rfun(n, q) >= 1]
        staircase(ax, hn, [rfun(n, q) for n in hn], color="white", linewidth=2.2)
        staircase(ax, hn, [rfun(n, q) for n in hn], color=INK, linewidth=1.0, linestyle=(0, (3, 1.6)))
        ax.text(0.03, 0.95, rf"$q={q}$", transform=ax.transAxes, ha="left", va="top", fontsize=10, color=INK)
        ax.text(0.03, 0.80, r"$3(r+1)\geq n$", transform=ax.transAxes, ha="left", va="top", fontsize=8,
                color=MUTED)
        ax.text(0.97, 0.05, lab, transform=ax.transAxes, ha="right", va="bottom", fontsize=8.5, color="white")
        ax.set_xlim(n0 - 0.5, n1 + 0.5)
        ax.set_ylim(0.5, r1 + 0.5)
        ax.set_xticks([20, 40, 60, 80, 100, 120])
        ax.set_yticks([1, 10, 20, 30])
    for ax in axes[1]:
        ax.set_xlabel(r"$n$", fontsize=9.5, color=INK)
    for ax in axes[:, 0]:
        ax.set_ylabel(r"$r$", fontsize=9.5, color=INK)
    fig.tight_layout(h_pad=0.6, w_pad=0.8)
    cb = fig.colorbar(im, ax=axes, fraction=0.03, pad=0.025, aspect=28)
    cb.set_ticks([-4, -2, 0, 2, 4])
    cb.set_ticklabels([r"$\leq 1/16$", r"$1/4$", r"$1$", r"$4$", r"$\geq 16$"])
    cb.ax.tick_params(colors=INK2, labelsize=8.5, width=0.6, length=3)
    cb.outline.set_visible(False)
    cb.set_label("left side of (4.1)", fontsize=9, color=INK)
    save(fig, "fig_region.pdf")


if __name__ == "__main__":
    os.makedirs(FIGS, exist_ok=True)
    fig_q()
    fig_n()
    fig_region()
