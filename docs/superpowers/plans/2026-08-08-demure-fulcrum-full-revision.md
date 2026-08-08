# The Demure Fulcrum Full Revision Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild the repository and working paper around negotiation as an agency-preserving higher-order meta-response under threat, with calibrated claims, defensible scholarly references, explicit falsifiability, separated applications, reproducible PDF generation, and review-ready repository metadata.

**Architecture:** Markdown remains the source of truth. The core paper contains the conceptual framework and research agenda; research companions provide deeper reviews and formalization; Hexure is isolated as a speculative application note. A single BibTeX database supports all scholarly documents, while repository QA checks claims, citations, paths, metadata, and generated PDF consistency before a pull request is opened.

**Tech Stack:** Markdown, Pandoc citation syntax, BibTeX, CSL/Pandoc citeproc, Bash, Python 3 standard library, CC BY 4.0, CFF 1.2.0, GitHub branches and pull requests, and a PDF engine selected from the tools available in the execution environment.

## Global Constraints

- The central claim must remain a higher-order agency-preserving meta-response, not a proven fourth autonomic reflex or hard-wired instinct.
- The main title is `The Demure Fulcrum: Negotiation as an Agency-Preserving Meta-Response Under Threat`.
- The paper must display `A Conceptual Framework and Research Agenda — Working Paper, Not Peer Reviewed`.
- Interpersonal or institutional negotiation is the strict construct; intrapersonal and existential negotiation are explicitly labelled conceptual extensions.
- Negotiation is not defined as necessarily calm, ethical, cooperative, or win-win.
- Appeasement is not treated as moral failure, and victim-blaming language is prohibited.
- Polyvagal Theory may be discussed only as a contested, non-essential interpretation.
- Cultural works are illustrations of meaning and agency, not biological evidence.
- Hexure, trading, OMAD, radical transparency, the Knight's Oath, and Cathedral Building must not appear as validation of the core theory.
- Popular sources must not support scientific propositions.
- No DOI, peer-review, empirical-validation, or release claim may be added unless it is true at execution time.
- Work remains on `revision/agency-meta-response`; do not merge into `main` without Daniel Demure's explicit approval.

---

### Task 1: Establish the local revision workspace and source inventory

**Files:**
- Read: all tracked repository files on `revision/agency-meta-response`
- Create locally: a revision workspace mirroring the branch
- Preserve: `assets/demure_fulcrum_symbol.png`

**Interfaces:**
- Consumes: approved design at `docs/superpowers/specs/2026-08-08-demure-fulcrum-revision-design.md`
- Produces: an exact inventory of files to replace, create, retain, and delete, plus the current branch head used for all later commits

- [ ] **Step 1: Clone and select the revision branch**

```bash
git clone https://github.com/DanielDemure/The-Demure-Fulcrum.git /mnt/data/The-Demure-Fulcrum
git -C /mnt/data/The-Demure-Fulcrum fetch origin revision/agency-meta-response
git -C /mnt/data/The-Demure-Fulcrum checkout -B revision/agency-meta-response origin/revision/agency-meta-response
```

Expected: the working tree contains the original paper, three original research files, the symbol image, the approved design, and this plan.

- [ ] **Step 2: Record the baseline**

```bash
git -C /mnt/data/The-Demure-Fulcrum status --short
git -C /mnt/data/The-Demure-Fulcrum log --oneline --decorate -5
find /mnt/data/The-Demure-Fulcrum -maxdepth 4 -type f | sort
```

Expected: a clean worktree and `revision/agency-meta-response` at the design/plan commits.

- [ ] **Step 3: Create the target directories**

```bash
mkdir -p /mnt/data/The-Demure-Fulcrum/{applications,provenance,references,scripts}
```

- [ ] **Step 4: Confirm the change boundary**

Retain the image and Git history. Replace the README and paper source, replace the three research documents with the new names, create repository metadata and QA/build files, regenerate the PDF, and delete only the three obsolete research paths.

- [ ] **Step 5: Commit only if workspace scaffolding is tracked**

No empty directories are committed. This task should ordinarily produce no repository commit.

---

