#!/usr/bin/env python3
"""Validate repository structure, scholarly citations, links, and generated PDF."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "README.md",
    "CITATION.cff",
    "LICENSE",
    "CHANGELOG.md",
    "REVIEW_GUIDE.md",
    "CONTRIBUTING.md",
    "paper/The_Demure_Fulcrum_Academic_Paper.md",
    "references/references.bib",
    "research/01_threat_response_and_regulation.md",
    "research/02_construct_and_formal_model.md",
    "research/03_cultural_and_philosophical_illustrations.md",
    "applications/hexure.md",
    "provenance/README.md",
    "scripts/build_pdf.py",
]

BANNED_DOMAINS = {
    "wikipedia.org",
    "investopedia.com",
    "reddit.com",
    "pinterest.com",
    "tiktok.com",
    "facebook.com",
    "example.com",
    "verywellmind.com",
    "psychologytoday.com",
}

PROHIBITED_POSITIVE_CLAIMS = [
    r"is a fourth primary instinct",
    r"is a hard[- ]wired survival instinct",
    r"provides quantitative validation",
    r"constitutes quantitative validation",
    r"grand unified theory of agency",
    r"the reptilian brain",
]

OLD_RESEARCH = [
    "research/01_psychological_foundations.md",
    "research/02_philosophical_evolutionary.md",
    "research/03_cultural_manifestations.md",
]


def parse_bib_keys(text: str) -> set[str]:
    return set(re.findall(r"@[A-Za-z]+\s*\{\s*([^,\s]+)", text))


def markdown_files() -> list[Path]:
    paths = []
    for path in ROOT.rglob("*.md"):
        rel = path.relative_to(ROOT).as_posix()
        if rel.startswith("docs/superpowers/"):
            continue
        paths.append(path)
    return paths


def check_required() -> list[str]:
    errors = []
    for rel in REQUIRED:
        if not (ROOT / rel).exists():
            errors.append(f"missing required file: {rel}")
    return errors


def check_claim_language() -> list[str]:
    errors = []
    targets = markdown_files()
    for path in targets:
        text = path.read_text(encoding="utf-8")
        for pattern in PROHIBITED_POSITIVE_CLAIMS:
            if re.search(pattern, text, flags=re.IGNORECASE):
                errors.append(f"prohibited positive claim in {path.relative_to(ROOT)}: {pattern}")
    return errors


def check_bibliography() -> tuple[list[str], set[str]]:
    errors: list[str] = []
    path = ROOT / "references" / "references.bib"
    if not path.exists():
        return ["bibliography missing"], set()
    text = path.read_text(encoding="utf-8")
    keys = re.findall(r"@[A-Za-z]+\s*\{\s*([^,\s]+)", text)
    if not keys:
        errors.append("no BibTeX entries found")
    if len(keys) != len(set(keys)):
        errors.append("duplicate BibTeX keys found")
    lowered = text.lower()
    for domain in BANNED_DOMAINS:
        if domain in lowered:
            errors.append(f"weak or prohibited bibliography domain: {domain}")
    for key in keys:
        block_match = re.search(
            rf"@[A-Za-z]+\s*\{{\s*{re.escape(key)}\s*,(.*?)(?=\n@|\Z)",
            text,
            flags=re.DOTALL,
        )
        block = block_match.group(1) if block_match else ""
        for field in ("author", "title", "year"):
            if not re.search(rf"\b{field}\s*=", block, flags=re.IGNORECASE):
                errors.append(f"BibTeX entry {key} lacks {field}")
    return errors, set(keys)


def check_citations(bib_keys: set[str]) -> list[str]:
    errors = []
    cited: set[str] = set()
    for path in markdown_files():
        text = path.read_text(encoding="utf-8")
        cited.update(re.findall(r"(?<![A-Za-z0-9])@([A-Za-z0-9_:\-.]+)", text))
    missing = sorted(cited - bib_keys)
    if missing:
        errors.append("missing bibliography keys: " + ", ".join(missing))
    main = (ROOT / "paper" / "The_Demure_Fulcrum_Academic_Paper.md").read_text(encoding="utf-8")
    main_keys = set(re.findall(r"(?<![A-Za-z0-9])@([A-Za-z0-9_:\-.]+)", main))
    if len(main_keys) < 25:
        errors.append(f"main paper has only {len(main_keys)} unique scholarly citations; expected at least 25")
    return errors


def local_links(text: str) -> list[str]:
    links = []
    for raw in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
        target = raw.split("#", 1)[0].strip()
        if not target or target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        links.append(unquote(target))
    return links


def check_links() -> list[str]:
    errors = []
    for path in markdown_files():
        text = path.read_text(encoding="utf-8")
        for target in local_links(text):
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                errors.append(f"link escapes repository in {path.relative_to(ROOT)}: {target}")
                continue
            if not resolved.exists():
                errors.append(f"broken local link in {path.relative_to(ROOT)}: {target}")
    return errors


def check_main_structure() -> list[str]:
    errors = []
    path = ROOT / "paper" / "The_Demure_Fulcrum_Academic_Paper.md"
    if not path.exists():
        return ["main paper missing"]
    text = path.read_text(encoding="utf-8")
    required_phrases = [
        "Working Paper, Not Peer Reviewed",
        "Levels of Analysis",
        "Operational Definition",
        "Boundary Conditions",
        "Differentiation from Adjacent Constructs",
        "Formal Model",
        "Testable Predictions",
        "Disconfirmation Criteria",
        "Empirical Research Programme",
        "Limitations",
        "References",
    ]
    for phrase in required_phrases:
        if phrase.lower() not in text.lower():
            errors.append(f"main paper missing required section or status: {phrase}")
    if "<!-- FIGURE:FULCRUM -->" not in text:
        errors.append("main paper lacks reproducible fulcrum figure marker")
    word_count = len(re.findall(r"\b\w+[\w'-]*\b", text))
    if word_count < 4500:
        errors.append(f"main paper is unexpectedly short: {word_count} words")
    return errors


def check_cff() -> list[str]:
    errors = []
    path = ROOT / "CITATION.cff"
    if not path.exists():
        return ["CITATION.cff missing"]
    text = path.read_text(encoding="utf-8")
    for phrase in (
        "cff-version: 1.2.0",
        "Daniel",
        "Demure",
        "CC-BY-4.0",
        "preferred-citation:",
        "repository-code:",
    ):
        if phrase not in text:
            errors.append(f"CITATION.cff lacks: {phrase}")
    if re.search(r"\bdoi:\s*\S+", text, flags=re.IGNORECASE):
        errors.append("CITATION.cff contains a DOI although none has been assigned")
    try:
        import yaml  # type: ignore

        data = yaml.safe_load(text)
        if not isinstance(data, dict):
            errors.append("CITATION.cff does not parse to a mapping")
    except ImportError:
        pass
    except Exception as exc:  # pragma: no cover - parser detail
        errors.append(f"CITATION.cff YAML error: {exc}")
    return errors


def check_old_paths() -> list[str]:
    errors = []
    for rel in OLD_RESEARCH:
        if (ROOT / rel).exists():
            errors.append(f"obsolete research file still present: {rel}")
    return errors


def check_pdf(skip_pdf: bool) -> list[str]:
    if skip_pdf:
        return []
    errors = []
    path = ROOT / "paper" / "The_Demure_Fulcrum_Academic_Paper.pdf"
    if not path.exists():
        return ["generated PDF missing"]
    data = path.read_bytes()
    if not data.startswith(b"%PDF-"):
        errors.append("generated PDF has invalid signature")
    if len(data) < 20_000:
        errors.append(f"generated PDF is unexpectedly small: {len(data)} bytes")
    try:
        from pypdf import PdfReader  # type: ignore

        reader = PdfReader(str(path))
        if len(reader.pages) < 12:
            errors.append(f"generated PDF has only {len(reader.pages)} pages")
        first_pages = "\n".join((page.extract_text() or "") for page in reader.pages[:3])
        if "Not Peer Reviewed" not in first_pages:
            errors.append("working-paper status not extractable from opening PDF pages")
        metadata = reader.metadata or {}
        if "Demure Fulcrum" not in str(metadata.get("/Title", "")):
            errors.append("PDF title metadata is incomplete")
    except ImportError:
        pass
    except Exception as exc:
        errors.append(f"PDF parse error: {exc}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-pdf", action="store_true")
    args = parser.parse_args()

    errors: list[str] = []
    errors.extend(check_required())
    errors.extend(check_claim_language())
    bib_errors, bib_keys = check_bibliography()
    errors.extend(bib_errors)
    errors.extend(check_citations(bib_keys))
    errors.extend(check_links())
    errors.extend(check_main_structure())
    errors.extend(check_cff())
    errors.extend(check_old_paths())
    errors.extend(check_pdf(args.skip_pdf))

    if errors:
        print("VALIDATION FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print("VALIDATION PASSED")
    print(f"- {len(bib_keys)} unique BibTeX entries")
    print(f"- {len(markdown_files())} Markdown documents checked")
    if not args.skip_pdf:
        pdf = ROOT / "paper" / "The_Demure_Fulcrum_Academic_Paper.pdf"
        print(f"- PDF present ({pdf.stat().st_size:,} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
