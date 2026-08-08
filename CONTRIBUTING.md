# Contributing

Contributions are welcome when they improve conceptual precision, evidentiary quality, testability, ethical safeguards, reproducibility, or accessibility.

## Before contributing

Read:

- [`paper/The_Demure_Fulcrum_Academic_Paper.md`](paper/The_Demure_Fulcrum_Academic_Paper.md)
- [`REVIEW_GUIDE.md`](REVIEW_GUIDE.md)
- [`provenance/README.md`](provenance/README.md)
- [`simulations/README.md`](simulations/README.md) when contributing computational work

The project is a working paper. Do not describe it as peer reviewed, clinically validated, a discovered biological response, or a computationally validated theory.

## Preferred contribution types

- identify overlap with an established construct;
- challenge an inference or boundary condition;
- supply a primary study, systematic review, or major scholarly source;
- improve behavioural coding or experimental design;
- add a documented cross-cultural counterexample;
- report a broken citation, metadata error, or reproducibility problem;
- implement or audit the preregistered simulation protocol;
- submit null, adverse, or falsifying empirical results;
- improve the PDF build or validation scripts without changing scholarly claims silently.

## Issues

Use one main concern per issue. Include the relevant section, the exact claim, and the reason it should change. Link primary or publisher sources where possible.

Suggested issue themes include:

- `review-feedback` — conceptual, methodological, evidentiary, or ethical critique;
- `empirical-results` — completed behavioural, field, clinical, or computational study;
- `literature` — a source that materially changes a claim or boundary;
- `simulation` — implementation, reproduction, protocol ambiguity, or sensitivity finding;
- `reproducibility` — build, metadata, data, or environment problem.

Labels may not yet exist; the theme can be included in the issue title.

## Pull requests

1. Create a focused branch.
2. Keep the Markdown paper as the source of truth.
3. Add or update BibTeX entries in `references/references.bib`.
4. Cite sources with `[@bibkey]` syntax.
5. Run:

```bash
python -m pip install reportlab pyyaml pypdf
python -m unittest discover -s tests -p "test_*.py"
python scripts/build_pdf.py
python scripts/validate_repo.py
```

6. Commit the regenerated PDF with source changes when the paper changes.
7. Explain the conceptual or empirical effect of the change in the pull-request body.
8. State whether the change was preregistered, confirmatory, exploratory, or purely technical.

## Simulation contributions

The current formal protocol is [`simulations/hexure_ipd_protocol.md`](simulations/hexure_ipd_protocol.md). An implementation pull request should include:

- deterministic replay from recorded seeds;
- unit tests for payoffs, strategy state, reputation, rewiring, and shocks;
- frozen configuration files for every confirmatory condition;
- paired initial networks where the protocol calls for paired comparisons;
- export of run-level outcomes and implementation metadata;
- sensitivity and ablation support;
- explicit handling of rewiring cost, observation error, exclusion, false sanction, and concentration;
- no result language implying psychological validation.

Do not tune confirmatory parameters after inspecting outcomes without recording the change as exploratory. Null results and cases where simpler strategies perform better are valuable contributions.

## Empirical-result submissions

An empirical-results issue or pull request should report:

- research question and preregistration status;
- sample or simulation-run size;
- inclusion and exclusion rules;
- measures, task, or strategy implementation;
- statistical analysis and uncertainty;
- all primary outcomes, including null and adverse findings;
- materials, code, data availability, and ethical approval where applicable;
- the narrowest conclusion supported by the design.

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

Do not add invented brain regions, hormonal profiles, evolutionary just-so stories, clinical recommendations, or arbitrary success thresholds presented as established science.

## Licence

By contributing original text or documentation, you agree that it may be distributed under CC BY 4.0. Clearly identify any material that cannot be licensed on those terms. Future software must declare an appropriate software licence separately.
