#!/usr/bin/env python3
"""Integrate the simulation addendum and correct the review-response modality summary."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"expected exactly one marker for {label}, found {count}")
    return text.replace(old, new, 1)


def transform_paper(text: str) -> str:
    old_development = (
        "Negotiation behaviours may become more complex as children develop perspective taking, "
        "metacognition, language, executive control, and understanding of commitments "
        "[@premack1978; @flavell1979; @tomasello2005]. The repository does not assume a fixed age "
        "window or a six-month relation to one Theory-of-Mind milestone."
    )
    new_development = (
        "Negotiation behaviours may become more complex as children develop perspective taking, "
        "metacognition, language, executive control, and understanding of commitments "
        "[@premack1978; @flavell1979; @wimmerperner1983; @wellman2001; @tomasello2005]. The "
        "repository does not assume a fixed age window or a six-month relation to one Theory-of-Mind "
        "milestone. Developmental tasks must distinguish contingent attempts to change terms from "
        "requests, imitation, turn taking, and general verbal maturity."
    )
    text = replace_once(text, old_development, new_development, "paper developmental hypothesis")

    old_network = """### 10.7.4 Dynamic-network simulation

Agent-based models can test whether contingent cooperation, reputation, partner choice, and rewiring improve outcomes under specified network conditions [@wattsstrogatz1998; @nowak2006; @rand2011]. Such results would evaluate a formal strategy, not validate the psychological construct or the Hexure brand.

**Prerequisite:** strategies, topology, mutation, noise, payoff structure, rewiring costs, seeds, and benchmark models must be preregistered.

**Disconfirmation condition:** if performance depends on tuned assumptions, disappears under sensitivity analysis, or fails to improve on simpler strategies out of sample, the claimed application advantage is rejected.
"""
    new_network = """### 10.7.4 Dynamic-network simulation

Agent-based models can test whether contingent cooperation, reputation, partner choice, and rewiring improve outcomes under specified network conditions [@wattsstrogatz1998; @nowak2006; @rand2011]. Such results would evaluate a formal strategy, not validate the psychological construct or the Hexure brand.

A complete protocol is maintained separately at [`../simulations/hexure_ipd_protocol.md`](../simulations/hexure_ipd_protocol.md). It specifies the Iterated Prisoner's Dilemma payoff matrix, seven strategies, costly dynamic rewiring, noisy reputation, defector invasion, frequency dependence, mechanism ablations, held-out robustness environments, run-level inference, and adverse outcomes such as exclusion, false sanction, and concentration [@rapoport1965; @osbornerubinstein1994; @cohen1988; @wasserstein2016]. No simulation results have yet been reported.

**Prerequisite:** strategies, topology, mutation, noise, payoff structure, rewiring costs, seeds, benchmark models, primary outcomes, and rejection rules must be preregistered before confirmatory runs.

**Disconfirmation condition:** if performance depends on tuned assumptions, disappears under sensitivity analysis, fails to improve on simpler strategies out of sample, or produces unacceptable exclusion or power concentration, the claimed application advantage is rejected.
"""
    return replace_once(text, old_network, new_network, "paper network-simulation section")


def transform_threat_review(text: str) -> str:
    old_dynamic = (
        "Walter Cannon's account of bodily mobilisation under threat remains historically important "
        "[@cannon1915]. Modern research, however, does not support a simple menu of three mutually "
        "exclusive responses. Defensive behaviour varies with threat distance, escape availability, "
        "prior learning, environmental affordances, and the perceived cost of action "
        "[@fanselow1994; @blanchard2001; @mobbs2007]."
    )
    new_dynamic = (
        "Walter Cannon's account of bodily mobilisation under threat remains historically important "
        "[@cannon1915]. Modern research, however, does not support a simple menu of three mutually "
        "exclusive responses. Expanded stress-response lists and defence-cascade models are themselves "
        "heuristics rather than evidence for neatly separated modules [@bracha2004; @kozlowska2015]. "
        "Defensive behaviour varies with threat distance, escape availability, prior learning, "
        "environmental affordances, and the perceived cost of action "
        "[@fanselow1994; @blanchard2001; @mobbs2007]."
    )
    text = replace_once(text, old_dynamic, new_dynamic, "threat-review dynamic systems paragraph")

    old_polyvagal = """Polyvagal Theory offers an influential account linking autonomic state, safety, immobilisation, mobilisation, and social engagement [@porges2007; @porges2022]. It has also received serious criticism regarding its evolutionary narrative, anatomical premises, and interpretation of respiratory sinus arrhythmia [@grossmantaylor2007; @grossman2023].

