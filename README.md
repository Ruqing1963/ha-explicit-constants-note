# A note on the explicit theorem of Ha on irreducible polynomials with prescribed coefficients

Ruqing Chen (2026). Split off from the paper in
[short-intervals-char2](https://github.com/Ruqing1963/short-intervals-char2).

J. Ha (Finite Fields Appl. 40 (2016), 10–25) gives three explicit ranges of `(q, n, r)` in which an irreducible
polynomial of degree `n` over `F_q` with `r` prescribed coefficients exists. This note recomputes the constants.

* With the formulas as printed, the sufficient condition fails at `(q, rho, B) = (16, 1/4, 1)` and `(5, 1/5, 2)`
  (right-hand side 1.3004 and 1.0121, not 0.994 and 0.884).
* Three steps need repair: inequality (13), `J` versus `1/rho`, and denominators divisible by `T`.
* A corrected criterion recovers the first two assertions (the second already for `n >= 71`) and the third for
  `q >= 3`; for `q = 2` it needs `n >= 81` instead of `n >= 52`.

The statements are conditional on Lemmas 2.3 and 2.8 of Ha's paper as printed.

| path | content |
|---|---|
| `ha_explicit_constants_note.tex`, `.pdf` | the note (5 pages) |
| `code/verify_ha_audit.py` | pure-Python recomputation of all tables (a few seconds) |
| `code/make_figure.py` | the figure (matplotlib) |
| `data/verify_ha_audit.txt` | output of the script |
