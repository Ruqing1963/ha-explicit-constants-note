#!/usr/bin/env python3
"""Figure 1 of the note (needs matplotlib)."""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
FIGS = os.path.join(HERE, "..", "figures")
BLUE, ORANGE = "#2a78d6", "#eb6834"
INK, INK2, GRID = "#0b0b0b", "#52514e", "#dddcd6"


def style(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(INK2)
        ax.spines[s].set_linewidth(0.6)
    ax.tick_params(colors=INK2, labelsize=8, width=0.6, length=3)
    ax.grid(axis="y", color=GRID, linewidth=0.6)
    ax.set_axisbelow(True)


def fig3():
    from verify_ha_audit import ha_printed, restored, exact_criterion, prime_powers
    fig, axes = plt.subplots(1, 2, figsize=(6.3, 2.9))
    ax = axes[0]
    style(ax)
    qs = [q for q in prime_powers(64) if q >= 4]
    ax.plot(qs, [ha_printed(q, 1 / 4, 1)[6] for q in qs], color=ORANGE, marker="o", markersize=4,
            linewidth=1.6, markeredgecolor="white", markeredgewidth=0.6, label="printed constants")
    ax.plot(qs, [restored(q, 1 / 4, 4, 1) for q in qs], color=BLUE, marker="s", markersize=4,
            linewidth=1.6, markeredgecolor="white", markeredgewidth=0.6, label="Proposition 4.1")
    ax.axhline(1, color=INK, linewidth=0.8)
    ax.plot([16], [0.994], marker="x", color=INK, markersize=7, linestyle="none")
    ax.annotate("value stated\nby Ha", (16, 0.994), xytext=(4.3, 0.35), fontsize=7.5, color=INK,
                arrowprops=dict(arrowstyle="-", color=INK2, linewidth=0.6))
    ax.axvline(16, color=INK2, linewidth=0.6, linestyle=(0, (1, 2)))
    ax.set_ylim(0, 3.2)
    ax.set_xscale("log", base=2)
    ax.set_xticks([4, 8, 16, 32, 64])
    ax.set_xticklabels(["4", "8", "16", "32", "64"])
    ax.set_xlabel(r"$q$", fontsize=9, color=INK)
    ax.set_ylabel("left side of the criterion", fontsize=9, color=INK)
    ax.set_title(r"$\rho=1/4$, $B=1$", fontsize=8.5, color=INK)
    ax.legend(fontsize=7.5, frameon=False, loc="upper right", labelcolor=INK)
    ax = axes[1]
    style(ax)
    ns = list(range(30, 201))
    for q, m, col, lab, ls in ((2, 10, ORANGE, r"$q=2$, $r=\lfloor n/10\rfloor$", "-"),
                               (5, 5, BLUE, r"$q=5$, $r=\lfloor n/5\rfloor$", "-")):
        ys = [min(exact_criterion(q, n, n // m), 10) for n in ns]
        ax.plot(ns, ys, color=col, linewidth=1.4, label=lab, linestyle=ls)
    ax.axhline(1, color=INK, linewidth=0.8)
    for x, lab in ((52, "52"), (97, "97")):
        ax.axvline(x, color=INK2, linewidth=0.6, linestyle=(0, (1, 2)))
    ax.set_ylim(0, 3.2)
    ax.set_xlabel(r"$n$", fontsize=9, color=INK)
    ax.set_title(r"criterion (4.1)", fontsize=8.5, color=INK)
    ax.set_xticks([52, 97, 150, 200])
    ax.legend(fontsize=7.5, frameon=False, loc="upper right", labelcolor=INK)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGS, "fig_ha.pdf"))
    plt.close(fig)


if __name__ == "__main__":
    os.makedirs(FIGS, exist_ok=True)
    sys.path.insert(0, HERE)
    fig3()
