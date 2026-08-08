#!/usr/bin/env python3
"""One-time integration of the 8 August 2026 external review.

The migration intentionally preserves the repository's calibrated meta-response
framing while integrating useful review deltas. It is designed for one run on
revision/2026-review-integration and validates all source markers before writing.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def replace_section(text: str, start: str, end: str, replacement: str, rel: str) -> str:
    if text.count(start) != 1:
        raise RuntimeError(f"{rel}: expected one start marker: {start!r}")
    start_index = text.index(start)
    end_index = text.find(end, start_index + len(start))
    if end_index < 0:
        raise RuntimeError(f"{rel}: end marker not found: {end!r}")
    return text[:start_index] + replacement.strip() + "\n\n" + text[end_index:]


def insert_before(text: str, marker: str, block: str, rel: str) -> str:
    key = block.strip().splitlines()[0]
    if key in text:
        return text
    if text.count(marker) != 1:
        raise RuntimeError(f"{rel}: expected one insertion marker: {marker!r}")
    return text.replace(marker, block.strip() + "\n\n" + marker, 1)


def insert_after(text: str, marker: str, block: str, rel: str) -> str:
    key = block.strip().splitlines()[0]
    if key in text:
        return text
    if text.count(marker) != 1:
        raise RuntimeError(f"{rel}: expected one insertion marker: {marker!r}")
    return text.replace(marker, marker + "\n\n" + block.strip(), 1)


def replace_once(text: str, old: str, new: str, rel: str) -> str:
    if old == new:
        return text
    if text.count(old) != 1:
        raise RuntimeError(f"{rel}: expected one exact replacement for {old[:80]!r}")
    return text.replace(old, new, 1)


def transform_paper(text: str) -> str:
    rel = "paper/The_Demure_Fulcrum_Academic_Paper.md"
    typology = r"""
## 4.3 Four Forms of Negotiation

The external review usefully separates four meanings that had previously been compressed into three rows. They are retained here with different evidentiary status rather than treated as one biological system.

| Form | Counterpart or decision structure | Main structural target | Evidentiary status |
|---|---|---|---|
| **Interpersonal negotiation** | one or more responsive people or groups | offers, concessions, information, commitments, timing, or relationship terms | core empirical form |
| **Institutional negotiation** | an authorised procedure, representative, organisation, regulator, court, appeal channel, or multi-actor governance process | rules, permissions, enforcement, representation, decision rights, or available channels | core empirical form |
| **Intrapersonal negotiation** | competing goals, identities, values, or temporal selves | priorities, self-imposed rules, interpretations, or commitments | conceptual extension overlapping self-regulation and reappraisal |
| **Existential negotiation** | fate, God, death, identity, meaning, or an imagined absolute | the narrative relationship to conditions that may be literally uncontrollable | phenomenological and cultural extension, not direct behavioural evidence |

Interpersonal and institutional forms satisfy the strict construct only when an influenceable external actor or process can respond contingently. Institutional negotiation is separated because authority, cognition, memory, and commitment can be distributed across procedures and representatives rather than residing in one counterpart. A grievance appeal, mediated settlement, labour negotiation, or regulatory waiver can therefore qualify even when no single person controls the whole outcome.

Intrapersonal negotiation may describe useful self-dialogue: “If I complete this task, I will permit myself rest,” or “I can retain this value while revising that belief.” Yet such cases lack an independent external decision maker. They should not be assumed to share all mechanisms with bargaining.

Existential negotiation names a lived experience in which a person bargains with what cannot literally respond. Prayer, vows, defiance of fate, and bargaining in grief may preserve a sense of subjecthood, but they are better studied through phenomenology, narrative psychology, religion, or meaning-making than through a standard negotiation experiment.

The forms do not share a presumed unique neural substrate. Nor is positive-sum agreement a definitional requirement: distributive, hostile, or coercive bargaining can still contain contingency and structural transformation. Ethical legitimacy, outcome quality, and degree of residual agency must be coded separately.
"""
    text = replace_section(
        text,
        "## 4.3 Strict, intrapersonal, and existential forms",
        "# 5. Differentiation from Adjacent Constructs",
        typology,
        rel,
    )

    exploratory = r"""
## 10.7 Secondary Mechanism and Extension Hypotheses

