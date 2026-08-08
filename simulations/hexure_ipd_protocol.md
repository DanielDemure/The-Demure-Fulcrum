# Pre-registration Protocol: A Negotiation-Inspired Strategy in Dynamic Small-World IPD Networks

**Protocol version:** 0.1  
**Status:** design specification — no simulation results have been produced or examined  
**Scope:** formal application test, not psychological or clinical validation

## 1. Research question

Does a precisely specified negotiation-inspired strategy produce different payoff, cooperation, and resilience outcomes from established Iterated Prisoner's Dilemma strategies when agents can observe reputational information and alter network ties at a cost?

The protocol is intentionally neutral about the answer. It tests a formal strategy derived from selected Demure Fulcrum and Hexure ideas. It does **not** assume superiority and does not treat a positive result as evidence for a new biological stress-response system.

## 2. Confirmatory hypotheses

### H0 — No application-level advantage

After correction for multiple comparisons, the negotiation-inspired strategy does not improve mean payoff or network resilience relative to the strongest preregistered comparator across held-out conditions.

### H1 — Conditional application-level advantage

Under at least one preregistered environment with repeat interaction, noisy reputation, non-zero rewiring cost, and defector entry, the negotiation-inspired strategy improves both:

1. mean payoff per interaction; and
2. network resilience after shock,

relative to the strongest comparator, with an uncertainty interval excluding zero.

A gain in only one metric, a gain that disappears under modest sensitivity analysis, or a gain produced by excessive exclusion or power concentration is not sufficient to support H1.

## 3. Base game

**Game:** Iterated Prisoner's Dilemma (IPD)

| | Player B cooperates | Player B defects |
|---|---:|---:|
| **Player A cooperates** | `R = 3`, `R = 3` | `S = 0`, `T = 5` |
| **Player A defects** | `T = 5`, `S = 0` | `P = 1`, `P = 1` |

The ordering is `T > R > P > S`, and `2R > T + S`, so repeated mutual cooperation is collectively preferable to alternating exploitation [@rapoport1965; @osbornerubinstein1994].

**Temporal discount used in discounted-payoff sensitivity analysis:** `lambda_payoff = 0.95`.

Primary analyses use undiscounted realised payoff per interaction. Discounted results are secondary.

## 4. Initial network topology

**Model:** undirected Watts–Strogatz small-world network [@wattsstrogatz1998]

| Parameter | Primary value |
|---|---:|
| Nodes `N` | 500 |
| Mean degree `k` | 8 |
| Initial topology rewiring probability `beta_init` | 0.10 |
| Rounds `T_rounds` | 1,000 |
| Burn-in for steady-state summaries | rounds 1–100 |
| Independent repetitions | 100 per frozen condition |

`beta_init` controls construction of the initial Watts–Strogatz graph. It is distinct from **strategy-driven dynamic rewiring**, which occurs during the simulation.

Each undirected edge plays one simultaneous IPD interaction per round. With `N = 500` and `k = 8`, the initial graph contains approximately 2,000 edges. The exact computational budget must be benchmarked from the implementation; no runtime claim is preregistered.

## 5. Strategies

### 5.1 Always Defect (`ALLD`)

- defect every round;
- no memory;
- no partner-directed rewiring.

### 5.2 Always Cooperate (`ALLC`)

- cooperate every round;
- no memory;
- no partner-directed rewiring.

### 5.3 Tit-for-Tat (`TFT`)

- cooperate on the first move;
- then mirror the partner's previous move;
- memory depth: one interaction.

### 5.4 Generous Tit-for-Tat (`GTFT`)

- cooperate on the first move;
- after partner cooperation: cooperate;
- after partner defection: cooperate with probability `p_generous = 0.33`, otherwise defect;
- memory depth: one interaction.

### 5.5 Grim Trigger (`GRIM`)

- cooperate until a partner defects once;
- defect against that partner thereafter;
- partner-specific persistent memory.

### 5.6 Win-Stay, Lose-Shift (`WSLS`)

- repeat the previous action after outcomes `R` or `T`;
- switch after outcomes `S` or `P`;
- memory depth: one interaction.

### 5.7 Negotiation-inspired strategy (`NEG-v0.1`)

`NEG-v0.1` is an engineered strategy. Its name does not imply that it captures all human negotiation.

#### Action rule

- first interaction with a partner: cooperate;
- maintain the last three partner actions;
- tolerate at most one defection in the three-interaction window;
- if two or more defections occur in the current window, defect once as a bounded sanction;
- after the sanction, re-evaluate rather than entering permanent retaliation;
- when the partner returns to cooperation, resume cooperation on the next eligible move.

#### Reputation rule

