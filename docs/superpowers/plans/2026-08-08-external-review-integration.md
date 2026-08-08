# External Review Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Integrate the attached 8 August 2026 review into the complete repository while preserving the approved framing of negotiation as an agency-preserving higher-order meta-response rather than reverting to an unsupported fourth-autonomic-reflex claim.

**Architecture:** Keep the main working paper as the canonical conceptual framework. Add a transparent author-response document, strengthen the four-form typology and limitations, place neurobiological/developmental/network proposals in a secondary exploratory agenda, deepen the cross-cultural companion without treating examples as proof, and keep Hexure separate as a speculative application. Update visual assets, navigation, validation, and the reproducible PDF build as one reviewed change set.

**Tech Stack:** Markdown, BibTeX, Python 3, ReportLab, GitHub Actions, CC BY 4.0, CFF 1.2.0.

## Global Constraints

- Do not restore claims that negotiation is a demonstrated fourth autonomic reflex, hard-wired instinct, or unique biological module.
- Interpersonal and institutional negotiation are empirical core forms; intrapersonal and existential negotiation remain explicitly labelled extensions.
- Do not preassign unique brain regions, hormonal profiles, clinical syndromes, or universal numerical thresholds to an unvalidated construct.
- Polyvagal Theory remains contested and non-essential.
- Cultural examples generate hypotheses and test measurement portability; they do not prove universality.
- Hexure and the twenty-trade record remain illustrative, not validating evidence.
- The name `Demure` remains eponymous; no unverified etymology is added.
- All scholarly claims use the shared BibTeX database and calibrated language.
- The repository must build and validate in GitHub Actions before merge.

---

### Task 1: Record and classify the external review

**Files:**
- Create: `reviews/2026-08-08-external-review-response.md`
- Modify: `REVIEW_GUIDE.md`

**Interfaces:**
- Consumes: the attached review document and the current scholarly reconstruction.
- Produces: an explicit accepted / partially accepted / not accepted / requires evidence matrix.

- [ ] Summarise every major recommendation: typology, predictions, Polyvagal discussion, limitations, references, Hexure, naming, structure, and cross-cultural material.
- [ ] Identify recommendations already implemented in `main`.
- [ ] Explain modifications to over-specific or unsupported proposed remedies.
- [ ] Add review questions for four-form boundaries and sequencing of behavioural versus neurobiological work.

### Task 2: Strengthen the canonical paper and construct companion

**Files:**
- Modify: `paper/The_Demure_Fulcrum_Academic_Paper.md`
- Modify: `research/02_construct_and_formal_model.md`

**Interfaces:**
- Produces: a four-form typology and a secondary exploratory research agenda that remain subordinate to behavioural construct validation.

- [ ] Replace the three-form table with four forms: interpersonal, institutional, intrapersonal, and existential.
- [ ] State which forms are core empirical targets and which are extensions.
- [ ] Add exploratory hypotheses on expert automaticity, development, cross-cultural portability, network simulation, and physiology, each with explicit prerequisites and disconfirmation conditions.
- [ ] Convert the limitations section into eight named limitations, including categorical-versus-dimensional status and single-author origin.
- [ ] Preserve the existing six core behavioural predictions and formal `G → G′` model.

### Task 3: Deepen cultural and Hexure companions

**Files:**
- Modify: `research/03_cultural_and_philosophical_illustrations.md`
- Modify: `applications/hexure.md`
- Modify: `references/references.bib`

**Interfaces:**
- Produces: a source-qualified cross-cultural research matrix and a preregistration-ready Hexure extension agenda.

- [ ] Add candidate comparative cases for Hawaiian reconciliation, Ubuntu/lekgotla, Japanese consensus preparation, Melanesian exchange politics, and hunter-gatherer conflict management.
- [ ] Label each case as a research candidate and specify what evidence would be needed before making modal or universality claims.
- [ ] Add only bibliographically verified scholarly sources.
- [ ] Clarify `Rewiring Engine`, `Sanctioned Small World`, and `Cathedral Building` as coined application concepts rather than established scientific terms.
- [ ] Add an agent-based simulation outline with benchmark strategies, preregistered outcomes, sensitivity analysis, and no predetermined superiority threshold.

### Task 4: Update public presentation and repository safeguards

**Files:**
- Modify: `README.md`
- Modify: `CHANGELOG.md`
- Modify: `scripts/validate_repo.py`
- Modify: `.github/workflows/build-paper.yml`
- Add: `assets/demure_fulcrum_banner.jpg`
- Replace: `assets/demure_fulcrum_symbol.png`

**Interfaces:**
- Produces: updated navigation, matching visual identity, asset-aware CI, and required-file checks.

- [ ] Use the new wide banner at the top of the README.
- [ ] Keep a compact matching symbol for the generated PDF cover.
- [ ] Link the external-review response and four-form typology from the README.
- [ ] Add `assets/**` to workflow path filters.
- [ ] Require the banner and review response in repository validation.
- [ ] Document the integration in the changelog.

### Task 5: Verify, review, and integrate

**Files:**
- Generated: `paper/The_Demure_Fulcrum_Academic_Paper.pdf`

**Interfaces:**
- Produces: a green pull request and merged `main` branch.

- [ ] Run unit tests, build the PDF, and run the complete repository validator.
- [ ] Inspect the changed-file list and generated PDF artifact.
- [ ] Confirm no prohibited claims or weak bibliography domains were introduced.
- [ ] Open a pull request against `main` with the source-integration decisions documented.
- [ ] Merge only after GitHub Actions succeeds, then confirm the post-merge main-branch build and regenerated PDF.