The six predictions above concern the behavioural core and should be tested first. The following hypotheses respond to proposals in the external review but remain secondary. They become interpretable only after researchers can code strict negotiation reliably and distinguish it from active coping, persuasion, appeasement, and ordinary skill.

### 10.7.1 Expertise and partial automaticity

Experienced crisis negotiators, mediators, or diplomats may identify negotiability cues and generate appropriate first moves faster than matched non-experts. Behavioural latency and EEG may test whether expertise changes early attention, frontal control, or later evaluative processing. A difference would support learned automaticity, not a newly discovered autonomic reflex.

**Prerequisite:** experts and controls must perform a task that has already demonstrated negotiation-specific behavioural validity.

**Disconfirmation condition:** if expertise affects only general speed, vocabulary, or confidence and does not improve detection of influenceability, contingency, or structural options, the automaticity extension is weakened.

### 10.7.2 Developmental emergence

Negotiation behaviours may become more complex as children develop perspective taking, metacognition, language, executive control, and understanding of commitments [@premack1978; @flavell1979; @tomasello2005]. The repository does not assume a fixed age window or a six-month relation to one Theory-of-Mind milestone.

**Prerequisite:** tasks must separate requests, turn taking, persuasion, and imitation from genuinely contingent attempts to alter terms.

**Disconfirmation condition:** if age-related changes are fully explained by language, general inhibition, or learned scripts, no negotiation-specific developmental sequence is established.

### 10.7.3 Cross-cultural portability

The structural definition should permit coding across contexts that use direct offers, indirect signalling, mediators, households, elders, councils, or collective representation. Surface form and the meaning of agency may vary substantially [@brett2000].

**Prerequisite:** local scholars and participants must help define authority, commitment, refusal, collective interest, and acceptable evidence.

**Disconfirmation condition:** failure of inter-rater reliability or measurement invariance after localisation requires revision or abandonment of universal framing; no preset percentage of societies is treated as proof.

### 10.7.4 Dynamic-network simulation

Agent-based models can test whether contingent cooperation, reputation, partner choice, and rewiring improve outcomes under specified network conditions [@wattsstrogatz1998; @nowak2006; @rand2011]. Such results would evaluate a formal strategy, not validate the psychological construct or the Hexure brand.

**Prerequisite:** strategies, topology, mutation, noise, payoff structure, rewiring costs, seeds, and benchmark models must be preregistered.

**Disconfirmation condition:** if performance depends on tuned assumptions, disappears under sensitivity analysis, or fails to improve on simpler strategies out of sample, the claimed application advantage is rejected.

### 10.7.5 Psychophysiological constraint

After behavioural validation, autonomic, endocrine, EEG, or neuroimaging studies may test how arousal, time pressure, preparation, and task support constrain negotiation [@arnsten2009; @hermans2014; @shields2016]. No dlPFC, vmPFC, amygdala, vagal, or cortisol pattern is declared unique in advance.

**Prerequisite:** control conditions must match cognitive effort, social interaction, language, and outcome stakes without permitting structural negotiation.

**Disconfirmation condition:** if observed physiology tracks generic effort, threat, or social engagement rather than validated negotiation behaviour, it does not support a distinct mechanism.
"""
    text = insert_before(text, "# 11. Disconfirmation Criteria", exploratory, rel)

    limitations = r"""
# 15. Limitations

## 15.1 Theoretical, not empirical, status

The framework is theoretical. The cited literatures establish threat dynamics, appraisal, regulation, social cognition, bargaining, and cooperation; they do not directly validate the Demure Fulcrum as one construct. The predictions are a research agenda, not findings.

## 15.2 Categorical versus dimensional status

Negotiation may not be a categorical response comparable to a discrete reflex. It may prove to be a higher-order policy, a dimensional combination of active coping and social cognition, or a context-dependent overlay that modulates several action tendencies. The repository favours the meta-response interpretation, but empirical work must adjudicate rather than assume distinctiveness.

## 15.3 Cultural and WEIRD-sample bias

Much relevant research comes from Western, educated, industrialised, rich, and democratic settings. Explicit individual bargaining, personal veto, and direct interest statements may not capture collective, relational, implicit, or mediator-led practices. Cross-cultural work must test local meanings and measurement invariance rather than adding decorative examples.

## 15.4 Overlap and incremental validity