### Task 2: Build and verify the scholarly source pack

**Files:**
- Create: `references/references.bib`
- Create: `provenance/README.md`
- Create locally: `references/source-audit.tsv` for execution evidence; do not commit unless it adds lasting value

**Interfaces:**
- Consumes: claims and evidence needs from the approved design
- Produces: stable BibTeX keys used by the paper and companion documents, with verified authors, titles, years, venues, DOI or canonical publisher URLs

- [ ] **Step 1: Define evidence groups**

Create source groups for: defense cascade and threat systems; appraisal, control, coping, and agency; acute stress and executive regulation; negotiation and bargaining; appeasement and socially mediated threat responses; cooperation, reciprocity, and social networks; anthropology; metacognition and social cognition; and the Polyvagal debate.

- [ ] **Step 2: Verify every candidate against a primary or publisher record**

For each source, record:

```text
bibkey	authors	year	title	venue	doi_or_canonical_url	claim_supported	verification_status
```

Expected: no entry sourced only from Wikipedia, commercial blogs, social media, generic film lists, or an aggregator when a primary record exists.

- [ ] **Step 3: Write `references/references.bib`**

Use consistent keys such as `cannon1915`, `kozlowska2015`, `ledoux2016`, `lazarus1984`, `buhle2014`, `taylor2000`, `nash1950`, `trivers1971`, and `grossman2023`. Include DOI fields where verified and avoid duplicate records.

- [ ] **Step 4: Write the provenance note**

`provenance/README.md` must identify Daniel Demure's December 2025 foundational notes as the origin of the concept, state that author-origin material establishes provenance rather than independent validation, and explain that Git history preserves the January 2026 version.

- [ ] **Step 5: Run bibliography integrity checks**

```bash
python - <<'PY'
from pathlib import Path
import re
text = Path('/mnt/data/The-Demure-Fulcrum/references/references.bib').read_text()
keys = re.findall(r'@[A-Za-z]+\s*\{\s*([^,\s]+)', text)
assert keys, 'No BibTeX entries found'
assert len(keys) == len(set(keys)), 'Duplicate BibTeX keys found'
for banned in ('wikipedia.org', 'investopedia.com', 'reddit.com', 'pinterest.com', 'example.com'):
    assert banned not in text.lower(), f'Banned source remains: {banned}'
print(f'{len(keys)} unique bibliography entries')
PY
```

Expected: unique keys and no banned source domains.

- [ ] **Step 6: Commit the evidence foundation**

```bash
git add references/references.bib provenance/README.md
git commit -m "docs: rebuild scholarly evidence foundation"
```

---

### Task 3: Rewrite the main working paper

**Files:**
- Replace: `paper/The_Demure_Fulcrum_Academic_Paper.md`

**Interfaces:**
- Consumes: verified BibTeX keys from Task 2
- Produces: the canonical conceptual paper used by README, PDF, citation metadata, and companion documents

- [ ] **Step 1: Add document metadata and status**

Use Pandoc-compatible YAML containing the revised title, Daniel Demure as author, the revision date, `references/references.bib`, and a prominent working-paper/not-peer-reviewed notice.

- [ ] **Step 2: Write the abstract and contribution statement**

The abstract must state that the paper proposes a conceptual meta-response, does not establish a fourth autonomic reflex, defines strict negotiation by attempts to alter constraints/options/payoffs, and presents testable predictions and a research programme.

- [ ] **Step 3: Write the levels-of-analysis and construct-definition sections**

Separate physiological state, defensive behaviour, higher-order response policy, and institutional application. Define strict negotiation using the seven criteria in the approved design and explain `G → G′` in plain language before any notation.

- [ ] **Step 4: Write boundary conditions and typology**

State when negotiation is possible, impaired, or conceptually inapplicable. Distinguish strict interpersonal/institutional negotiation from intrapersonal and existential extensions.

- [ ] **Step 5: Differentiate adjacent constructs**

Provide a careful comparison with fight, flight, freeze, appeasement/fawn, tend-and-befriend, cognitive reappraisal, problem-focused coping, assertiveness, social approach, and general negotiation skill. Include a table with observable indicators and avoid invented biomarkers.