For partner `j`, agent `i` maintains an exponentially weighted cooperation score:

```text
rep_i(j, t) = alpha * observed_cooperation(j, t)
              + (1 - alpha) * rep_i(j, t - 1)
```

Primary value: `alpha = 0.20`. Initial reputation: `0.50`.

Observed actions are flipped with probability `epsilon_obs = 0.05` in the primary noisy-information condition. Sensitivity values are `0.00`, `0.10`, and `0.20`.

#### Dynamic rewiring rule

Every `rewire_interval = 10` rounds:

1. identify the active neighbour with the lowest local reputation;
2. if its reputation is below `theta_trust = 0.60`, attempt to sever that edge;
3. pay `c_rewire = 1.0` payoff unit for a completed replacement;
4. select a non-neighbour from the eligible candidate set;
5. form one replacement edge so the focal agent's degree is preserved;
6. cooperate on the first move with the new partner as a conciliation/opening signal;
7. if no candidate is eligible, retain the current edge and record a failed rewiring attempt without cost.

#### Candidate-information variants

The primary condition uses a **noisy shared reputation directory** based on the mean of available local reports. The following ablations are mandatory:

- local information only;
- perfect shared reputation;
- no reputation information;
- shared reputation with strategic false reports.

This distinguishes any strategy effect from the value or unfairness of the information infrastructure itself.

## 6. Rewiring constraints and safeguards

- no self-loops;
- no duplicate edges;
- network degree changes must be logged;
- a severed partner may be selected again only after a `50`-round cooling period;
- candidate selection is random among eligible candidates unless an explicitly preregistered policy states otherwise;
- isolated nodes reconnect through a neutral random mechanism, not through privileged access to a known cooperator;
- all sanctions, failed rewirings, and mistaken exclusions are recorded.

## 7. Experimental conditions

### Condition A — Baseline mixed population

Compare:

1. six-strategy population without `NEG-v0.1`, each strategy assigned `1/6` of nodes;
2. seven-strategy population, each strategy assigned `1/7` of nodes.

No invasion occurs. Report rounds 101–1,000.

### Condition B — Defector invasion

Use the seven-strategy mixed population. At round 500, replace 10% of nodes selected uniformly at random with `ALLD` agents. Preserve the incoming edges of replaced nodes.

Primary shock outcomes:

- total payoff damage relative to the pre-shock trend;
- cooperation recovery time;
- post-shock network resilience;
- exclusion and false-sanction rates.

### Condition C — Monoculture resistance

Run each of the seven strategies as the initial monoculture. At round 500, replace 10% of nodes with `ALLD` agents.

This condition tests resilience but does not imply that monoculture is desirable. Report collapse, concentration, and exclusion alongside cooperation.

### Condition D — Frequency dependence

Set the `NEG-v0.1` population share to:

```text
1%, 5%, 10%, 25%, 50%, 75%, 100%
```

For shares below 100%, divide the remaining population equally among the six comparator strategies. This resolves the ambiguity of adding a `NEG` frequency on top of a population that already sums to 100%.

### Condition E — Mechanism ablations

Starting from the primary seven-strategy condition, remove one component at a time:

- no dynamic rewiring;
- no reputation;
- no bounded sanction;
- no conciliation first move;
- memory depth one instead of three;
- zero rewiring cost;
- doubled rewiring cost;
- local-only reputation;
- false-reporting shared reputation.

An advantage that vanishes under one mild implementation change must be reported as conditional rather than general.

### Condition F — Held-out robustness environments

Freeze a held-out set before confirmatory analysis. It must include at least:

- `N` in `{250, 1,000}`;
- `k` in `{4, 12}`;
- `beta_init` in `{0.01, 0.30}`;
- payoff matrices that preserve the Prisoner's Dilemma ordering but alter temptation strength;
- observation error in `{0.00, 0.10, 0.20}`;
- rewiring cost in `{0.0, 0.5, 1.0, 2.0}`;
- invasion rates in `{5%, 20%}`.

## 8. Outcome variables

### 8.1 Mean payoff per interaction (`MPA`)

Run-level mean realised payoff divided by the number of interactions. Report mean, median, dispersion, and lower-tail outcomes.

### 8.2 Mutual cooperation rate (`CR`)

Fraction of edge interactions producing mutual cooperation, reported as a time series and as a run-level summary after burn-in.

### 8.3 Network resilience index (`NRI`)

Ratio of cooperative edges at the final assessment window to cooperative edges in the pre-shock window. A cooperative edge is one with mutual cooperation in at least 80% of its last 50 interactions.

### 8.4 Recovery time (`RT`)

Rounds after invasion until the cooperation-rate rolling mean returns to within 5% of its pre-invasion mean and remains there for 25 consecutive rounds. Runs that never recover are right-censored.

