# A note on the explicit theorem of Ha on irreducible polynomials with prescribed coefficients

Ruqing Chen (2026). DOI: [10.5281/zenodo.24269019](https://doi.org/10.5281/zenodo.24269019). Split off from the paper in
[short-intervals-char2](https://github.com/Ruqing1963/short-intervals-char2).

J. Ha (Finite Fields Appl. 40 (2016), 10–25) gives three explicit ranges of `(q, n, r)` in which an irreducible
polynomial of degree `n` over `F_q` with `r` prescribed coefficients exists. This note recomputes the constants.

* With the formulas as printed, the sufficient condition fails at `(q, rho, B) = (16, 1/4, 1)` and `(5, 1/5, 2)`
  (right-hand side 1.3004 and 1.0121, not 0.994 and 0.884).
* Three steps need repair: inequality (13), `J` versus `1/rho`, and denominators divisible by `T`.
* A corrected criterion recovers the first two assertions (the second already for `n >= 66`) and the third for
  `q >= 3`; for `q = 2` only `n = 52, 53, 60` remain open.

The statements are conditional on Lemmas 2.3 and 2.8 of Ha's paper as printed.

| path | content |
|---|---|
| `ha_explicit_constants_note.tex`, `.pdf` | the note (6 pages, 4 figures) |
| `code/verify_ha_audit.py` | pure-Python recomputation of all tables (a few seconds) |
| `code/make_figure.py` | Figures 2-4 (matplotlib, numpy); Figure 1 is TikZ in the source |
| `figures/fig_q.pdf`, `fig_n.pdf`, `fig_region.pdf` | the condition against `q`; criterion (4.1) against `n`; criterion (4.1) in the `(n, r)` plane |
| `data/verify_ha_audit.txt` | output of the script |

## License

* The code in `code/` is released under the MIT License, see [`LICENSE`](LICENSE).
* The note (`ha_explicit_constants_note.tex`, `.pdf`), the figures in `figures/` and the output in `data/` are
  licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), see
  [`LICENSE-CC-BY-4.0.txt`](LICENSE-CC-BY-4.0.txt).

Copyright (c) 2026 Ruqing Chen.
