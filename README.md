# Delannoy valuation laws

**César Augusto Grisa — Independent Researcher**

*Explicit thresholds and multiplicative differences. Version 1.0.2, 16 November 2026.*

## Status

This is a public working preprint and reproducibility archive. It has not
been peer reviewed or accepted by a journal. Internal audits and exact
computations are distinct from independent human refereeing.

Version 1.0.2 updates the presentation and accompanying metadata. The
mathematical statements, proofs, verification scripts, and original finite
NEG dataset are unchanged. A future journal submission has not been selected.

## Mathematical content

The draft presents integrated arguments for Lengyel's four Delannoy valuation
conjectures, including negative shifts whenever both Delannoy indices exist.
It deduces a two-point law for distinct positive even M,N of equal valuation a:

    v2(D(M)-D(N)) = v2(M-N) + 2a.

In particular, for every positive even n and odd integer p>1:

    v2(D(pn)-D(n)) = v2(p-1) + 3*v2(n).

The multiplier need not be prime. The explicit bridge to the finite NEG target
is written out in the manuscript. The universal proof does not use the NEG
tables as a premise.

## Files and reproduction

- `artigo/main.tex`: complete editable English manuscript.
- `artigo/Grisa_Delannoy_valuation_laws.pdf`: matching current preprint PDF.
- `O_que_a_uniao_resolve.pdf`: Portuguese explanation of results and limits.
- `artigo/eight_checks.py`: eight finite evaluations used in the proof.
- `artigo/check_cubic_increment.py`: checks of the cubic increment.
- `artigo/reaudit_full_theorem.py`: checks of the earlier integrated theorem.
- `artigo/check_joined_claims.py`: 14,016 additional checks, zero failures.
- `artigo/verify_NEG_archive.py`: internal archive-consistency checks only.
- `suplemento/NEG_original.zip`: original supplied NEG archive, unchanged.

Scripts require only Python 3's standard library and write reports next to
themselves. To compile the manuscript, run `pdflatex main.tex` twice inside
`artigo/`.

The retained NEG tables contain 11,858 states representing 13,552 NEG cases.
The missing term generator, block definitions, uniform state reduction, and
tail proof were not reconstructed. A total valuation law does not establish
those separate internal claims.

## Provenance and citation

This is a substantially revised working draft derived from the earlier
[Delannoy C4 candidate archive](https://github.com/cagrisa-creator/delannoy-c4-candidate).
The earlier project is not overwritten. See `CITATION.cff` for author metadata.
New repository: https://github.com/cagrisa-creator/delannoy-valuation-laws

Zenodo version 1.0.2 is saved as a new-version draft at
https://zenodo.org/uploads/24293242. Reserved DOI: `10.5281/zenodo.24293242`.
The new files and description have not yet been published in Zenodo. Earlier releases remain available in the
repository and Zenodo version history.

## License

Manuscript and documentation: CC BY 4.0 (`LICENSE-DOCS`).
Code: MIT (`LICENSE-CODE`).

## Publication preference (16 November 2026)

The author will decide whether and where to submit a future version.
No arXiv deposit is authorized. GitHub and Zenodo are archival destinations,
not journal acceptance.