The framework may overlap extensively with problem-focused coping, perceived control, social problem solving, assertiveness, cognitive reappraisal, and negotiation skill. Incremental validity is an empirical requirement. A branded label that adds no reliable explanatory or predictive value should be narrowed or rejected.

## 15.5 Power, residual agency, and safety

The language of agency can become moralising. People facing violence, coercive control, disability, poverty, discrimination, or institutional exclusion may have very limited alternatives. Appeasement, exit, silence, or immediate protective action can be safer than negotiation. The framework must not convert structural deprivation into an individual failure to find leverage.

## 15.6 Neurobiological specificity

Prefrontal, cingulate, amygdala, default-mode, autonomic, and endocrine processes proposed as possible correlates participate in many forms of cognition and social behaviour. No unique neural or hormonal signature has been established. Biological studies require validated behavioural tasks and control conditions matched for effort, language, social interaction, and threat.

## 15.7 Evolutionary and formal-model inference

The evolutionary rationale is plausible but indirect. Comparative, archaeological, and ethnographic evidence cannot cleanly identify the emergence of a negotiation meta-response. Likewise, `G → G′` is a simplifying formal representation: values may be unstable, actors may misunderstand themselves, commitments may fail, and emotion may change what counts as a payoff.

## 15.8 Single-author origin and branded label

The framework originates with one author and has not undergone formal peer review. Open publication, explicit falsification criteria, and invited criticism improve transparency but do not substitute for independent replication. The name *Demure* is eponymous and may shape interpretation; future research should test the construct without relying on the brand.
"""
    text = replace_section(text, "# 15. Limitations", "# 16. Conclusion", limitations, rel)
    return text


def transform_construct_companion(text: str) -> str:
    rel = "research/02_construct_and_formal_model.md"
    typology = r"""
### 3.4 Four-form typology and coding consequence

The framework distinguishes four forms because they require different units of analysis.

| Form | Unit of analysis | Core coding consequence |
|---|---|---|
| Interpersonal | exchange among responsive external agents | code offers, counteroffers, information, concessions, commitments, and alternatives |
| Institutional | exchange through authorised rules, representatives, appeals, or multi-actor procedures | code who has authority, how the procedure can change terms, and where commitments are stored or enforced |
| Intrapersonal | interaction among goals, values, identities, or temporal selves | do not score as strict negotiation; study as a self-regulation extension |
| Existential | narrative engagement with fate, death, God, meaning, or an imagined absolute | do not score as strict negotiation; study phenomenology and cultural meaning |

Interpersonal and institutional episodes may be combined for some analyses only after testing whether their measurement structure is equivalent. Institutional cases may distribute authority and memory across several nodes, making “the counterpart” a process rather than one person. Intrapersonal and existential cases should never be used as positive examples in a confirmatory scale for the strict construct.
"""
    text = insert_before(text, "## 4. Formal representation", typology, rel)

    studies = r"""
### 8.6 Secondary exploratory studies

These studies are downstream of Experiments A–E and should not be launched as searches for a unique biomarker before construct validity exists.

#### Study F: expert cue detection and automaticity

Compare experienced negotiators with matched controls on validated scenarios containing or withholding influenceability, contingency, and transformability. Measure behavioural latency and accuracy first; EEG may then examine timing. The critical test is selective detection of negotiability, not a generic expert speed advantage.

#### Study G: developmental differentiation

Use age-appropriate interactive conflicts to separate requests, persuasion, sharing, imitation, appeasement, and contingent exchange. Model language, executive function, perspective taking, and metacognition [@flavell1979]. Do not preregister a fixed age boundary as though the construct were one maturational switch.

#### Study H: cross-cultural portability

Translate the codebook through collaborative adaptation, not literal wording alone. Compare direct and indirect signalling, individual and collective representation, and mediator-led processes. Test coder reliability and measurement invariance; treat failure as evidence for localisation or construct revision.

#### Study I: psychophysiological constraints

After behavioural validity, compare negotiation with effort-matched social problem solving, persuasion, and non-social control conditions. Measure arousal, EEG, endocrine response, or imaging only to constrain mechanisms. No region or hormone is assumed diagnostic.

#### Study J: dynamic-network strategy comparison

