#!/usr/bin/env python3
"""Build the Demure Fulcrum working paper PDF from Markdown and BibTeX.

The script intentionally uses a small, deterministic Markdown subset so the
repository can rebuild the committed PDF without a full TeX toolchain.
"""

from __future__ import annotations

import html
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

try:
    from reportlab.graphics.shapes import Drawing, Line, Rect, String
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import mm
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.platypus import (
        HRFlowable,
        Image,
        KeepTogether,
        PageBreak,
        Paragraph,
        Preformatted,
        SimpleDocTemplate,
        Spacer,
        Table,
        TableStyle,
    )
except ImportError as exc:  # pragma: no cover - dependency guard
    raise SystemExit(
        "ReportLab is required. Install it with: python -m pip install reportlab"
    ) from exc

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "paper" / "The_Demure_Fulcrum_Academic_Paper.md"
BIB = ROOT / "references" / "references.bib"
OUTPUT = ROOT / "paper" / "The_Demure_Fulcrum_Academic_Paper.pdf"
SYMBOL = ROOT / "assets" / "demure_fulcrum_symbol.png"


@dataclass(frozen=True)
class BibEntry:
    key: str
    kind: str
    fields: dict[str, str]

    @property
    def author_text(self) -> str:
        return self.fields.get("author", self.fields.get("editor", "Unknown"))

    @property
    def year(self) -> str:
        return self.fields.get("year", "n.d.")


def register_fonts() -> tuple[str, str, str]:
    candidates = [
        (
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf",
        ),
        (
            "/usr/local/share/fonts/DejaVuSans.ttf",
            "/usr/local/share/fonts/DejaVuSans-Bold.ttf",
            "/usr/local/share/fonts/DejaVuSans-Oblique.ttf",
        ),
    ]
    for regular, bold, italic in candidates:
        if all(Path(p).exists() for p in (regular, bold, italic)):
            pdfmetrics.registerFont(TTFont("DemureSans", regular))
            pdfmetrics.registerFont(TTFont("DemureSans-Bold", bold))
            pdfmetrics.registerFont(TTFont("DemureSans-Italic", italic))
            pdfmetrics.registerFontFamily(
                "DemureSans",
                normal="DemureSans",
                bold="DemureSans-Bold",
                italic="DemureSans-Italic",
                boldItalic="DemureSans-Bold",
            )
            return "DemureSans", "DemureSans-Bold", "DemureSans-Italic"
    return "Helvetica", "Helvetica-Bold", "Helvetica-Oblique"


def parse_front_matter(text: str) -> tuple[dict[str, str], str]:
    metadata: dict[str, str] = {}
    if not text.startswith("---\n"):
        return metadata, text
    closing = text.find("\n---\n", 4)
    if closing == -1:
        return metadata, text
    raw = text[4:closing]
    for line in raw.splitlines():
        if ":" not in line or line.startswith((" ", "\t")):
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip('"').strip("'")
    return metadata, text[closing + 5 :]


def parse_bibtex(path: Path) -> dict[str, BibEntry]:
    text = path.read_text(encoding="utf-8")
    starts = list(re.finditer(r"@([A-Za-z]+)\s*\{\s*([^,\s]+)\s*,", text))
    entries: dict[str, BibEntry] = {}
    for index, match in enumerate(starts):
        end = starts[index + 1].start() if index + 1 < len(starts) else len(text)
        body = text[match.end() : end]
        fields: dict[str, str] = {}
        for line in body.splitlines():
            field_match = re.match(
                r"\s*([A-Za-z][A-Za-z0-9_-]*)\s*=\s*[\{\"](.*?)[\}\"]\s*,?\s*$",
                line,
            )
            if field_match:
                fields[field_match.group(1).lower()] = field_match.group(2).strip()
        key = match.group(2).strip()
        entries[key] = BibEntry(key=key, kind=match.group(1).lower(), fields=fields)
    if not entries:
        raise ValueError(f"No BibTeX entries parsed from {path}")
    return entries


def family_name(author: str) -> str:
    author = author.strip()
    if "," in author:
        return author.split(",", 1)[0].strip()
    particles = {"de", "del", "van", "von", "der", "da"}
    words = author.split()
    if len(words) >= 2 and words[-2].lower() in particles:
        return " ".join(words[-2:])
    return words[-1] if words else "Unknown"