- [ ] **Step 6: Rebuild the evidence sections**

Use calibrated language: evidence may motivate, constrain, or support the framework but does not validate a unique biological system. Remove triune-brain language and describe cognition and emotion as interacting networks. Treat Polyvagal Theory as contested and non-essential.

- [ ] **Step 7: Add formal model, predictions, rivals, and research programme**

Include the negotiability effect, incremental validity, negotiation–appeasement dissociation, and stress-regulation interaction. Add explicit disconfirmation criteria and staged studies beginning with construct development and behavioural experiments before physiology or neuroimaging.

- [ ] **Step 8: Reframe cultural and ethical material**

Keep a concise section on Lieutenant Dan, Orpheus, Kafka, Dostoevsky, and existential bargaining only as interpretive illustrations. Separate descriptive negotiation from ethical commitments and coercive bargaining.

- [ ] **Step 9: Add limitations and conclusion**

Acknowledge conceptual novelty, overlap risk, Western terminology, limited direct evidence, measurement challenges, power asymmetry, and the possibility that the construct adds no incremental validity. End with a research invitation rather than a claim of proof.

- [ ] **Step 10: Run claim-language and citation checks**

```bash
python - <<'PY'
from pathlib import Path
import re
p = Path('/mnt/data/The-Demure-Fulcrum/paper/The_Demure_Fulcrum_Academic_Paper.md')
text = p.read_text()
banned = [
    'fourth primary instinct', 'hard-wired survival instinct', 'reptilian brain',
    'grand unified theory', 'quantitative validation', 'proves that negotiation'
]
for phrase in banned:
    assert phrase.lower() not in text.lower(), phrase
assert 'Working Paper' in text and 'Not Peer Reviewed' in text
assert 'Disconfirmation' in text or 'disconfirmation' in text
assert len(re.findall(r'\[@[^\]]+\]', text)) >= 20, 'Too few scholarly citations'
print(len(text.split()), 'words')
PY
```

Expected: no prohibited claims, explicit status and falsifiability, and substantial scholarly citation coverage.

- [ ] **Step 11: Commit the rewritten framework**

```bash
git add paper/The_Demure_Fulcrum_Academic_Paper.md
git commit -m "docs: reconstruct Demure Fulcrum framework"
```

---

### Task 4: Replace the research companions and isolate Hexure

**Files:**
- Create: `research/01_threat_response_and_regulation.md`
- Create: `research/02_construct_and_formal_model.md`
- Create: `research/03_cultural_and_philosophical_illustrations.md`
- Create: `applications/hexure.md`
- Delete: `research/01_psychological_foundations.md`
- Delete: `research/02_philosophical_evolutionary.md`
- Delete: `research/03_cultural_manifestations.md`

**Interfaces:**
- Consumes: the main paper's definitions and citation keys
- Produces: deeper material without reintroducing unsupported claims into the core paper

- [ ] **Step 1: Write the threat-response review**

Cover defense cascades, appraisal, controllability, active coping, acute stress effects on executive function, social threat responses, and the limits of simple fight-flight-freeze lists. End with direct implications and non-implications for the Demure Fulcrum.

- [ ] **Step 2: Write the construct and formal-model companion**

Expand strict inclusion/exclusion rules, present the `G → G′` formalization, define observable coding dimensions, list rival hypotheses, outline scale-development steps, and specify behavioural experimental designs and analysis plans.

- [ ] **Step 3: Write the cultural and philosophical companion**

Separate primary works, interpretive claims, and empirical claims. Explain why recurring cultural bargaining motifs illuminate human meaning-making but cannot demonstrate a distinct stress-response system.

- [ ] **Step 4: Write the Hexure application note**

Label Hexure `Speculative Application Note — Not Empirically Validated`. Separate network-science inspiration, strategic intermediation, ethical doctrine, Cathedral Building, and personal anecdotes. The twenty-trade example, if retained, must be explicitly non-generalizable and incapable of causal validation.

- [ ] **Step 5: Delete obsolete companions**