Formalise a negotiation-inspired strategy independently of the Hexure name. Compare it with Always Defect, Tit-for-Tat, Generous Tit-for-Tat, Grim Trigger, Win-Stay-Lose-Shift, and partner-choice baselines across topology, noise, rewiring cost, and payoff regimes. Preregister seeds, primary outcomes, sensitivity analyses, and out-of-sample replications. A tuned win under one parameter set is not evidence of general superiority.
"""
    text = insert_before(text, "## 9. Analysis plan principles", studies, rel)
    return text


def transform_cultural_companion(text: str) -> str:
    rel = "research/03_cultural_and_philosophical_illustrations.md"
    block = r"""
## 10. Cross-cultural comparison as a research programme

Cross-cultural extension is necessary, but a named tradition should not be counted as proof merely because it contains reconciliation, reciprocity, consensus, or gift exchange. The relevant question is whether local practices contain an influenceable authority, contingent exchange, attempted transformation, and a culturally meaningful form of residual agency.

The following cases are **candidate research sites**, not evidence that negotiation is the modal response of a society.

| Candidate case | Scholarly starting point | Potential relevance | Required caution |
|---|---|---|---|
| Hawaiian *ho'oponopono* | Shook's study of contemporary Hawaiian problem-solving practice [@shook1986] | facilitated family process, admission, restitution, relationship repair, and restoration of balance | document historical and contemporary variation; do not infer a universal Hawaiian response or treat reconciliation as automatically agent-preserving |
| Ubuntu, reconciliation, and council processes | Tutu's account of truth and reconciliation provides one macro-level entry point [@tutu1999] | collective recognition, testimony, accountability, relationship continuity, and negotiated political transition | Ubuntu is not one procedure; local legal and ethnographic work is needed on *lekgotla* and other council forms |
| Japanese *wa* and *nemawashi* | Lebra's analysis of Japanese behavioural patterns [@lebra1976] | indirect signalling, consensus preparation, face, role, and relationship-preserving decision processes | avoid national-character generalisation; compare sectors, generations, hierarchy, and cases where consensus masks coercion |
| Mendi gift politics in Highland Papua New Guinea | Lederman's ethnography of gifts, social relations, and politics [@lederman1986] | reputation, exchange, brokerage, obligation, coalition, and distributed political influence | gift exchange is not reducible to positive-sum bargaining; code gender, status, coercion, and historical change |
| Ju/'hoansi and other forager conflict contexts | Lee's ethnography, together with work on egalitarian institutions and exchange [@lee1979; @woodburn1982; @wiessner2002] | mediation, mobility, levelling, sharing, humour, reputation, and exit as possible components of conflict management | do not claim that negotiation is modal without systematic event coding; violence, departure, gender, and external pressure must remain visible |

### 10.1 Minimum comparative evidence

For each case, researchers should document:

1. who can authoritatively alter the outcome;
2. how interests are represented—individual, household, lineage, community, or office;
3. how contingency is expressed, including silence, intermediaries, ritual, gifts, sequencing, or indirect language;
4. what makes a commitment credible and how breach is handled;
5. whether refusal, appeal, delay, exit, mobility, or collective voice remains available;
6. how often the practice occurs relative to command, violence, withdrawal, avoidance, or imposed settlement;
7. whose agency and safety are preserved or sacrificed;
8. whether the account describes an ideal, a historical institution, a contemporary practice, or observed episodes.

### 10.2 Comparative design

A defensible programme would combine local-language archival work, ethnography, event coding, interviews, and collaboration with scholars or communities who can challenge imported categories. It should sample counterexamples as deliberately as apparent matches. Measurement invariance should be tested across sites; failure would require localisation or revision rather than treating local practice as deficient.

### 10.3 What convergence could mean

Cross-cultural recurrence could support a modest claim: interdependent groups repeatedly develop social technologies for altering terms without immediate force or exit. It would not establish a dedicated neural circuit, a universal fourth response, or a predetermined percentage of societies in which negotiation is “default.”
"""
    return replace_section(
        text,
        "## 10. Cross-cultural expansion without tokenism",
        "## 11. What cultural recurrence can support",
        block,
        rel,
    )


def transform_hexure(text: str) -> str:
    rel = "applications/hexure.md"
    if "## 3. Architecture vocabulary and falsifiable status" not in text:
        def renumber(match: re.Match[str]) -> str:
            number = int(match.group(1))
            return f"## {number + 1}. " if number >= 3 else match.group(0)

        text = re.sub(r"^## (\d+)\. ", renumber, text, flags=re.MULTILINE)
        architecture = r"""
