# Kannangara prior work and Stepping-Stone manuscript context

Research handoff prepared 2026-11-03. This is a literature review and preliminary consistency audit, **not** a journal decision or response to reviewers.

## Primary papers

- Kannangara, Tanin, Harwood, Karunasekera (2018), *Stepping Stone Graph for Public Movement Analysis*, ACM SIGSPATIAL, DOI [10.1145/3274895.3274913](https://doi.org/10.1145/3274895.3274913).
- The same authors (2019), *Stepping Stone Graph: A Graph for Finding Movement Corridors using Sparse Trajectories*, *ACM Transactions on Spatial Algorithms and Systems* 5(4), Article 23 (24 pages), DOI [10.1145/3324883](https://doi.org/10.1145/3324883).
- Espino-Montelongo and Maravillo (2026), *Geometry and Volume of Stepping-Stone Diversion Neighborhoods in Euclidean Spaces of Arbitrary Dimension*, 13-page PDF reviewed from conversation attachment, marked “Preprint submitted to Elsevier”.

## Mathematical definition and notation

Original Kannangara work treats **planar** locations and uses `d` as the diversion *exponent*, not as spatial dimension. Their closed diversion neighborhood is
```math
DN(p,q;\delta)=\{z\in\mathbb R^2:\|z-p\|^\delta+\|z-q\|^\delta\leq\|p-q\|^\delta\},\quad\delta\geq1.
```
An edge `pq` belongs to `SSG_δ(V)` iff the diversion neighborhood is empty of `V \ {p,q}`.

The new paper reserves `d≥2` for *ambient dimension* and `α≥1` for the exponent. Its normalized volume constant is
```math
a_{d,SS}(\alpha)=\lambda_d\{z\in\mathbb R^d:\|z\|^\alpha+\|z-e_1\|^\alpha\leq1\}.
```
Similarity factorization gives `Vol(S_SS,α(p,q))=||p-q||^d a_d,SS(α)`.

## Provenance: already established by Kannangara et al.

- Nested SSG edge sets as exponent increases (both papers, Theorem 3.3).
- Gabriel-graph equality at exponent 2; RNG limit as exponent tends to infinity (Theorems 3.4–3.5).
- **Planar** SSG planarity for exponent ≥2 and connectivity for exponent ≥1 (Lemmas 3.6–3.8).
- `SPG(t) ⊆ SSG(δ)` when `δ≤t` (Theorem 3.9).
- Relationships with β-skeletons and planar Delaunay containment (2018 Theorems 3.10–3.11; 2019 Theorems 3.10–3.12).
- The edge-deletion threshold or parameter spectrum (2019 Definition 3.13) already implies an eventual finite threshold for each fixed finite planar point set. Attribute this inspiration in any generalized result.
- Original algorithms use planar Delaunay candidates, edge-spectrum/deletion thresholds, Java 8, and a secant root solver. Delaunay containment alone does *not* guarantee linear-time graph construction.

The original sources contain two misleading phrasings: calling `x↦x^β` subadditive for `β≥1` (the intended inequality is justified using appropriate power/norm monotonicity) and saying that shortest-path distances both increase and decrease as the graph loses edges. Do not copy either phrase.

## New paper: contribution map by PDF page

- pp. 3–4, Proposition 1: arbitrary-dimensional normalized-region similarity and volume scaling.
- pp. 4–5, Proposition 3: explicit boundary parametrization.
- pp. 5–6, Theorem 1: one-dimensional integral for all `d≥2` and `α>1`.
- p. 6, Proposition 4: zero-volume segment at α=1 and exact Gabriel-ball constant `κ_d/2^d` at α=2.
- pp. 6–7, Proposition 5: union of finite-α neighborhoods excluding the defining sites equals the **open** RNG lune; limit volume `κ_d I_{3/4}((d+1)/2,1/2)`.
- p. 7, Theorem 2 and Corollary 1: **strict** geometric/volume monotonicity and continuous volume-to-parameter calibration.
- p. 8, Proposition 6 and Corollaries 3–4: inclusion chains, arbitrary-dimensional connectivity, and exact eventual RNG stabilization for each fixed finite point set (not uniformly over all point sets).
- p. 9, Proposition 7 and Corollary 5: specialization of Devroye (1988) regular-set expected-size results; these stochastic theorems themselves are earlier work. Conditional expected degree tends to `κ_d/a_d,SS(α)` at f-a.e. site; `liminf E[edges]/n≥κ_d/(2a)`.
- p. 9, Proposition 8: planar Watanabe-style **modeled** edge-length approximation, not an unconditional exact law of the graph's observed edge lengths.
- p. 10, Proposition 9: stable, endpoint-regularizing one-dimensional quadrature.

The manuscript's graph convention is **closed Gabriel ball, open RNG lune**. Preserve that distinction: equal-volume regions can produce different edges at boundary sites. Avoid any implication that Delaunay containment alone gives a subquadratic higher-dimensional algorithm; the manuscript correctly notes dimension-3 quadratic candidate-set cases.

## Evidence and numerical reproducibility

Paper-specific repository: [heri-espino/Stepping-Stone-Volume-Constants](https://github.com/heri-espino/Stepping-Stone-Volume-Constants).

- Two retained files: `results/paper_validation_dimensions_2_3_4_5_8.csv` and `results/paper_validation_dimensions_9_10_12_20.csv`.
- Tested α = 1.25 and 10 and dimensions d = 2,3,4,5,8,9,10,12,20: **18 cases × 100,000,000 samples = 1.8 billion membership tests**. CSVs preserve hits, seeds, acceptance rates, cylinder volumes, standard errors, and quadrature estimates.
- Reported maximum absolute standardized error = 1.660; maximum absolute relative error = 2.113e-4; all 18 cases are inside their *individual* two-sided 95% normal intervals.
- Numerical volume crossings: a₂=a₃ at α≈7.118390847; a₂=a₄ at α≈23.643510648.
- Independent direct SciPy integration of the paper's quadrature formula reproduced a₂(1.25)=0.4142943509938045, a₂(10)=1.1966680373213512, a₃(10)=1.2306929604275472, and both crossing values. This verifies several numerical anchors, not the full proofs or Monte Carlo execution.

The original 2019 study instead uses movement datasets and empirical comparisons: 724,651 geotagged Twitter posts from 36,639 users, YFCC100M geotagged imagery, and 100,000 simulated Melbourne GPS points; a festival subset had 183 distinct sites. Reported empirical examples include 9/10 vs 6/10 sampled paths within 20% of real OSM path lengths for SSG(3) versus SPG(3), and higher London tour-recommendation F1 (0.774 vs 0.676). These are the *original paper's* application findings, not validation of the new volume theorem.

## Preliminary consistency flags (check against source LaTeX)

1. **Version/archive discrepancy**: [Zenodo 10.5281/zenodo.21291269](https://doi.org/10.5281/zenodo.21291269) archives **v1.0.0**, while the GitHub README describes **v1.1.0** and says the new version has not yet been separately archived. The manuscript calls the Zenodo archive the “exact computational release.” Identify precisely which version produced the submission's numerical artifacts. Its references also list `10.5281/zenodo.21291268`; this may be a concept DOI, so reconcile without assuming it is wrong.
2. **Theorem 2, manuscript p. 7**: duplicated display/text as equations (61) and (62).
3. **Section 6.2, manuscript p. 10**: incomplete prose around “GitHub public repository ...” and “Additionally records ...”.
4. **Conclusion, manuscript p. 12**: visible typo “Devroye’s tageneral results”.
5. **Citation metadata**: `CITATION.cff` title differs from the title used by Zenodo and README; align with chosen canonical release and paper citation.
6. **Statistics**: keep “all 18 within their individual 95% intervals” descriptive; do not claim joint 95% coverage.
7. **Attribution**: do not present planar monotonicity, Gabriel/RNG anchors, spectrum, or Delaunay candidate generation as novel.
8. **Scope of review**: full independent formal proof checking, fresh Monte Carlo reproduction, release-source diffs, and editorial responses remain to be done.

## Editor/reviewer status and subsequent handoff

No editor decision letter, reviewer comments, formal minor-revision decision, target journal, submission ID, or response deadline has been verified. The PDF alone says “Preprint submitted to Elsevier”. Obtain the primary decision correspondence before preparing an itemized response.

For revisions: review README, code, tests, results and any new AGENTS/handoff; locate the **actual LaTeX source**; enumerate reviewer comments; map each to manuscript equations/sections, explicit changes, tests, and response text; preserve all outputs, seeds, figures and releases. Build and visually inspect the two-column PDF before submitting. Do not merge a PR without authorization.