def citation_label(entry: BibEntry) -> str:
    authors = [a.strip() for a in entry.author_text.split(" and ") if a.strip()]
    if not authors:
        lead = "Unknown"
    elif len(authors) == 1:
        lead = family_name(authors[0])
    elif len(authors) == 2:
        lead = f"{family_name(authors[0])} & {family_name(authors[1])}"
    else:
        lead = f"{family_name(authors[0])} et al."
    return f"{lead}, {entry.year}"


def replace_citations(text: str, entries: dict[str, BibEntry]) -> str:
    def repl(match: re.Match[str]) -> str:
        raw = match.group(1)
        labels: list[str] = []
        for part in raw.split(";"):
            token = part.strip()
            key_match = re.match(r"@([A-Za-z0-9_:\-.]+)", token)
            if not key_match:
                labels.append(token)
                continue
            key = key_match.group(1)
            entry = entries.get(key)
            label = citation_label(entry) if entry else f"MISSING:{key}"
            suffix = token[key_match.end() :].strip()
            labels.append(f"{label}{', ' + suffix if suffix else ''}")
        return f"({'; '.join(labels)})"

    return re.sub(r"\[@([^\]]+)\]", repl, text)


def inline_markup(text: str, entries: dict[str, BibEntry]) -> str:
    text = replace_citations(text, entries)
    text = html.escape(text, quote=False)
    text = re.sub(
        r"\[([^\]]+)\]\((https?://[^)]+)\)",
        r'<a href="\2" color="#24527a"><u>\1</u></a>',
        text,
    )
    text = re.sub(r"`([^`]+)`", r'<font name="Courier">\1</font>', text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", text)
    return text


def make_styles(font: str, bold: str, italic: str) -> dict[str, ParagraphStyle]:
    sample = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "Title",
            parent=sample["Title"],
            fontName=bold,
            fontSize=23,
            leading=28,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#182b3a"),
            spaceAfter=12,
        ),
        "subtitle": ParagraphStyle(
            "Subtitle",
            parent=sample["Normal"],
            fontName=italic,
            fontSize=11.5,
            leading=16,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#3c5263"),
            spaceAfter=12,
        ),
        "meta": ParagraphStyle(
            "Meta",
            parent=sample["Normal"],
            fontName=font,
            fontSize=9.5,
            leading=13,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#536976"),
        ),
        "status": ParagraphStyle(
            "Status",
            parent=sample["Normal"],
            fontName=bold,
            fontSize=10,
            leading=14,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#7a341c"),
            borderColor=colors.HexColor("#c47a59"),
            borderWidth=0.8,
            borderPadding=8,
            backColor=colors.HexColor("#fff4ed"),
        ),
        "h1": ParagraphStyle(
            "H1",
            parent=sample["Heading1"],
            fontName=bold,
            fontSize=17,
            leading=21,
            textColor=colors.HexColor("#182b3a"),
            spaceBefore=14,
            spaceAfter=8,
            keepWithNext=True,
        ),
        "h2": ParagraphStyle(
            "H2",
            parent=sample["Heading2"],
            fontName=bold,
            fontSize=13.2,
            leading=17,
            textColor=colors.HexColor("#24527a"),
            spaceBefore=12,
            spaceAfter=6,
            keepWithNext=True,
        ),
        "h3": ParagraphStyle(
            "H3",
            parent=sample["Heading3"],
            fontName=bold,
            fontSize=10.8,
            leading=14,
            textColor=colors.HexColor("#3a596c"),
            spaceBefore=10,
            spaceAfter=4,
            keepWithNext=True,
        ),
        "body": ParagraphStyle(
            "Body",
            parent=sample["BodyText"],
            fontName=font,
            fontSize=9.3,
            leading=13.2,
            alignment=TA_JUSTIFY,
            textColor=colors.HexColor("#1f2a30"),
            spaceAfter=6,
            allowWidows=0,
            allowOrphans=0,
        ),
        "lead": ParagraphStyle(
            "Lead",
            parent=sample["BodyText"],
            fontName=font,
            fontSize=10.1,
            leading=14.2,
            alignment=TA_JUSTIFY,
            textColor=colors.HexColor("#1d303d"),
            spaceAfter=7,
        ),
        "quote": ParagraphStyle(
            "Quote",
            parent=sample["BodyText"],
            fontName=italic,
            fontSize=9.2,
            leading=13,
            leftIndent=9 * mm,
            rightIndent=6 * mm,
            borderColor=colors.HexColor("#91a8b5"),
            borderWidth=1,
            borderPadding=7,
            textColor=colors.HexColor("#314754"),
            spaceBefore=4,
            spaceAfter=8,
        ),
        "bullet": ParagraphStyle(
            "Bullet",
            parent=sample["BodyText"],
            fontName=font,
            fontSize=9.2,
            leading=12.7,
            leftIndent=7 * mm,
            firstLineIndent=-3.5 * mm,
            spaceAfter=3,
        ),
        "code": ParagraphStyle(
            "Code",
            parent=sample["Code"],
            fontName="Courier",
            fontSize=8.1,
            leading=10.5,
            leftIndent=5 * mm,
            rightIndent=5 * mm,
            borderColor=colors.HexColor("#cad5db"),
            borderWidth=0.5,
            borderPadding=6,
            backColor=colors.HexColor("#f4f7f8"),
            spaceAfter=7,
        ),
        "reference": ParagraphStyle(
            "Reference",
            parent=sample["BodyText"],
            fontName=font,
            fontSize=7.8,
            leading=10.5,
            leftIndent=5 * mm,
            firstLineIndent=-5 * mm,
            spaceAfter=4,
            alignment=TA_LEFT,
        ),
        "caption": ParagraphStyle(
            "Caption",
            parent=sample["Normal"],
            fontName=italic,
            fontSize=8,
            leading=10.5,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#526a78"),
            spaceBefore=4,
            spaceAfter=9,
        ),
    }