## 3. Architecture vocabulary and falsifiable status

Hexure uses three coined terms. They are design hypotheses, not established constructs in network science.

### Rewiring Engine

A **Rewiring Engine** is a governance capability that identifies, creates, modifies, or ends relationships and decision channels. It may add a mediator, alternative supplier, appeal route, escrow mechanism, verified bridge, or exit option. Its value must be compared with simpler interventions rather than inferred from the metaphor.

### Sanctioned Small World

A **Sanctioned Small World** is a proposed network subset in which eligibility, reputation, commitments, sanctions, privacy, and exit are governed explicitly. The term does not imply that cooperation is guaranteed or “structurally enforced.” Rules can be gamed, sanctions can concentrate power, and filtering can create exclusion or groupthink.

### Cathedral Building

**Cathedral Building** is a normative reinvestment rule: a declared portion of value is directed toward durable shared capacity, knowledge, resilience, or public goods. It is not derived from graph topology. Tests must specify governance, beneficiaries, opportunity cost, durability, and whether the mechanism reduces or entrenches dependence on the intermediary.

These definitions make the application vulnerable to failure. If a named mechanism adds no benefit beyond ordinary partner choice, contracting, mediation, or governance, the brand should not be treated as explanatory.
"""
        text = insert_before(text, "## 4. Rewiring as an organisational capability", architecture, rel)

    simulation = r"""
### Simulation preregistration outline

A network simulation should be specified before results are observed:

- **topology:** lattice, random, scale-free, and Watts–Strogatz small-world variants;
- **strategies:** Always Defect, Tit-for-Tat, Generous Tit-for-Tat, Grim Trigger, Win-Stay-Lose-Shift, random partner choice, and a clearly formalised negotiation-inspired strategy;
- **rewiring:** who may sever or create links, at what cost, with what information, delay, and capacity limit;
- **reputation:** observation error, strategic manipulation, decay, privacy, and false positives;
- **shocks:** defector entry, information corruption, bridge failure, coalition capture, and resource inequality;
- **outcomes:** mean and distributional payoff, cooperation, exclusion, resilience, concentration of power, false sanction, and recovery time;
- **robustness:** preregistered parameter ranges, seeds, sensitivity analysis, ablations, and held-out conditions;
- **reporting:** publish null results and the regions in which simpler strategies outperform the named model.

No cooperation percentage or superiority margin is assumed in advance. A result would support only the formalised strategy under the tested conditions; it would not validate the psychological framework.
"""
    text = insert_before(text, "Each hypothesis can fail.", simulation, rel)
    return text


def transform_readme(text: str) -> str:
    rel = "README.md"
    text = replace_once(
        text,
        "![The Demure Fulcrum symbol](assets/demure_fulcrum_symbol.png)",
        "![The Demure Fulcrum — negotiation as an agency-preserving meta-response under threat](assets/demure_fulcrum_banner.jpg)",
        rel,
    )
    four_forms = r"""
## Four-form typology

- **Interpersonal negotiation** — responsive external people or groups; core empirical form.
- **Institutional negotiation** — authorised procedures, representatives, appeals, rules, or multi-actor governance; core empirical form.
- **Intrapersonal negotiation** — deliberation among goals, values, identities, or temporal selves; conceptual extension.
- **Existential negotiation** — bargaining with fate, God, death, meaning, or an imagined absolute; phenomenological extension.