### 8.5 Total shock damage (`TSD`)

Cumulative difference between observed post-invasion payoff and a forecast based only on the preregistered pre-invasion trend.

### 8.6 Exclusion rate (`ER`)

Fraction of agents or edges excluded through rewiring, stratified by actual partner behaviour.

### 8.7 False-sanction rate (`FSR`)

Fraction of sanctions or severed links directed at partners whose true cooperation rate exceeds the trust threshold.

### 8.8 Degree and influence concentration (`DIC`)

Report degree Gini coefficient, largest-component share, bridge centralisation, and whether trusted nodes accumulate disproportionate control.

### 8.9 Rewiring burden (`RB`)

Total rewiring cost, failed rewiring attempts, and edge churn per agent.

A strategy is not considered favourable when higher cooperation is purchased through severe exclusion, unbounded centralisation, or unsustainable rewiring cost.

## 9. Randomisation and reproducibility

- generate and publish the complete seed list before confirmatory runs;
- use common random numbers and matched initial graphs for paired comparisons where feasible;
- freeze configuration files and software commit before producing confirmatory results;
- record every parameter, library version, platform, and seed;
- store run-level results rather than only aggregated charts;
- mark all post hoc analyses as exploratory.

## 10. Statistical analysis plan

The independent unit for confirmatory inference is the **simulation run**, not the agent or edge.

### Primary contrasts

For each held-out condition, compare `NEG-v0.1` with the strongest comparator on:

1. `MPA`; and
2. `NRI` after invasion.

Use paired run-level differences when matched seeds and initial graphs are available. Report:

- mean and median difference;
- 95% bootstrap confidence interval;
- standardised effect size;
- Monte Carlo standard error.

Control family-wise error across the two primary outcomes and six comparator contrasts with the Holm procedure rather than interpreting uncorrected pairwise tests.

### Secondary analyses

- cooperation trajectories with uncertainty bands;
- recovery-time survival analysis with right censoring;
- distributional payoff and lower-tail risk;
- mechanism-ablation contrasts;
- frequency-response curves;
- interaction between strategy and observation error, rewiring cost, and topology.

Bounded cooperation rates should not be treated as normally distributed without diagnostics. Report effect sizes and uncertainty, not only p-values [@cohen1988; @wasserstein2016].

## 11. Repetition count and stopping rule

The initial confirmatory repetition count is 100 runs per frozen condition. Before comparing strategies, inspect only implementation diagnostics and Monte Carlo precision.

If the Monte Carlo standard error for either primary outcome exceeds a preregistered tolerance, increase **all affected conditions** to 300 runs. Do not increase only conditions that look promising. No optional stopping based on statistical significance is permitted.

## 12. Implementation tests required before execution

1. hand-verified payoff tests for every action pair;
2. deterministic strategy traces for fixed partner histories;
3. reputation-update tests with known sequences;
4. rewiring invariant tests for self-loops, duplicates, degree, and cost;
5. observation-error tests at `epsilon_obs = 0` and `1`;
6. invasion tests confirming exactly the specified replacement fraction;
7. replay tests confirming identical results from the same seed;
8. ablation tests confirming each mechanism is actually disabled;
9. export-schema tests for all primary outcomes;
10. a small end-to-end run whose totals can be independently recomputed.

## 13. Interpretation and rejection rules

The application-level advantage is rejected when any of the following occurs:

- `NEG-v0.1` does not improve both primary outcomes after multiplicity correction;
- the effect disappears in held-out environments;
- a simpler comparator performs equivalently within the uncertainty bounds;
- the effect depends on cost-free rewiring or unrealistically perfect information;
- gains are accompanied by materially worse exclusion, false sanction, or concentration;
- independent implementations do not reproduce the result.

A positive result supports only `NEG-v0.1` under the tested conditions. It does not establish the Demure Fulcrum as a psychological category, prove Hexure as an institution, or justify deployment in high-stakes settings.

## 14. Reporting template

Every report must include:

- protocol and code version;
- preregistration timestamp;
- full configuration and seed list;
- all exclusions and failed runs;
- primary and secondary outcomes;
- null and adverse findings;
- sensitivity and ablation results;
- computational resource use;
- deviations from protocol;
- a statement separating formal-strategy evidence from psychological inference.

## 15. Implementation note

Python with NetworkX or an agent-based framework such as Mesa is suitable, but the protocol does not require one library. Correctness, deterministic replay, and transparent configuration take priority over framework choice.

Future simulation software should be licensed explicitly as software. This protocol document remains part of the CC BY 4.0 scholarly repository.

## References

See the shared bibliography at [`../references/references.bib`](../references/references.bib).