The Demure Fulcrum does not require resolution of that dispute. The general proposition that autonomic regulation affects communication is compatible with many traditions. Specific claims about a uniquely mammalian ventral-vagal hierarchy should not be treated as established foundations for negotiation.
"""
    new_polyvagal = """Polyvagal Theory offers an influential account linking autonomic state, safety, immobilisation, mobilisation, and social engagement [@porges2007; @porges2022]. It has also received serious criticism regarding its evolutionary narrative, anatomical premises, and interpretation of respiratory sinus arrhythmia [@grossmantaylor2007; @taylor2015; @grossman2017; @grossman2023]. The critiques differ in scope, but together they justify treating the framework as contested rather than settled.

The Demure Fulcrum does not require resolution of that dispute. The general proposition that autonomic regulation affects communication is compatible with many traditions. Specific claims about a uniquely mammalian ventral-vagal hierarchy should not be treated as established foundations for negotiation. If those specific claims are revised or rejected, the functional distinction between choosing within a situation and attempting to transform its terms remains independently testable.
"""
    return replace_once(text, old_polyvagal, new_polyvagal, "threat-review Polyvagal section")


def transform_construct_review(text: str) -> str:
    old_study = """#### Study J: dynamic-network strategy comparison

Formalise a negotiation-inspired strategy independently of the Hexure name. Compare it with Always Defect, Tit-for-Tat, Generous Tit-for-Tat, Grim Trigger, Win-Stay-Lose-Shift, and partner-choice baselines across topology, noise, rewiring cost, and payoff regimes. Preregister seeds, primary outcomes, sensitivity analyses, and out-of-sample replications. A tuned win under one parameter set is not evidence of general superiority.
"""
    new_study = """#### Study J: dynamic-network strategy comparison

Formalise a negotiation-inspired strategy independently of the Hexure name. Compare it with Always Defect, Always Cooperate, Tit-for-Tat, Generous Tit-for-Tat, Grim Trigger, Win-Stay-Lose-Shift, and partner-choice baselines across topology, noise, rewiring cost, information quality, and payoff regimes. Preregister seeds, primary outcomes, sensitivity analyses, adverse outcomes, and out-of-sample replications. A tuned win under one parameter set is not evidence of general superiority.

The current pre-registration-ready specification is [`../simulations/hexure_ipd_protocol.md`](../simulations/hexure_ipd_protocol.md). It treats run-level summaries as the inferential unit, includes mechanism ablations and held-out environments, and requires rejection when gains depend on unrealistic information, cost-free rewiring, exclusion, false sanction, or concentration.
"""
    return replace_once(text, old_study, new_study, "construct-review Study J")


def transform_hexure(text: str) -> str:
    old_heading = """### Simulation preregistration outline

A network simulation should be specified before results are observed:
"""
    new_heading = """### Simulation preregistration outline

A full protocol is available at [`../simulations/hexure_ipd_protocol.md`](../simulations/hexure_ipd_protocol.md). It converts the outline below into a versioned design with a neutral null hypothesis, exact strategy rules, non-zero rewiring cost, noisy and manipulable reputation, paired run-level comparisons, mechanism ablations, held-out environments, and explicit rejection conditions. No simulation results have yet been reported.

A network simulation should be specified before results are observed:
"""
    return replace_once(text, old_heading, new_heading, "Hexure simulation link")


def transform_review_response(text: str) -> str:
    correction = """## Correction: the supplied review separated fMRI and EEG

An earlier version of this response described the rejected proposal as “fMRI within 500 ms.” That summary was inaccurate. The supplied review used **fMRI for spatial activation and connectivity hypotheses** and **EEG for the separate 300–500 ms expertise and timing hypothesis**. The distinction between modalities is methodologically valid and is now recorded correctly.

The repository still does not predeclare a unique dlPFC/vmPFC/amygdala pattern, cortisol profile, or EEG time window as characteristic of a new response system. Those questions remain secondary to reliable behavioural definition and control conditions matched for language, effort, threat, and social interaction.

