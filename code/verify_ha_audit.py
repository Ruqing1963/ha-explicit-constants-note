#!/usr/bin/env python3
"""
verify_ha_audit.py -- pure-Python recomputation for

    "A note on the explicit theorem of Ha on irreducible polynomials
     with prescribed coefficients"

Usage:  python verify_ha_audit.py      (a few seconds)
Output is also written to ../data/verify_ha_audit.txt.

Table 1: the constants of Ha (2016), Sections 3-4, as printed.
Table 2: the corrected criterion (Proposition 4.1).
Table 3 / Theorem 1.1(c): the scan of criterion (4.1).
"""
import math
import os
import sys

OUT = []
FAIL = []


def say(s=""):
    print(s, flush=True)
    OUT.append(s)


def check(cond, label):
    if not cond:
        FAIL.append(label)
    return "ok" if cond else "FAIL"


EG = math.exp(0.5772156649015329)
E1 = math.e


def ha_printed(q, rho, B):
    """Constants exactly as printed in Ha (2016), Sections 3-4, with the
    worst case C_1 = 2/(1+rho) and J = 1/rho."""
    C1 = 2 / (1 + rho)
    C2 = 1 - 2 * C1 * rho
    Cq2 = q ** C2 / (q ** C2 - 1)
    C3 = Cq2 * (E1 + EG + EG / (q * math.log(q)))
    J = 1 / rho
    br2 = EG * Cq2 * (math.log(1 / rho, q) + 1 + 1 / (J * math.log(q)))
    C8 = q / (q - 1) * max(C3, br2)
    rhs = C8 / q ** (C2 / rho) + q ** (-B)
    return C1, C2, Cq2, C3, br2, C8, rhs

def weight(q, j):
    return E1 if j <= q else EG * (math.log(j, q) + 1)

def restored(q, rho, J, B, n_min=8):
    """Left side of the criterion of Proposition 4.1:
    C_(q) * sum_{j >= J} w_q(j) q^(-c2 j) + q^(-B)/(1 - 2 q^(-n_min/2))."""
    c2 = (1 - 3 * rho) / (1 + rho)
    s, j = 0.0, J
    while True:
        term = weight(q, j) * q ** (-c2 * j)
        s += term
        j += 1
        if term < 1e-16 and j > q + 5:
            break
        if j > 200000:
            break
    return q / (q - 1) * s + q ** (-B) / (1 - 2 * q ** (-n_min / 2))

def series(q, rho, J):
    c2 = (1 - 3 * rho) / (1 + rho)
    s, j = 0.0, J
    while j < 200000:
        term = weight(q, j) * q ** (-c2 * j)
        s += term
        j += 1
        if term < 1e-16 and j > q + 5:
            break
    return s