def fulcrum_figure(font: str, bold: str) -> Drawing:
    width, height = 470, 190
    d = Drawing(width, height)
    navy = colors.HexColor("#1f4054")
    blue = colors.HexColor("#4f7d95")
    pale = colors.HexColor("#eaf1f4")
    warm = colors.HexColor("#a85f3a")
    d.add(String(width / 2, 176, "The Demure Fulcrum as a level-of-analysis model", fontName=bold, fontSize=12, textAnchor="middle", fillColor=navy))
    labels = [
        (12, 112, 100, 42, "1. Physiological state", "arousal and regulation"),
        (132, 112, 100, 42, "2. Action tendency", "fight, flight, freeze, approach"),
        (252, 112, 100, 42, "3. Meta-response", "attempt to transform the situation"),
        (372, 112, 86, 42, "4. Application", "mediation, institutions, Hexure"),
    ]
    for idx, (x, y, w, h, title, sub) in enumerate(labels):
        fill = colors.HexColor("#fff0e8") if idx == 2 else pale
        stroke = warm if idx == 2 else blue
        d.add(Rect(x, y, w, h, rx=5, ry=5, fillColor=fill, strokeColor=stroke, strokeWidth=1.2))
        d.add(String(x + w / 2, y + 26, title, fontName=bold, fontSize=7.8, textAnchor="middle", fillColor=navy))
        d.add(String(x + w / 2, y + 12, sub, fontName=font, fontSize=6.7, textAnchor="middle", fillColor=colors.HexColor("#405864")))
        if idx < len(labels) - 1:
            d.add(Line(x + w + 3, y + h / 2, labels[idx + 1][0] - 3, y + h / 2, strokeColor=blue, strokeWidth=1))
    d.add(Line(88, 55, 382, 55, strokeColor=navy, strokeWidth=2))
    d.add(Rect(226, 43, 28, 24, fillColor=colors.HexColor("#d9e4e9"), strokeColor=navy, strokeWidth=1))
    d.add(String(240, 28, "fulcrum: inhibit immediate selection, test whether G can become G′", fontName=italic_font_name(), fontSize=8, textAnchor="middle", fillColor=warm))
    return d


def italic_font_name() -> str:
    return "DemureSans-Italic" if "DemureSans-Italic" in pdfmetrics.getRegisteredFontNames() else "Helvetica-Oblique"


