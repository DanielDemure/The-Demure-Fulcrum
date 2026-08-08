# The Demure Fulcrum

![The Demure Fulcrum symbol](assets/demure_fulcrum_symbol.png)

> **Working conceptual paper — not peer reviewed**  
> The framework has not been empirically validated as a distinct psychological, clinical, autonomic, or neurobiological response system.

## Overview

**The Demure Fulcrum** proposes negotiation as an **agency-preserving higher-order meta-response under threat**. The central distinction is functional:

- a first-order response selects an action within the situation as currently structured;
- a negotiation meta-response attempts to change the situation's options, constraints, information, commitments, timing, participants, or payoffs.

The revised framework does **not** present negotiation as a demonstrated fourth reflex equivalent to fight, flight, or freeze. It defines a testable construct, specifies where it should and should not apply, compares it with adjacent concepts, and sets out conditions under which evidence should weaken or reject it.

## Core definition

Strict negotiation under threat requires:

1. a meaningful adverse prospect;
2. an influenceable counterpart or institutional process;
3. partial interdependence;
4. communication or signalling;
5. a contingent proposal, request, concession, commitment, or exchange;
6. an attempt to alter the structure of the situation;
7. some retained capacity for refusal, counterproposal, delay, appeal, exit, or alternative action.

Interpersonal and institutional negotiation form the **core empirical construct**. Intrapersonal negotiation and bargaining with fate, God, identity, or meaning are retained as **conceptual and phenomenological extensions**, not assumed to be the same process.

## Read the work

### Main working paper

- [Markdown source](paper/The_Demure_Fulcrum_Academic_Paper.md)
- [Generated PDF](paper/The_Demure_Fulcrum_Academic_Paper.pdf)

The PDF is generated reproducibly from the Markdown and shared BibTeX database by [`scripts/build_pdf.py`](scripts/build_pdf.py). GitHub Actions validates the repository and regenerates the PDF after relevant changes.

### Research companions

- [Threat response, appraisal, and regulation](research/01_threat_response_and_regulation.md)
- [Construct definition, formal model, and empirical designs](research/02_construct_and_formal_model.md)
- [Cultural and philosophical illustrations](research/03_cultural_and_philosophical_illustrations.md)

### Application and provenance

- [Hexure: speculative application note](applications/hexure.md)
- [Concept provenance and revision history](provenance/README.md)

Hexure is deliberately separated from the evidentiary core. Network design, strategic intermediation, ethical commitments, and personal anecdotes do not validate the psychological framework.

## What changed in the 2026 reconstruction?

- The central claim was narrowed from an instinct claim to a higher-order response-policy hypothesis.
- Physiological state, defensive behaviour, meta-response, and institutional application are separated.
- Negotiation is distinguished from appeasement, tend-and-befriend, reappraisal, problem-focused coping, assertiveness, persuasion, and bargaining skill.
- A formal `G → G′` model describes attempts to transform the game rather than merely choose within it.
- Six testable predictions, rival hypotheses, disconfirmation criteria, and a staged research programme are included.
- Polyvagal Theory is treated as contested and non-essential.
- Cultural material is labelled illustrative rather than evidentiary.
- The original weak and placeholder reference list is replaced by a curated scholarly bibliography.
- The twenty-trade anecdote is no longer described as validation.

See the full [`CHANGELOG.md`](CHANGELOG.md).

## Evidence status

The cited literature supports background propositions about defensive behaviour, stress, appraisal, controllability, emotion regulation, social cognition, bargaining, cooperation, and cultural variation. It does not directly establish the Demure Fulcrum as one coherent construct.

The framework earns scientific value only if future research can show:

- reliable behavioural coding;
- selective response to negotiability conditions;
- distinction from adjacent constructs;
- incremental predictive validity;
- meaningful cross-cultural applicability;
- and willingness to accept disconfirming results.

## Review and contribution

Critical review is explicitly invited.

- [Focused review questions](REVIEW_GUIDE.md)
- [Contribution instructions](CONTRIBUTING.md)
- [Shared BibTeX bibliography](references/references.bib)

The most useful contribution may be a well-supported argument that the construct is redundant, incorrectly bounded, culturally narrow, or unsafe in a particular context.

## Reproducible build

```bash
python -m pip install reportlab pyyaml pypdf
python scripts/build_pdf.py
python scripts/validate_repo.py
```

The validator checks required files, citation keys, weak source domains, local links, status language, construct sections, obsolete research paths, CFF metadata, and the generated PDF.

## Citation

Citation metadata is available in [`CITATION.cff`](CITATION.cff). Until a versioned DOI is issued, cite the repository working paper as:

```text
Demure, D. (2026). The Demure Fulcrum: Negotiation as an
Agency-Preserving Meta-Response Under Threat. A Conceptual Framework
and Research Agenda. Working paper, not peer reviewed.
https://github.com/DanielDemure/The-Demure-Fulcrum
```

No DOI has yet been assigned.

## Licence

Original scholarly text, diagrams, and documentation are licensed under the [Creative Commons Attribution 4.0 International Licence](LICENSE). Third-party works and referenced publications remain subject to their respective rights.