The forms are not treated as one biological system. The strict research construct applies to interpersonal and institutional episodes that contain an influenceable counterpart or process, contingency, attempted structural transformation, and residual agency.
"""
    marker = "Interpersonal and institutional negotiation form the **core empirical construct**. Intrapersonal negotiation and bargaining with fate, God, identity, or meaning are retained as **conceptual and phenomenological extensions**, not assumed to be the same process."
    text = insert_after(text, marker, four_forms, rel)
    text = replace_once(
        text,
        "- Six testable predictions, rival hypotheses, disconfirmation criteria, and a staged research programme are included.",
        "- Six core behavioural predictions, rival hypotheses, disconfirmation criteria, and a staged research programme are included.\n- A second review cycle adds four explicit forms and secondary developmental, cross-cultural, network, expertise, and psychophysiological hypotheses without predeclaring biomarkers or universal thresholds.",
        rel,
    )
    text = replace_once(
        text,
        "- [Focused review questions](REVIEW_GUIDE.md)\n- [Contribution instructions](CONTRIBUTING.md)",
        "- [Focused review questions](REVIEW_GUIDE.md)\n- [Response to the 8 August 2026 external review](reviews/2026-08-08-external-review-response.md)\n- [Contribution instructions](CONTRIBUTING.md)",
        rel,
    )
    return text


def transform_review_guide(text: str) -> str:
    rel = "REVIEW_GUIDE.md"
    text = replace_once(
        text,
        "7. **Evidence calibration**  \n   Which claims are supported by the cited literature, which are only plausible inferences, and which require direct study?",
        "7. **Four-form boundary**  \n   Does separating interpersonal, institutional, intrapersonal, and existential forms clarify the theory, or does institutional negotiation remain reducible to interpersonal bargaining and procedure? Are the extensions labelled strongly enough?\n\n8. **Evidence sequencing**  \n   Is behavioural construct validation appropriately prior to clinical, developmental, endocrine, EEG, or neuroimaging claims? Which secondary hypothesis is mature enough to test first?\n\n9. **Evidence calibration**  \n   Which claims are supported by the cited literature, which are only plausible inferences, and which require direct study?",
        rel,
    )
    text = insert_after(
        text,
        "## How to review",
        "The repository's documented response to the latest supplied critique is available at [`reviews/2026-08-08-external-review-response.md`](reviews/2026-08-08-external-review-response.md). Reviewers are encouraged to challenge both the external recommendations and the author's integration decisions.",
        rel,
    )
    return text


def transform_changelog(text: str) -> str:
    rel = "CHANGELOG.md"
    block = r"""
### External-review integration

- Added a public accepted / partially accepted / not accepted / requires-evidence response to the 8 August 2026 review.
- Split the typology into interpersonal, institutional, intrapersonal, and existential forms while retaining core-versus-extension status.
- Added secondary hypotheses on expert automaticity, development, cross-cultural portability, dynamic-network simulation, and psychophysiological constraints after behavioural validation.
- Recast limitations as eight named constraints, including categorical-versus-dimensional status and single-author origin.
- Expanded the cultural companion into a source-qualified comparative research programme rather than a universality argument.
- Defined Hexure's Rewiring Engine, Sanctioned Small World, and Cathedral Building as falsifiable application concepts and added a simulation preregistration outline.
- Updated the README banner, matching PDF-cover symbol, workflow asset tracking, and repository validation requirements.
"""
    return insert_before(text, "### Changed", block, rel)


def transform_validator(text: str) -> str:
    rel = "scripts/validate_repo.py"
    text = replace_once(
        text,
        '    "README.md",\n    "CITATION.cff",',
        '    "README.md",\n    "assets/demure_fulcrum_banner.jpg",\n    "assets/demure_fulcrum_symbol.png",\n    "reviews/2026-08-08-external-review-response.md",\n    "CITATION.cff",',
        rel,
    )
    text = replace_once(
        text,
        '        "Boundary Conditions",\n        "Differentiation from Adjacent Constructs",',
        '        "Boundary Conditions",\n        "Four Forms of Negotiation",\n        "Differentiation from Adjacent Constructs",',
        rel,
    )
    text = replace_once(
        text,
        '        "Testable Predictions",\n        "Disconfirmation Criteria",',
        '        "Testable Predictions",\n        "Secondary Mechanism and Extension Hypotheses",\n        "Disconfirmation Criteria",',
        rel,
    )
    return text


def transform_workflow(text: str) -> str:
    rel = ".github/workflows/build-paper.yml"
    old = '      - "applications/**"\n      - "provenance/**"'
    new = '      - "applications/**"\n      - "assets/**"\n      - "provenance/**"\n      - "reviews/**"'
    if text.count(old) != 2:
        raise RuntimeError(f"{rel}: expected two path-filter insertion points")
    return text.replace(old, new)


def transform_bibliography(text: str) -> str:
    rel = "references/references.bib"
    entries = r"""

@article{flavell1979,
  author = {Flavell, John H.},
  title = {Metacognition and Cognitive Monitoring: A New Area of Cognitive-Developmental Inquiry},
  year = {1979},
  journal = {American Psychologist},
  volume = {34},
  number = {10},
  pages = {906--911},
  doi = {10.1037/0003-066X.34.10.906}
}