def table_from_lines(
    lines: list[str],
    styles: dict[str, ParagraphStyle],
    entries: dict[str, BibEntry],
    available_width: float,
) -> Table:
    rows: list[list[str]] = []
    for line in lines:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells and all(re.fullmatch(r":?-{3,}:?", c.replace(" ", "")) for c in cells):
            continue
        rows.append(cells)
    max_cols = max(len(r) for r in rows)
    for row in rows:
        row.extend([""] * (max_cols - len(row)))
    data = [
        [Paragraph(inline_markup(cell, entries), styles["body"]) for cell in row]
        for row in rows
    ]
    widths = [available_width / max_cols] * max_cols
    table = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dbe8ee")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#17384a")),
                ("FONTNAME", (0, 0), (-1, 0), styles["h3"].fontName),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#9fb2bc")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f7f9fa")]),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return table


def format_reference(entry: BibEntry) -> str:
    f = entry.fields
    authors = f.get("author", f.get("editor", "Unknown"))
    year = f.get("year", "n.d.")
    title = f.get("title", "Untitled")
    container = f.get("journal", f.get("booktitle", f.get("publisher", "")))
    volume = f.get("volume", "")
    number = f.get("number", "")
    pages = f.get("pages", "")
    parts = [f"{authors} ({year}). <i>{title}</i>."]
    if container:
        venue = f" {container}"
        if volume:
            venue += f", {volume}"
        if number:
            venue += f"({number})"
        if pages:
            venue += f", {pages}"
        parts.append(venue + ".")
    doi = f.get("doi", "")
    url = f.get("url", "")
    if doi:
        parts.append(f' <a href="https://doi.org/{html.escape(doi)}" color="#24527a">https://doi.org/{html.escape(doi)}</a>')
    elif url:
        safe = html.escape(url)
        parts.append(f' <a href="{safe}" color="#24527a">{safe}</a>')
    return "".join(parts)


def page_decor(canvas, doc) -> None:  # type: ignore[no-untyped-def]
    canvas.saveState()
    page = canvas.getPageNumber()
    width, height = A4
    font = "DemureSans" if "DemureSans" in pdfmetrics.getRegisteredFontNames() else "Helvetica"
    canvas.setFont(font, 7.5)
    canvas.setFillColor(colors.HexColor("#607681"))
    if page > 1:
        canvas.drawString(18 * mm, height - 12 * mm, "The Demure Fulcrum — Working Paper")
        canvas.drawRightString(width - 18 * mm, height - 12 * mm, "Not Peer Reviewed")
        canvas.setStrokeColor(colors.HexColor("#cfdae0"))
        canvas.line(18 * mm, height - 14 * mm, width - 18 * mm, height - 14 * mm)
    canvas.drawCentredString(width / 2, 10 * mm, str(page))
    canvas.restoreState()


