# Contributing

Contributions are welcome when they improve conceptual precision, evidentiary quality, testability, ethical safeguards, reproducibility, or accessibility.

## Before contributing

Read:

- [`paper/The_Demure_Fulcrum_Academic_Paper.md`](paper/The_Demure_Fulcrum_Academic_Paper.md)
- [`REVIEW_GUIDE.md`](REVIEW_GUIDE.md)
- [`provenance/README.md`](provenance/README.md)

The project is a working paper. Do not describe it as peer reviewed, clinically validated, or a discovered biological response.

## Preferred contribution types

- identify overlap with an established construct;
- challenge an inference or boundary condition;
- supply a primary study, systematic review, or major scholarly source;
- improve behavioural coding or experimental design;
- add a documented cross-cultural counterexample;
- report a broken citation, metadata error, or reproducibility problem;
- improve the PDF build or validation scripts without changing scholarly claims silently.

## Issues

Use one main concern per issue. Include the relevant section, the exact claim, and the reason it should change. Link primary or publisher sources where possible.

## Pull requests

1. Create a focused branch.
2. Keep the Markdown paper as the source of truth.
3. Add or update BibTeX entries in `references/references.bib`.
4. Cite sources with `[@bibkey]` syntax.
5. Run:

```bash
python -m pip install reportlab pyyaml pypdf
python scripts/build_pdf.py
python scripts/validate_repo.py
```

6. Commit the regenerated PDF with source changes.
7. Explain the conceptual effect of the change in the pull-request body.

## Source standard

For scientific claims, prefer:

1. primary empirical studies and original theory publications;
2. systematic reviews and meta-analyses;
3. major scholarly syntheses and academic books.

Popular articles may be cited only when the popular artefact itself is being analysed. Wikipedia, social media, listicles, and commercial explainers are not acceptable support for scientific propositions.

## Style and epistemic language

Use calibrated verbs:

- *shows* only for evidence directly demonstrated;
- *supports* when evidence increases plausibility;
- *is consistent with* when multiple explanations remain;
- *proposes* for the framework's own claims;
- *illustrates* for cultural examples;
- *speculates* for untested applications.

Do not add invented brain regions, hormonal profiles, evolutionary just-so stories, or clinical recommendations.

## Licence

By contributing original text or documentation, you agree that it may be distributed under CC BY 4.0. Clearly identify any material that cannot be licensed on those terms.