```bash
rm research/01_psychological_foundations.md \
   research/02_philosophical_evolutionary.md \
   research/03_cultural_manifestations.md
```

- [ ] **Step 6: Verify conceptual consistency**

```bash
grep -RniE 'fourth primary instinct|hard-wired|reptilian brain|quantitative validation|grand unified theory' research applications && exit 1 || true
```

Expected: no prohibited claims.

- [ ] **Step 7: Commit the companion architecture**

```bash
git add research applications
git commit -m "docs: separate research companions and Hexure application"
```

---

### Task 5: Rebuild repository metadata, navigation, licensing, and review guidance

**Files:**
- Replace: `README.md`
- Create: `CITATION.cff`
- Create: `LICENSE`
- Create: `CHANGELOG.md`
- Create: `REVIEW_GUIDE.md`
- Create: `CONTRIBUTING.md`

**Interfaces:**
- Consumes: final titles, paths, status, and scope from Tasks 3–4
- Produces: a coherent public entry point and citation/review contract

- [ ] **Step 1: Rewrite README**

Include the symbol, calibrated description, status banner, key concept, strict and extended uses, repository map, evidence status, limitations, review invitation, citation link, licence, and PDF/build links. Remove the unverifiable Frankl attribution.

- [ ] **Step 2: Add `CITATION.cff`**

Use CFF 1.2.0, Daniel Demure as author, the revised title, repository URL, revision date, CC BY 4.0 licence identifier, and a preferred citation for the working paper. Do not invent a DOI or published version.

- [ ] **Step 3: Add CC BY 4.0 licence**

Use the official Creative Commons Attribution 4.0 International legal code or the standard repository licence text and make clear that future software may use a separate licence.

- [ ] **Step 4: Add changelog and review guidance**

`CHANGELOG.md` documents the unreleased scholarly reconstruction. `REVIEW_GUIDE.md` asks reviewers about construct distinctiveness, boundary conditions, rival explanations, measurement validity, cultural scope, and evidentiary overreach. `CONTRIBUTING.md` explains issues, evidence proposals, corrections, and respectful review.

- [ ] **Step 5: Check all local README links**

```bash
python - <<'PY'
from pathlib import Path
import re
root = Path('/mnt/data/The-Demure-Fulcrum')
text = (root/'README.md').read_text()
for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)', text):
    if '://' in target or target.startswith('#'):
        continue
    path = (root / target.split('#', 1)[0]).resolve()
    assert path.exists(), f'Broken local link: {target}'
print('README local links pass')
PY
```

- [ ] **Step 6: Validate CFF YAML**

```bash
python - <<'PY'
from pathlib import Path
try:
    import yaml
except ImportError:
    raise SystemExit('PyYAML is required for this validation run')
data = yaml.safe_load(Path('/mnt/data/The-Demure-Fulcrum/CITATION.cff').read_text())
assert data['cff-version'] == '1.2.0'
assert data['title'].startswith('The Demure Fulcrum')
assert data['authors'][0]['family-names'] == 'Demure'
print('CITATION.cff parses')
PY
```

- [ ] **Step 7: Commit repository metadata**

```bash
git add README.md CITATION.cff LICENSE CHANGELOG.md REVIEW_GUIDE.md CONTRIBUTING.md
git commit -m "docs: rebuild repository metadata and review guidance"
```

---

### Task 6: Add reproducible QA/build tooling and regenerate the PDF

**Files:**
- Create: `scripts/validate_repo.py`
- Create: `paper/build.sh`
- Replace: `paper/The_Demure_Fulcrum_Academic_Paper.pdf`

**Interfaces:**
- Consumes: all final Markdown, BibTeX, metadata, and repository paths
- Produces: deterministic validation output and a readable PDF matching the Markdown source

- [ ] **Step 1: Implement `scripts/validate_repo.py`**

The script must use the Python standard library to check required paths, prohibited phrases, Markdown citation keys against BibTeX keys, duplicate BibTeX keys, local README links, placeholder domains, document status, limitations/falsification headings, and absence of stale research filenames.

- [ ] **Step 2: Verify the validator catches a controlled failure**

