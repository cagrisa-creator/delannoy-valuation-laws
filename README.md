# Delannoy valuation laws

**César Augusto Grisa — Independent Researcher**

*Explicit thresholds and multiplicative differences. Version 1.0.0, 9 November 2026.*

## Status

This is a working preprint, not a peer-reviewed theorem paper. The manuscript
discloses AI-assisted mathematical review, proof suggestions, verification,
literature search, and drafting. The author must verify the arguments and
adapt the narrative to the chosen journal's authorship policy.

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
- `O_que_a_uniao_resolve.pdf`: Portuguese explanation of results and limits.
- `artigo/eight_checks.py`: eight finite evaluations used in the proof.
- `artigo/check_cubic_increment.py`: checks of the cubic increment.
- `artigo/reaudit_full_theorem.py`: checks of the earlier integrated theorem.
- `artigo/check_joined_claims.py`: 14,016 additional checks, zero failures.
- `artigo/verify_NEG_archive.py`: internal archive-consistency checks only.
- `suplemento/NEG_original.zip`: original supplied NEG archive, unchanged.

Scripts require only Python 3's standard library and write reports next to
themselves. To compile the manuscript, run `pdflatex main.tex` twice inside
`artigo/`, or open that folder in the Codex LaTeX editor.

The retained NEG tables contain 11,858 states representing 13,552 NEG cases.
The missing term generator, block definitions, uniform state reduction, and
tail proof were not reconstructed. A total valuation law does not establish
those separate internal claims.

## Provenance and citation

This is a substantially revised working draft derived from the earlier
[Delannoy C4 candidate archive](https://github.com/cagrisa-creator/delannoy-c4-candidate).
The earlier project is not overwritten. See `CITATION.cff` for author metadata.
New repository: https://github.com/cagrisa-creator/delannoy-valuation-laws

Reserved DOI: `10.5281/zenodo.24074633` (not active until the Zenodo draft is published).
The deposit is currently saved as a draft.

## License

Manuscript and documentation: CC BY 4.0 (`LICENSE-DOCS`).
Code: MIT (`LICENSE-CODE`).

## Publication preference (9 November 2026)

The author does not authorize depositing this work on arXiv. The current
Courant/CPAM submission route requires arXiv, so it is excluded under this
constraint. A US journal accepting direct submission is to be selected.
GitHub and Zenodo are archival destinations, not journal acceptance.
