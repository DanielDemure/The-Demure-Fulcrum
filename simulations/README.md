# Simulation Programme

**Status:** protocol and implementation roadmap — no simulation results have been produced or reported.

This directory separates computational testing of a **formal negotiation-inspired strategy** from empirical testing of the Demure Fulcrum as a psychological construct.

## Current protocol

- [`hexure_ipd_protocol.md`](hexure_ipd_protocol.md) — pre-registration-ready specification for comparing a negotiation-inspired strategy with established strategies in dynamic Iterated Prisoner's Dilemma networks.

The protocol defines:

- the payoff matrix and temporal horizon;
- Watts–Strogatz initial network construction;
- seven comparison strategies;
- memory, reputation, sanction, conciliation, and rewiring rules;
- baseline, invasion, monoculture, frequency-dependence, and ablation conditions;
- outcome variables covering payoff, cooperation, resilience, exclusion, false sanction, and concentration;
- analysis, multiplicity control, sensitivity analysis, and stopping rules;
- explicit conditions under which the application-level advantage should be rejected.

## Interpretation boundary

A simulation can establish only that a specified algorithm performs in a specified model under specified assumptions. It cannot by itself show that:

- humans possess a fourth autonomic stress response;
- the Demure Fulcrum is a distinct psychological latent variable;
- Hexure is a validated organisational architecture;
- reputation systems are fair, safe, or resistant to manipulation;
- the same strategy will work in markets, diplomacy, trauma, or institutions.

The protocol therefore treats the simulation as a test of an **application hypothesis**, not as validation of the core theory.

## Planned implementation layout

A future implementation should use a structure similar to:

```text
simulations/
├── README.md
├── hexure_ipd_protocol.md
├── pyproject.toml                 # future code dependencies and tooling
├── src/demure_sim/                # future implementation
├── configs/                       # frozen preregistered conditions
├── tests/                         # deterministic unit and property tests
└── results/                       # generated locally; not committed by default
```

## Implementation acceptance criteria

Before any result is interpreted, an implementation should demonstrate:

1. deterministic replay from recorded random seeds;
2. correct payoff accounting on hand-checkable two-agent examples;
3. degree and edge-count invariants before and after rewiring;
4. explicit treatment of rewiring cost and failed rewiring attempts;
5. reputation updates that match worked examples;
6. isolated ablation tests for reputation, rewiring, tolerance, and conciliation;
7. identical initial networks and seeds for paired strategy comparisons where appropriate;
8. export of configuration, code version, environment, seeds, and raw run-level summaries;
9. publication of null, adverse, and sensitivity results;
10. no retrospective redefinition of the primary outcome after observing results.

## Contribution

Implementation contributions are welcome. Read [`../CONTRIBUTING.md`](../CONTRIBUTING.md) first. A pull request should include tests, frozen configuration files, reproducibility instructions, and a clear separation between preregistered and exploratory analyses.

Protocol text is covered by the repository's CC BY 4.0 licence. Future software should declare a separate software licence explicitly.