def exact_criterion(q, n, r):
    """Left side of (4.1)."""
    J = -(-n // (r + 1))
    Js = -(-n // (r + 2))
    if 3 * (r + 1) >= n:
        return float('inf')
    return (series(q, r / n, J) + series(q, (r + 1) / n, Js) / (q - 1)
            + n * q ** (r - n / 4) / (1 - 2 * q ** (-n / 2)))

def prime_powers(limit):
    out = []
    for m in range(2, limit + 1):
        p = next(d for d in range(2, m + 1) if m % d == 0)
        x = m
        while x % p == 0:
            x //= p
        if x == 1:
            out.append(m)
    return out

def section_F():
    say("=" * 76)
    say("Audit of the constants in Ha (2016), Sections 3-4")
    say("=" * 76)
    say("  e^gamma = %.6f" % EG)
    say("  Table 1: constants as printed, at the boundary parameters")
    say(f"  {'q':>3} {'rho':>5} {'B':>2} {'C1':>7} {'C2':>7} {'C_(q^C2)':>9} {'C3':>8} "
        f"{'C4log+C5':>9} {'C8':>8} {'C8[Ha]':>8} {'RHS':>7} {'RHS[Ha]':>8}")
    for q, rho, B, c8ha, rhsha in ((16, 1 / 4, 1, 8.552, 0.994),
                                   (5, 1 / 5, 2, 12.335, 0.884),
                                   (2, 1 / 10, 2, 42.342, 0.764)):
        C1, C2, Cq2, C3, br2, C8, rhs = ha_printed(q, rho, B)
        say(f"  {q:>3} {rho:>5.3f} {B:>2} {C1:>7.4f} {C2:>7.4f} {Cq2:>9.4f} {C3:>8.4f} "
            f"{br2:>9.4f} {C8:>8.4f} {c8ha:>8.3f} {rhs:>7.4f} {rhsha:>8.3f}")
    say("  smallest prime power q with printed RHS < 1 (and for all larger q <= 4096):")
    pps = prime_powers(4096)
    for rho, B in ((1 / 4, 1), (1 / 5, 2), (1 / 10, 2)):
        good = [q for q in pps if ha_printed(q, rho, B)[6] < 1]
        bad = [q for q in pps if q not in good]
        q0 = min(q for q in good if all(x in good for x in pps if x >= q))
        say(f"    rho = 1/{round(1/rho)}, B = {B}: q0 = {q0}   (fails for q in {bad})")
    say()
    say("  Table 2: corrected criterion (Proposition 4.1),")
    say("  Xi = C_(q) * sum_{j>=J} w_q(j) q^(-c2(rho) j) + q^(-B)/(1-2q^(-4)) < 1")
    say(f"  {'rho*':>6} {'J*':>3} | {'q0 (B=1)':>9} {'Xi(q0)':>8} | {'q0 (B=2)':>9} {'Xi(q0)':>8} |"
        f" {'Xi(q=16,B=1)':>13}")
    for m in (4, 5, 6, 8, 10):
        rho = 1 / m
        row = f"  {'1/'+str(m):>6} {m:>3} |"
        for B in (1, 2):
            good = [q for q in pps if restored(q, rho, m, B) < 1]
            q0 = min(q for q in good if all(x in good for x in pps if x >= q))
            row += f" {q0:>9} {restored(q0, rho, m, B):>8.4f} |"
        row += f" {restored(16, rho, m, 1):>13.4f}"
        say(row)
    say("  Table 3 / Theorem 1.1(c): the criterion (4.1),")
    say("    S(r/n, J) + S((r+1)/n, J*)/(q-1) + n q^(r-n/4)/(1-2q^(-n/2)) < 1,")
    say("  for the three families of Ha's Theorem 1.3 (n scanned up to 3000):")
    fams = (("q=16, r=floor(n/4-log_q n-1)", 16, lambda n: math.floor(n / 4 - math.log(n, 16) - 1), 8),
            ("q=5,  r=floor(n/5)", 5, lambda n: n // 5, 97),
            ("q=7,  r=floor(n/5)", 7, lambda n: n // 5, 97),
            ("q=2,  r=floor(n/10)", 2, lambda n: n // 10, 52),
            ("q=3,  r=floor(n/10)", 3, lambda n: n // 10, 52),
            ("q=4,  r=floor(n/10)", 4, lambda n: n // 10, 52))
    for lab, q, rfun, nha in fams:
        vals = {}
        for n in range(8, 3001):
            r = rfun(n)
            if r < 1:
                continue
            vals[n] = exact_criterion(q, n, r)
        bad = [n for n, v in vals.items() if v >= 1]
        n0 = (max(bad) + 1) if bad else min(vals)
        at = vals.get(nha, float('nan'))
        say(f"    {lab:<30} holds for all n >= {n0:>4} (value at Ha's n = {nha}: {at:.4f}; "
            f"value at n0: {vals[n0]:.4f})")
    say("  tail n > 3000 (rho <= 1/m, rho* <= 1/m + 1/3000, J, J* >= m):")
    for q, m in ((5, 5), (2, 10), (3, 10)):
        v = (series(q, 1 / m, m) + series(q, 1 / m + 1 / 3000, m) / (q - 1)
             + 3000 * q ** (-3000 * (1 / 4 - 1 / m)) )
        say(f"    q = {q}, m = {m}: bound {v:.4f}  {check(v < 1, f'tail q={q} m={m}')}")
    say("  largest rho* = 1/m (J* = m) for which the criterion holds, B = 1:")
    for q in (2, 3, 4, 5, 7, 8, 9, 16):
        ms = [m for m in range(4, 400) if restored(q, 1 / m, m, 1) < 1]
        m0 = min(m for m in ms if all(x in ms for x in range(m, 400))) if ms else None
        say(f"    q = {q:>2}: m >= {m0}" if m0 else f"    q = {q:>2}: none (q^(-B) term)")
    say()


def main():
    section_F()
    say("ALL CHECKS PASSED" if not FAIL else "FAILED CHECKS: " + ", ".join(FAIL))
    here = os.path.dirname(os.path.abspath(__file__))
    data = os.path.join(here, "..", "data")
    os.makedirs(data, exist_ok=True)
    with open(os.path.join(data, "verify_ha_audit.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(OUT) + "\n")
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