"""
    text = replace_once(text, "## Decision summary\n", correction + "## Decision summary\n", "review correction insertion")

    old_row = "| Measure fMRI differences within 500 ms | **Not accepted methodologically** | Conventional fMRI does not resolve a 300–500 ms process in the way implied. EEG/MEG may examine timing, but timing differences would show expertise-related processing, not automatically establish a new stress-response system. |"
    new_row = "| Separate spatial and temporal neurobiological hypotheses: fMRI for spatial mapping and EEG for 300–500 ms timing | **Methodological distinction accepted; exact predictions deferred** | The supplied review correctly separated the modalities; an earlier repository response conflated them. fMRI and EEG may later constrain mechanism, but no region, connectivity pattern, cortisol profile, or time window is treated as diagnostic before behavioural construct validation. |"
    text = replace_once(text, old_row, new_row, "review modality row")

    old_sim_row = "| Add agent-based network predictions for Hexure | **Accepted with modification** | A preregistration outline will compare named strategies, topology, rewiring rules, sensitivity, and resilience without assuming a 65% cooperation threshold or guaranteed superiority. |"
    new_sim_rows = """| Add agent-based network predictions for Hexure | **Accepted with modification** | A preregistration outline compares named strategies, topology, rewiring rules, sensitivity, resilience, exclusion, and concentration without assuming a 65% cooperation threshold or guaranteed superiority. |
| Add a pre-registration-ready IPD network protocol | **Accepted with methodological strengthening** | A standalone protocol now defines `NEG-v0.1`, costly rewiring, noisy reputation, defector invasion, frequency dependence, ablations, held-out conditions, run-level inference, stopping rules, and explicit rejection criteria. It tests a formal strategy, not the psychological framework. |"""
    text = replace_once(text, old_sim_row, new_sim_rows, "review simulation row")

    old_result = """- a preregistration outline for Hexure simulations;
- eight named limitations including single-author origin;
- updated review questions, README navigation, visual assets, changelog, CI asset tracking, and repository validation.
"""
    new_result = """- a preregistration outline and standalone formal protocol for Hexure-inspired simulations;
