# Delannoy differences: exact valuations and the two-adic image

**C�sar Augusto Grisa � Independent Researcher**

Version 1.1.0, 17 November 2026. Research preprint and reproducibility archive.
This revision has not been independently peer reviewed or accepted by a journal.

## Separate revision

This branch, `revision-v1.1.0`, contains the new mathematical revision.
The `main` branch remains at the earlier version and is not overwritten.
The exact PDF submitted to Houston Journal of Mathematics on 16 November 2026
is preserved separately; version 1.1.0 has not been sent to the journal.

## Results

For distinct nonnegative M,N let k=v2(M-N), t_X=v2(X(X+1)), t_0=infinity.
The complete difference law gives k+1 if k<=1 and k+2 min(t_M,t_N) otherwise.
The shifted formula also covers every nonnegative scale. The interpolant on
the two-adic integers is injective, has critical points only at 0 and -1,
and has an exact image of normalized Haar measure 1/7. The cubic precision
is sharpened and a quartic term is retained, with a uniform sharpness proof.

Known special cases are credited explicitly. No claim of certified universal
priority is made; see `pesquisa_bibliografica/` for the bounded comparison.

## Files

- `artigo/main.tex`: complete editable English manuscript.
- `artigo/Grisa_Delannoy_differences_v1.1.0.pdf`: matching 16-page PDF.
- `verificacao/pairs_complete_check.py`: 524,800 exact pairs.
- `verificacao/check_saturated_threshold.py`: 148,854 admissible shifted cases.
- `verificacao/precision_explore.py`: 252 exact cubic and quartic checks.
- `verificacao/precision_signed_audit.py`: 1,710 signed modular checks.
- `verificacao/check_image_residues.py`: image residues through modulus 2^16.
- `artigo/eight_checks.py`: eight finite entries in the analytic proof.
- `pesquisa_bibliografica/`: source-by-source comparison and search limits.
- `suplemento/NEG_original.zip`: unchanged original finite archive.

The calculations corroborate written proofs and do not replace them.
Python scripts require only the standard library. Compile `artigo/main.tex`
with a standard LaTeX engine. The original NEG archive does not supply its
term generator, full decomposition definitions, uniform state reduction or
tail proof. Its internal checks do not establish those missing assertions.
The universal total valuation laws do not use that dataset as a premise.

## Archives and license

Revision link: https://github.com/cagrisa-creator/delannoy-valuation-laws/tree/revision-v1.1.0

Published Zenodo record: https://zenodo.org/records/24316985
DOI: https://doi.org/10.5281/zenodo.24316985
The uploaded ZIP preserves the metadata snapshot at packaging; the verified
publication state is recorded here and in `PUBLICATION_STATUS.json`.
See `REGISTRO_DAS_VERSOES.txt` for the separate Houston and revision records.
No deposit to arXiv is authorized or performed.

Manuscript and documentation: CC BY 4.0. Code: MIT.