```bash
cp README.md /tmp/README.md.backup
printf '\n[broken](missing-file.md)\n' >> README.md
python scripts/validate_repo.py; test $? -ne 0
mv /tmp/README.md.backup README.md
```

Expected: the first run fails on the broken link.

- [ ] **Step 3: Run the validator on the real repository**

```bash
python scripts/validate_repo.py
```

Expected: exit code 0 with a concise summary of checks and citation counts.

- [ ] **Step 4: Implement `paper/build.sh`**

The script must resolve the repository root, require Pandoc, select an available PDF engine, invoke Pandoc with citeproc and the shared bibliography, fail clearly when dependencies are unavailable, and write `paper/The_Demure_Fulcrum_Academic_Paper.pdf`.

- [ ] **Step 5: Build the PDF**

```bash
bash paper/build.sh
file paper/The_Demure_Fulcrum_Academic_Paper.pdf
pdfinfo paper/The_Demure_Fulcrum_Academic_Paper.pdf
pdftotext paper/The_Demure_Fulcrum_Academic_Paper.pdf - | head -40
```

Expected: a valid PDF with selectable text, revised title, working-paper status, page count, and no build errors.

- [ ] **Step 6: Visually inspect every PDF page**

Render the full PDF to PNG pages and inspect for clipped tables, orphaned headings, bad margins, missing references, broken symbols, and unreadable text.

- [ ] **Step 7: Confirm source/PDF agreement**

Check that title, abstract opening, all top-level headings, final limitation statement, and reference count appear in both Markdown and extracted PDF text.

- [ ] **Step 8: Commit tooling and PDF**

```bash
git add scripts/validate_repo.py paper/build.sh paper/The_Demure_Fulcrum_Academic_Paper.pdf
git commit -m "build: add validation and regenerate working paper PDF"
```

---

### Task 7: Final verification, publish branch commits, and open the pull request

**Files:**
- Modify if required by QA: any file within the approved scope
- Create on GitHub: pull request from `revision/agency-meta-response` to `main`

**Interfaces:**
- Consumes: complete branch from Tasks 1–6
- Produces: a verified, reviewable pull request that is not merged

- [ ] **Step 1: Run final repository validation**

```bash
python scripts/validate_repo.py
bash paper/build.sh
git status --short
git diff --check origin/main...HEAD
git grep -niE 'example\.com|Wikipedia|Investopedia|Reddit|Pinterest|TikTok|fourth primary instinct|hard-wired survival instinct|reptilian brain|quantitative validation' -- ':!docs/superpowers/**'
```

Expected: validator and build pass, no whitespace errors, clean working tree after rebuild, and no prohibited evidentiary material.

- [ ] **Step 2: Review the complete branch diff**

```bash
git diff --stat origin/main...HEAD
git diff --name-status origin/main...HEAD
git log --oneline origin/main..HEAD
```

Expected: only approved files changed; obsolete research files are deleted; symbol image is unchanged.

- [ ] **Step 3: Synchronize the verified local files to GitHub**

Use GitHub's blob/tree/commit APIs so text and the binary PDF are committed exactly as validated. Preserve coherent commit groups where possible and move only `revision/agency-meta-response`.

- [ ] **Step 4: Compare remote branch to `main`**

Confirm changed filenames and commit counts through the GitHub connector. Fetch representative files from the remote branch and verify their hashes or exact content against the local validated copies.

- [ ] **Step 5: Open the pull request**

Title:

```text
Reconstruct The Demure Fulcrum as an agency-preserving meta-response framework
```

Body must summarize the calibrated claim, paper rewrite, evidence rebuild, explicit falsifiability, separated Hexure note, repository metadata, generated PDF, validation performed, remaining empirical limitations, and the fact that no peer review or empirical validation is claimed.

- [ ] **Step 6: Inspect the pull request**

Confirm base `main`, head `revision/agency-meta-response`, expected changed files, readable diff, and no accidental merge.

- [ ] **Step 7: Report completion with evidence**

Provide the PR number, branch, key commits, validation commands and outcomes, PDF page count, source count, changed-file summary, and any truthful residual limitation. Do not claim completion until all checks above have passed.