- eight named limitations including single-author origin;
- a correction distinguishing the review's fMRI spatial proposal from its EEG temporal proposal;
- a scalable SVG README banner, updated review questions, navigation, changelog, CI path tracking, and repository validation.
"""
    return replace_once(text, old_result, new_result, "review resulting changes")


BIB_ENTRIES = {
    "bracha2004": """@article{bracha2004,
  author = {Bracha, H. Stefan},
  title = {Freeze, Flight, Fight, Fright, Faint: Adaptationist Perspectives on the Acute Stress Response Spectrum},
  year = {2004},
  journal = {CNS Spectrums},
  volume = {9},
  number = {9},
  pages = {679--685},
  doi = {10.1017/S1092852900002006}
}
""",
    "grossman2017": """@article{grossman2017,
  author = {Grossman, Paul},
  title = {Comment on Polyvagal Theory: A Primer},
  year = {2017},
  journal = {Psychological Review},
  volume = {124},
  number = {4},
  pages = {496--500},
  doi = {10.1037/rev0000068}
}
""",
    "taylor2015": """@article{taylor2015,
  author = {Taylor, Emily N. and Lamb, Dana P. and Rule, Richard A.},
  title = {The Polyvagal Theory: A Critical Review},
  year = {2015},
  journal = {Journal of Humanistic Psychology},
  volume = {55},
  number = {5},
  pages = {584--596},
  doi = {10.1177/0022167814559423}
}
""",
    "rapoport1965": """@book{rapoport1965,
  author = {Rapoport, Anatol and Chammah, Albert M.},
  title = {Prisoner's Dilemma: A Study in Conflict and Cooperation},
  year = {1965},
  publisher = {University of Michigan Press}
}
""",
    "osbornerubinstein1994": """@book{osbornerubinstein1994,
  author = {Osborne, Martin J. and Rubinstein, Ariel},
  title = {A Course in Game Theory},
  year = {1994},
  publisher = {MIT Press}
}
""",
    "cohen1988": """@book{cohen1988,
  author = {Cohen, Jacob},
  title = {Statistical Power Analysis for the Behavioral Sciences},
  year = {1988},
  edition = {2},
  publisher = {Lawrence Erlbaum Associates}
}
""",
    "wasserstein2016": """@article{wasserstein2016,
  author = {Wasserstein, Ronald L. and Lazar, Nicole A.},
  title = {The ASA's Statement on p-Values: Context, Process, and Purpose},
  year = {2016},
  journal = {The American Statistician},
  volume = {70},
  number = {2},
  pages = {129--133},
  doi = {10.1080/00031305.2016.1154108}
}
""",
    "wellman2001": """@article{wellman2001,
  author = {Wellman, Henry M. and Cross, David and Watson, Julanne},
  title = {Meta-Analysis of Theory-of-Mind Development: The Truth about False Belief},
  year = {2001},
  journal = {Child Development},
  volume = {72},
  number = {3},
  pages = {655--684},
  doi = {10.1111/1467-8624.00304}
}
""",
    "wimmerperner1983": """@article{wimmerperner1983,
  author = {Wimmer, Heinz and Perner, Josef},
  title = {Beliefs about Beliefs: Representation and Constraining Function of Wrong Beliefs in Young Children's Understanding of Deception},
  year = {1983},
  journal = {Cognition},
  volume = {13},
  number = {1},
  pages = {103--128},
  doi = {10.1016/0010-0277(83)90004-5}
}
""",
}


def transform_bibliography(text: str) -> str:
    additions: list[str] = []
    for key, entry in BIB_ENTRIES.items():
        if re.search(rf"@[A-Za-z]+\s*\{{\s*{re.escape(key)}\s*,", text):
            continue
        additions.append(entry.rstrip())
    if not additions:
        return text
    return text.rstrip() + "\n\n" + "\n\n".join(additions) + "\n"


def build_changes() -> dict[str, str]:
    return {
        "paper/The_Demure_Fulcrum_Academic_Paper.md": transform_paper(
            read("paper/The_Demure_Fulcrum_Academic_Paper.md")
        ),
        "research/01_threat_response_and_regulation.md": transform_threat_review(
            read("research/01_threat_response_and_regulation.md")
        ),
        "research/02_construct_and_formal_model.md": transform_construct_review(
            read("research/02_construct_and_formal_model.md")
        ),
        "applications/hexure.md": transform_hexure(read("applications/hexure.md")),
        "reviews/2026-08-08-external-review-response.md": transform_review_response(
            read("reviews/2026-08-08-external-review-response.md")
        ),
        "references/references.bib": transform_bibliography(read("references/references.bib")),
    }


def validate_outputs(changes: dict[str, str]) -> None:
    paper = changes["paper/The_Demure_Fulcrum_Academic_Paper.md"]
    required_paper = (
        "../simulations/hexure_ipd_protocol.md",
        "@wimmerperner1983",
        "@wellman2001",
        "No simulation results have yet been reported.",
    )
    for phrase in required_paper:
        if phrase not in paper:
            raise RuntimeError(f"paper output lacks {phrase!r}")

    review = changes["reviews/2026-08-08-external-review-response.md"]
    for phrase in (
        "the supplied review separated fMRI and EEG",
        "Methodological distinction accepted; exact predictions deferred",
        "pre-registration-ready IPD network protocol",
    ):
        if phrase.lower() not in review.lower():
            raise RuntimeError(f"review response lacks {phrase!r}")

    bibliography = changes["references/references.bib"]
    for key in BIB_ENTRIES:
        if not re.search(rf"@[A-Za-z]+\s*\{{\s*{re.escape(key)}\s*,", bibliography):
            raise RuntimeError(f"bibliography lacks {key}")

    substantive = "\n".join(changes.values()).lower()
    for prohibited in (
        "is a fourth primary instinct",
        "is a hard-wired survival instinct",
        "provides quantitative validation",
        "constitutes quantitative validation",
    ):
        if prohibited in substantive:
            raise RuntimeError(f"prohibited positive claim introduced: {prohibited}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    changes = build_changes()
    validate_outputs(changes)

    if args.check:
        print("Simulation addendum preflight passed")
        for rel, content in changes.items():
            before = len(read(rel))
            print(f"- {rel}: {before:,} -> {len(content):,} characters")
        return 0

    for rel, content in changes.items():
        path = ROOT / rel
        path.write_text(content, encoding="utf-8")
        print(f"Updated {rel}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