def build_story(
    markdown: str,
    metadata: dict[str, str],
    entries: dict[str, BibEntry],
    styles: dict[str, ParagraphStyle],
    font: str,
    bold: str,
) -> list:
    story: list = []
    title = metadata.get("title", "The Demure Fulcrum")
    subtitle = metadata.get(
        "subtitle", "A Conceptual Framework and Research Agenda — Working Paper, Not Peer Reviewed"
    )
    author = metadata.get("author", "Daniel Demure")
    date = metadata.get("date", "2026-08-08")

    story.append(Spacer(1, 10 * mm))
    if SYMBOL.exists():
        image = Image(str(SYMBOL))
        image._restrictSize(72 * mm, 72 * mm)
        image.hAlign = "CENTER"
        story.append(image)
        story.append(Spacer(1, 5 * mm))
    story.append(Paragraph(html.escape(title), styles["title"]))
    story.append(Paragraph(html.escape(subtitle), styles["subtitle"]))
    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph(html.escape(author), styles["meta"]))
    story.append(Paragraph(f"Revision date: {html.escape(date)}", styles["meta"]))
    story.append(Spacer(1, 8 * mm))
    story.append(
        Paragraph(
            "WORKING PAPER — NOT PEER REVIEWED<br/>This repository presents a conceptual framework and research agenda, not an empirically validated clinical or neurobiological model.",
            styles["status"],
        )
    )
    story.append(PageBreak())

    lines = markdown.splitlines()
    paragraph_buffer: list[str] = []
    code_buffer: list[str] = []
    in_code = False
    used_keys = set(re.findall(r"@([A-Za-z0-9_:\-.]+)", markdown))

    def flush_paragraph() -> None:
        if not paragraph_buffer:
            return
        text = " ".join(line.strip() for line in paragraph_buffer).strip()
        paragraph_buffer.clear()
        if text:
            style = styles["lead"] if len(story) < 8 else styles["body"]
            story.append(Paragraph(inline_markup(text, entries), style))

    i = 0
    while i < len(lines):
        raw = lines[i]
        stripped = raw.strip()
        if stripped.startswith("```"):
            flush_paragraph()
            if in_code:
                story.append(Preformatted("\n".join(code_buffer), styles["code"]))
                code_buffer.clear()
                in_code = False
            else:
                in_code = True
            i += 1
            continue
        if in_code:
            code_buffer.append(raw)
            i += 1
            continue
        if not stripped:
            flush_paragraph()
            i += 1
            continue
        if stripped == "<!-- FIGURE:FULCRUM -->":
            flush_paragraph()
            story.append(Spacer(1, 3 * mm))
            story.append(fulcrum_figure(font, bold))
            story.append(
                Paragraph(
                    "Figure 1. The framework is located at the level of higher-order response policy; physiological and behavioural systems constrain it, while applications remain downstream hypotheses.",
                    styles["caption"],
                )
            )
            i += 1
            continue
        if stripped.startswith("|") and i + 1 < len(lines) and lines[i + 1].strip().startswith("|"):
            flush_paragraph()
            table_lines: list[str] = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i])
                i += 1
            story.append(table_from_lines(table_lines, styles, entries, 174 * mm))
            story.append(Spacer(1, 5 * mm))
            continue
        heading = re.match(r"^(#{1,3})\s+(.+)$", stripped)
        if heading:
            flush_paragraph()
            level = len(heading.group(1))
            text = heading.group(2)
            if text.lower() == "references":
                story.append(Paragraph("References", styles["h1"]))
                selected = [entries[k] for k in used_keys if k in entries]
                selected.sort(key=lambda e: (family_name(e.author_text).lower(), e.year, e.key))
                for entry in selected:
                    story.append(Paragraph(format_reference(entry), styles["reference"]))
                break
            story.append(Paragraph(inline_markup(text, entries), styles[f"h{level}"]))
            i += 1
            continue
        if stripped.startswith(">"):
            flush_paragraph()
            quote_lines = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote_lines.append(lines[i].strip()[1:].strip())
                i += 1
            story.append(Paragraph(inline_markup(" ".join(quote_lines), entries), styles["quote"]))
            continue
        bullet = re.match(r"^[-*]\s+(.+)$", stripped)
        numbered = re.match(r"^(\d+)\.\s+(.+)$", stripped)
        if bullet or numbered:
            flush_paragraph()
            if bullet:
                story.append(Paragraph(inline_markup(bullet.group(1), entries), styles["bullet"], bulletText="•"))
            else:
                story.append(Paragraph(inline_markup(numbered.group(2), entries), styles["bullet"], bulletText=f"{numbered.group(1)}."))
            i += 1
            continue
        if stripped in {"---", "***"}:
            flush_paragraph()
            story.append(HRFlowable(width="100%", thickness=0.6, color=colors.HexColor("#b4c3ca"), spaceBefore=5, spaceAfter=7))
            i += 1
            continue
        paragraph_buffer.append(stripped)
        i += 1

    flush_paragraph()
    return story


def main() -> int:
    if not SOURCE.exists():
        raise SystemExit(f"Missing source: {SOURCE}")
    if not BIB.exists():
        raise SystemExit(f"Missing bibliography: {BIB}")

    font, bold, italic = register_fonts()
    styles = make_styles(font, bold, italic)
    metadata, markdown = parse_front_matter(SOURCE.read_text(encoding="utf-8"))
    entries = parse_bibtex(BIB)
    story = build_story(markdown, metadata, entries, styles, font, bold)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    document = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=19 * mm,
        bottomMargin=17 * mm,
        title=metadata.get("title", "The Demure Fulcrum"),
        author=metadata.get("author", "Daniel Demure"),
        subject="A conceptual framework and research agenda on negotiation as an agency-preserving meta-response under threat",
    )
    document.build(story, onFirstPage=page_decor, onLaterPages=page_decor)
    if not OUTPUT.exists() or OUTPUT.stat().st_size < 20_000:
        raise RuntimeError("PDF build produced an unexpectedly small file")
    print(f"Built {OUTPUT.relative_to(ROOT)} ({OUTPUT.stat().st_size:,} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