@book{shook1986,
  author = {Shook, E. Victoria},
  title = {Ho'oponopono: Contemporary Uses of a Hawaiian Problem-Solving Process},
  year = {1986},
  publisher = {University of Hawaii Press},
  url = {https://uhpress.hawaii.edu/title/hooponopono-contemporary-uses-of-a-hawaiian-problem-solving-process/}
}

@book{tutu1999,
  author = {Tutu, Desmond},
  title = {No Future Without Forgiveness},
  year = {1999},
  publisher = {Doubleday}
}

@book{lebra1976,
  author = {Lebra, Takie Sugiyama},
  title = {Japanese Patterns of Behavior},
  year = {1976},
  publisher = {University Press of Hawaii}
}

@book{lederman1986,
  author = {Lederman, Rena},
  title = {What Gifts Engender: Social Relations and Politics in Mendi, Highland Papua New Guinea},
  year = {1986},
  publisher = {Cambridge University Press},
  doi = {10.1017/CBO9780511753022}
}

@book{lee1979,
  author = {Lee, Richard B.},
  title = {The !Kung San: Men, Women, and Work in a Foraging Society},
  year = {1979},
  publisher = {Cambridge University Press}
}
"""
    for key in ("flavell1979", "shook1986", "tutu1999", "lebra1976", "lederman1986", "lee1979"):
        if re.search(rf"@[A-Za-z]+\s*\{{\s*{key}\s*,", text):
            raise RuntimeError(f"{rel}: bibliography key already exists: {key}")
    return text.rstrip() + entries + "\n"


def build_changes() -> dict[str, str]:
    return {
        "paper/The_Demure_Fulcrum_Academic_Paper.md": transform_paper(read("paper/The_Demure_Fulcrum_Academic_Paper.md")),
        "research/02_construct_and_formal_model.md": transform_construct_companion(read("research/02_construct_and_formal_model.md")),
        "research/03_cultural_and_philosophical_illustrations.md": transform_cultural_companion(read("research/03_cultural_and_philosophical_illustrations.md")),
        "applications/hexure.md": transform_hexure(read("applications/hexure.md")),
        "README.md": transform_readme(read("README.md")),
        "REVIEW_GUIDE.md": transform_review_guide(read("REVIEW_GUIDE.md")),
        "CHANGELOG.md": transform_changelog(read("CHANGELOG.md")),
        "scripts/validate_repo.py": transform_validator(read("scripts/validate_repo.py")),
        ".github/workflows/build-paper.yml": transform_workflow(read(".github/workflows/build-paper.yml")),
        "references/references.bib": transform_bibliography(read("references/references.bib")),
    }


def validate_outputs(changes: dict[str, str]) -> None:
    paper = changes["paper/The_Demure_Fulcrum_Academic_Paper.md"]
    required = (
        "## 4.3 Four Forms of Negotiation",
        "## 10.7 Secondary Mechanism and Extension Hypotheses",
        "## 15.8 Single-author origin and branded label",
        "# 16. Conclusion",
    )
    for phrase in required:
        if phrase not in paper:
            raise RuntimeError(f"paper output lacks {phrase!r}")

    prohibited = (
        "is a fourth primary instinct",
        "hard-wired survival instinct",
        "provides quantitative validation",
        "constitutes quantitative validation",
    )
    combined = "\n".join(changes.values()).lower()
    for phrase in prohibited:
        if phrase in combined:
            raise RuntimeError(f"prohibited positive claim introduced: {phrase}")

    if '      - "assets/**"' not in changes[".github/workflows/build-paper.yml"]:
        raise RuntimeError("workflow output lacks assets path filter")
    if '      - "reviews/**"' not in changes[".github/workflows/build-paper.yml"]:
        raise RuntimeError("workflow output lacks reviews path filter")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="validate markers and generated outputs without writing")
    args = parser.parse_args()

    changes = build_changes()
    validate_outputs(changes)

    if args.check:
        print("Review integration preflight passed")
        for rel, content in changes.items():
            original = read(rel)
            print(f"- {rel}: {len(original):,} -> {len(content):,} characters")
        return 0

    for rel, content in changes.items():
        path = ROOT / rel
        path.write_text(content, encoding="utf-8")
        print(f"Updated {rel}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
