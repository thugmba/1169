#!/usr/bin/env python3
"""Build 16:9 lecture-note PDFs from the active student-facing session Markdown."""

from __future__ import annotations

import html
import csv
import re
from pathlib import Path

from pypdf import PdfReader
from weasyprint import HTML


ROOT = Path(__file__).resolve().parents[1]
MD_PATH = ROOT / "1169.md"
SLIDES = ROOT / "slides"
IMAGES = ROOT / "images"
STAGING = Path("/tmp/1169-markdown-lecture-notes")

ART = {
    "1_1": ("session_1_1_fundamentals_hanji.png", "Should we trust a fluent AI answer without checking the facts?"),
    "1_2": ("session_1_2_prompt_architecture_hanji.png", "How can one prompt produce a useful business briefing?"),
    "1_3": ("session_1_3_constraints_hanji.png", "How can we make this summary short, clear, and useful?"),
    "1_4": ("session_1_4_problem_hanji.png", "Should we test two more kiosks and keep staffed lanes open?"),
    "2_1": ("session_2_1_business_data_hanji.png", "Which lunch change could improve service without hurting profit?"),
    "2_2": ("session_2_2_prompt_quality_hanji.png", "Does this reply follow our return policy?"),
    "2_3": ("session_2_3_project_scope_hanji.png", "Can we add juice without breaking our budget or deadline?"),
    "2_4": ("session_2_4_customer_profiles_hanji.png", "What would make this budgeting app useful to different users?"),
    "3_1": ("session_3_1_financial_analysis_hanji.png", "Why did sales rise while gross profit fell?"),
    "3_2": ("session_3_2_operations_hanji.png", "Why were 18 of 30 orders late?"),
    "3_3": ("session_3_3_hr_communication_hanji.png", "What skills does this support role actually need?"),
    "3_4": ("session_3_4_ai_privacy_hanji.png", "What customer details should stay out of an unapproved AI tool?"),
    "4_1": ("session_4_1_reusable_workflows_hanji.png", "How can we turn meeting notes into a reliable recap?"),
    "4_2": ("session_4_2_prompt_troubleshooting_hanji.png", "What should AI do when key campaign details are missing?"),
    "4_3": ("session_4_3_prompt_selection_hanji.png", "Which prompt is worth polishing first?"),
    "4_4": ("session_4_4_prompt_portfolio_hanji.png", "Can a teammate use this prompt safely on their own?"),
}

REPLACEMENTS = {
    "\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"',
    "\u2014": "-", "\u2013": "-", "\u00a0": " ", "\u00d7": "x",
    "\u2212": "-", "\u00f7": "/", "\u2264": "<=", "\u2265": ">=",
    "\u2192": "->", "\u2026": "...", "\u2022": "-",
}


def plain(value: str) -> str:
    value = re.sub(r"!\[[^]]*\]\([^)]*\)", "", value)
    value = re.sub(r"\[([^]]+)\]\(([^)]+)\)", r"\1 (\2)", value)
    value = re.sub(r"<a\s+id=[^>]+></a>", "", value)
    value = re.sub(r"<[^>]+>", "", value)
    value = re.sub(r"`([^`]*)`", r"\1", value)
    value = re.sub(r"\*\*(.*?)\*\*", r"\1", value)
    value = re.sub(r"\*(.*?)\*", r"\1", value)
    for old, new in REPLACEMENTS.items():
        value = value.replace(old, new)
    return re.sub(r"\s+", " ", value).strip()


def split_sessions(markdown: str) -> list[tuple[str, str, str]]:
    active = re.sub(r"<!--.*?-->", "", markdown, flags=re.S)
    matches = list(re.finditer(r"(?m)^####\s+Session\s+(\d\.\d):\s*(.+?)\s*$", active))
    sessions = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(active)
        sessions.append((match.group(1), plain(match.group(2)), active[match.end():end]))
    return sessions


def top_blocks(section: str) -> list[tuple[str, str]]:
    pattern = re.compile(r"(?m)^-[ \t]+\*\*(.+?)\*\*:?[ \t]*(.*)$")
    found = list(pattern.finditer(section))
    blocks = []
    for i, match in enumerate(found):
        end = found[i + 1].start() if i + 1 < len(found) else len(section)
        label = plain(match.group(1)).rstrip(":")
        value = match.group(2) + "\n" + section[match.end():end]
        blocks.append((label, value.strip("\n")))
    return blocks


def pick(blocks: list[tuple[str, str]], *needles: str) -> str:
    for label, value in blocks:
        if any(n.lower() in label.lower() for n in needles):
            return value
    return ""


def items_from(block: str) -> list[str]:
    if not block:
        return []
    fence = r"\x60{3}(?:\w+)?[ \t]*\n([\s\S]*?)\n[ \t]*\x60{3}[ \t]*"
    block = re.sub(r"(?m)^[ \t]*" + fence, lambda m: "\nCODE: " + m.group(1).strip().replace("\n", " | ") + "\n", block)
    result: list[str] = []
    current = ""
    for raw in block.splitlines():
        line = raw.strip()
        if not line:
            continue
        if re.match(r"^(?:[-*+]\s+|\d+[.)]\s+)", line):
            if current:
                result.append(plain(current))
            current = re.sub(r"^(?:[-*+]\s+|\d+[.)]\s+)", "", line)
        elif current:
            current += " " + line
        else:
            current = line
    if current:
        result.append(plain(current))
    return [x for x in result if x]


def lecture_parts(lecture: str) -> list[tuple[str, list[str]]]:
    matches = list(re.finditer(r"(?m)^[ \t]{2}-[ \t]+\*\*Part\s+\d+:\s*(.*?)\*\*[ \t]*$", lecture))
    out = []
    for i, match in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(lecture)
        title = plain(match.group(1)).rstrip(":")
        content = lecture[match.end():end]
        out.append((title, items_from(content)))
    return out


def prompt_examples(section: str, blocks: list[tuple[str, str]]) -> tuple[list[str], list[str]]:
    candidates = [(label.lower(), value) for label, value in blocks
                  if any(w in label.lower() for w in ("prompt comparison", "prompt examples", "poor", "good"))]
    text = "\n".join(v for _, v in candidates)
    poor: list[str] = []
    good: list[str] = []
    fence_pat = re.compile(r"(?m)^[ \t]*\x60{3}(?:\w+)?[ \t]*\n([\s\S]*?)\n[ \t]*\x60{3}[ \t]*$")
    for match in fence_pat.finditer(text):
        before = text[max(0, match.start() - 420):match.start()]
        labels = list(re.finditer(r"(?i)\b(weak|strong|poor|improved|good)(?:\s+example)?(?:\s+[12])?\b", before))
        label = labels[-1].group(1).lower() if labels else ""
        snippet = plain(match.group(1))
        if len(snippet) > 1000:
            snippet = snippet[:997].rsplit(" ", 1)[0] + "..."
        if label in ("weak", "poor") and len(poor) < 2:
            poor.append(snippet)
        elif label in ("strong", "good", "improved") and len(good) < 2:
            good.append(snippet)
    if not poor or not good:
        inline = re.compile(r'(?im)^\s*[-*]\s*(Poor|Weak|Improved|Good|Strong)(?:\s+example)?\s*([12])?\s*:\s*(.+)$')
        for match in inline.finditer(text):
            kind = match.group(1).lower()
            raw = plain(match.group(3))
            quoted = re.match(r'"([^"]+)"', raw)
            if quoted:
                raw = quoted.group(1)
            raw = raw[:800]
            if kind in ("poor", "weak") and len(poor) < 2:
                poor.append(raw)
            elif kind in ("good", "strong", "improved") and len(good) < 2:
                good.append(raw)
    return poor, good


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def card(title: str, body: str, tag: str = "") -> str:
    return (f'<article class="card"><div class="tag">{esc(tag)}</div>'
            f'<h2>{esc(title)}</h2>{body}</article>')


def bullet_list(values: list[str]) -> str:
    return "<ul>" + "".join(f"<li>{esc(v)}</li>" for v in values) + "</ul>"


def slide(kicker: str, title: str, subtitle: str, content: str, slug: str, number: int) -> str:
    return (f'<section class="slide"><header><div class="meta"><span>{esc(kicker)}</span>'
            f'<span>Session {slug.replace("_", ".")}</span></div><div class="rule"></div>'
            f'<h1>{esc(title)}</h1><p class="subtitle">{esc(subtitle)}</p></header>'
            f'<main>{content}</main><footer><span>Business AI Tools | Lecture Notes</span>'
            f'<span>Session {slug.replace("_", ".")} | Slide {number}</span></footer></section>')


def chunked(values: list[str], limit: int = 1100) -> list[list[str]]:
    pages, page, length = [], [], 0
    for value in values:
        if page and length + len(value) > limit:
            pages.append(page)
            page, length = [], 0
        page.append(value)
        length += len(value)
    if page:
        pages.append(page)
    return pages or [["Use the complete session materials on the main course page."]]


def make_deck(num: str, title: str, section: str) -> str:
    slug = num.replace(".", "_")
    img, question = ART[slug]
    blocks = top_blocks(section)
    problem = plain(pick(blocks, "Problem"))
    goal = plain(pick(blocks, "Goal"))
    material = items_from(pick(blocks, "Practice material", "Practice dataset", "Lab material"))
    data_files = list(dict.fromkeys(re.findall(r"\]\((data/[^)]+)\)", section)))
    if data_files:
        material.extend(data_files)
    if not problem:
        legacy_problems = {
            "1.1": "Business staff need useful AI-written communication, but fluent output can contain unsupported facts. They must know when to search, when to draft with AI, and what a person must verify.",
            "1.2": "A vague request often produces a generic, poorly structured memo that takes repeated editing. The user needs a prompt that supplies the role, business context, task, and expected format.",
            "1.3": "An unconstrained AI summary can be too long, vague, and hard to use. A manager needs a way to specify required content, forbidden filler, audience, tone, and length.",
        }
        problem = legacy_problems.get(num, f"The practical challenge is to apply {title.lower()} to a real business task and check whether the result is useful.")
    if not goal:
        goal = f"Use the session method to address the problem in {title.lower()} and verify the result against the supplied source material."

    pages = []
    # Full-bleed session illustration page.
    pages.append(f'<section class="cover"><img src="../images/{esc(img)}" alt="{esc(question)}"></section>')
    n = 2
    duration = plain(pick(blocks, "Duration"))
    if data_files:
        materials_text = "CSV: " + ", ".join(Path(x).name for x in data_files)
    elif material:
        materials_text = "; ".join(material[:2])[:220]
    else:
        materials_text = "Use the practice material supplied in the session Markdown."
    pages.append(slide("Problem first", "What problem are we solving?", duration or "Session lesson and guided practice",
        '<div class="grid two">' + card("The problem", f'<p>{esc(problem)}</p>', "Situation") +
        card("Learning goal", f'<p>{esc(goal)}</p><p class="small"><b>Practice material:</b> {esc(materials_text)}</p>', "Target") + '</div>', slug, n)); n += 1

    case_terms = ("practice data", "practice facts", "practice message", "practice notes",
                  "practice request", "practice candidates", "practice task", "product facts",
                  "fictional shop policy", "customer messages", "fictional interview notes",
                  "scenario facts", "fictional scenario facts", "public data source")
    case_blocks = [(label, value) for label, value in blocks
                   if any(term in label.lower() for term in case_terms)]
    if case_blocks:
        cards = []
        for label, value in case_blocks:
            values = items_from(value)
            if values:
                cards.append(card(label, bullet_list(values[:8]), "Case material"))
        if data_files:
            cards.append(card("Files for practice", bullet_list(data_files), "Open or download"))
        if cards:
            for offset in range(0, len(cards), 2):
                group = cards[offset:offset + 2]
                if len(group) == 1:
                    group.append(card("Use the supplied facts", f'<p>{esc(problem)}</p>', "Boundary"))
                pages.append(slide("Case material", "Use these supplied facts", "Do not replace missing information with guesses.", '<div class="grid two">' + "".join(group) + '</div>', slug, n)); n += 1

    for relative in data_files:
        source = ROOT / relative
        if not source.is_file():
            continue
        with source.open(newline="", encoding="utf-8-sig") as stream:
            reader = csv.reader(stream)
            rows = list(reader)
        if len(rows) > 1 and len(rows) <= 20:
            headings, data_rows = rows[0], rows[1:]
            page_rows = 7 if len(data_rows) > 9 else len(data_rows)
            row_groups = [data_rows[i:i + page_rows] for i in range(0, len(data_rows), page_rows)]
            for part_no, group in enumerate(row_groups, start=1):
                table = '<div class="data-table-wrap"><table class="data-table"><thead><tr>'
                table += "".join(f"<th>{esc(value)}</th>" for value in headings)
                table += "</tr></thead><tbody>"
                for row in group:
                    table += "<tr>" + "".join(f"<td>{esc(value)}</td>" for value in row) + "</tr>"
                table += '</tbody></table><p class="data-caption">Fictional instructional data from ' + esc(relative) + '.</p></div>'
                title = "Use every supplied row" if len(row_groups) == 1 else f"Dataset rows {1 + (part_no - 1) * page_rows}-{(part_no - 1) * page_rows + len(group)} of {len(data_rows)}"
                subtitle = "The complete small practice dataset is reproduced here for spreadsheet work."
                if len(row_groups) > 1:
                    subtitle = f"Dataset part {part_no} of {len(row_groups)}. Use all parts as one practice dataset."
                pages.append(slide("Complete practice dataset", title, subtitle, table, slug, n)); n += 1

    concepts = items_from(pick(blocks, "Related concepts", "Core concepts", "Key concepts"))
    method = items_from(pick(blocks, "Three-step method", "Method"))
    lecture = pick(blocks, "Lecture Content")
    parts = lecture_parts(lecture) if lecture else []
    if concepts:
        concept_chunks = chunked(concepts, 900)
        for idx, group in enumerate(concept_chunks):
            body = '<div class="grid two">' + card("Core concepts", bullet_list(group), "Understand")
            if idx == 0 and method:
                body += card("A simple method", bullet_list(method[:5]), "Apply")
            elif len(concept_chunks) == 1:
                body += card("Why it matters", f'<p>{esc(goal)}</p>', "Use")
            body += '</div>'
            pages.append(slide("Concept and method", "Concepts for this problem" if idx == 0 else "More concepts to check", "Keep each concept tied to the practical decision.", body, slug, n)); n += 1
    elif parts:
        for offset in range(0, len(parts), 2):
            group = parts[offset:offset + 2]
            body = '<div class="grid two">'
            for part_title, part_items in group:
                body += card(part_title, bullet_list(part_items[:5]), "Core idea")
            body += '</div>'
            pages.append(slide("Lecture concepts", "What students need to understand", "Key explanations taken from the active session lesson.", body, slug, n)); n += 1

    poor, good = prompt_examples(section, blocks)
    if poor:
        body = '<div class="grid two">' + "".join(card(f"Weak example {i+1}", f'<pre>{esc(p)}</pre>', "Avoid") for i, p in enumerate(poor)) + '</div>'
        pages.append(slide("Compare examples", "What makes a prompt weak?", "These examples come from the current session scenario.", body, slug, n)); n += 1
    if good:
        body = '<div class="grid two">' + "".join(card(f"Improved example {i+1}", f'<pre>{esc(p)}</pre>', "Use") for i, p in enumerate(good)) + '</div>'
        pages.append(slide("Compare examples", "A clearer, safer prompt", "Keep the source, task, constraints, and output check visible.", body, slug, n)); n += 1

    exercise1 = pick(blocks, "Exercise 1") or pick(blocks, "How to Practice")
    exercise2 = pick(blocks, "Exercise 2")
    for label, title_text, block in (("Guided practice", "Exercise 1: Follow the steps", exercise1),
                                      ("Applied practice", "Exercise 2: Try a small variation", exercise2)):
        values = items_from(block)
        if not values:
            continue
        for ix, group in enumerate(chunked(values, 1450)):
            body = '<div class="grid one">' + card(title_text + (f" - continued {ix+1}" if ix else ""), bullet_list(group), label) + '</div>'
            pages.append(slide(label, title_text if ix == 0 else title_text + " (continued)", "Use the complete case and instructions from the session Markdown.", body, slug, n)); n += 1

    deliverable = items_from(pick(blocks, "Deliverable"))
    success = items_from(pick(blocks, "Success check", "What to Expect"))
    if not deliverable:
        deliverable = ["Submit the exercise output and briefly state which source facts support it."]
    if not success:
        success = ["The answer follows the session constraints, uses supplied evidence, and labels missing information instead of guessing."]
    body = '<div class="grid two">' + card("Deliverable", bullet_list(deliverable[:6]), "Submit") + card("Success check", bullet_list(success[:6]), "Verify") + '</div>'
    pages.append(slide("Finish and verify", "How to know the work is complete", "Check the output before sharing or acting on it.", body, slug, n))

    style = r'''
<style>
@page { size: 16in 9in; margin: 0; }
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; color: #172033; font-family: Arial, Helvetica, sans-serif; }
body { background: #f8fafc; }
.cover { width: 16in; height: 9in; padding: 0; margin: 0; display: flex; align-items: center; justify-content: center; overflow: hidden; background: #f8f5ed; page-break-after: always; break-after: page; }
.cover img { width: 100%; height: 100%; object-fit: contain; display: block; }
.slide { width: 16in; height: 9in; padding: .45in .8in .4in; margin: 0; display: flex; flex-direction: column; overflow: hidden; background: #fff; page-break-after: always; break-after: page; }
header { flex-shrink: 0; margin-bottom: .18in; }
.meta { display: flex; justify-content: space-between; color: #475569; font-size: 17px; font-weight: bold; letter-spacing: .08em; text-transform: uppercase; }
.meta span:first-child { color: #991b1b; }
.rule { height: 5px; flex-shrink: 0; background: #991b1b; margin: 8px 0 10px; }
h1 { margin: 0; font: bold 52px/1.08 Georgia, 'Times New Roman', serif; color: #172033; }
.subtitle { margin: 8px 0 0; color: #334155; font-size: 26px; line-height: 1.2; }
main { flex: 1; min-height: 0; display: flex; flex-direction: column; margin-bottom: .25in; }
.grid { display: flex; gap: 18px; flex: 1; min-height: 0; }
.grid.two > .card { width: 50%; }
.grid.one > .card { width: 100%; }
.card { min-width: 0; border: 1px solid #cbd5e1; border-radius: 14px; padding: 20px 24px; background: #fbfbfa; overflow: hidden; }
.tag { margin: 0 0 8px; color: #991b1b; font-size: 17px; font-weight: 800; letter-spacing: .08em; text-transform: uppercase; }
h2 { margin: 0 0 12px; color: #172033; font: bold 30px/1.12 Georgia, 'Times New Roman', serif; }
p, li { font-size: 24px; line-height: 1.28; }
p { margin: 0 0 12px; }
ul { margin: 0; padding-left: 26px; }
li { margin: 0 0 9px; }
.small { margin-top: 18px; font-size: 21px; color: #334155; }
.data-table-wrap { flex: 1; min-height: 0; display: flex; flex-direction: column; }
.data-table { width: 100%; border-collapse: collapse; table-layout: fixed; font-size: 20px; line-height: 1.13; }
.data-table th { background: #172033; color: #fff; text-align: left; font-size: 19px; }
.data-table th, .data-table td { border: 1px solid #cbd5e1; padding: 7px 8px; overflow-wrap: anywhere; }
.data-table tr:nth-child(even) { background: #f1f5f9; }
.data-caption { margin-top: 10px; color: #475569; font-size: 16px; }
pre { margin: 0; white-space: pre-wrap; overflow-wrap: anywhere; font: 21px/1.28 'Courier New', monospace; color: #172033; }
footer { height: .42in; flex-shrink: 0; border-top: 1px solid #cbd5e1; padding-top: 8px; display: flex; justify-content: space-between; color: #475569; font-size: 16px; }
</style>'''
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            f'<title>Session {num}: {esc(title)} - Lecture Notes</title>{style}</head><body>'
            + "".join(pages) + "</body></html>")


def main() -> None:
    STAGING.mkdir(parents=True, exist_ok=True)
    sessions = split_sessions(MD_PATH.read_text(encoding="utf-8"))
    if len(sessions) != 16:
        raise RuntimeError(f"Expected 16 active sessions in {MD_PATH}, found {len(sessions)}")
    generated = []
    for num, title, section in sessions:
        slug = num.replace(".", "_")
        if slug not in ART:
            raise RuntimeError(f"No approved illustration configured for Session {num}")
        html_path = SLIDES / f"session_{slug}_lecture.html"
        pdf_path = SLIDES / f"session_{slug}_lecture.pdf"
        html_path.write_text(make_deck(num, title, section), encoding="utf-8")
        staged_pdf = STAGING / pdf_path.name
        HTML(filename=str(html_path), base_url=str(SLIDES)).write_pdf(str(staged_pdf))
        reader = PdfReader(str(staged_pdf))
        if len(reader.pages) < 7:
            raise RuntimeError(f"Session {num} deck unexpectedly short: {len(reader.pages)} pages")
        for page_no, page in enumerate(reader.pages, start=1):
            box = page.mediabox
            if abs(float(box.width) - 1152) > 0.2 or abs(float(box.height) - 648) > 0.2:
                raise RuntimeError(f"Session {num} page {page_no}: unexpected page size {box}")
        if not reader.pages[0].images:
            raise RuntimeError(f"Session {num}: cover illustration did not render")
        generated.append((html_path, pdf_path, staged_pdf, len(reader.pages)))
    # Only replace PDFs after every source deck has rendered and passed validation.
    for _, pdf_path, staged_pdf, _ in generated:
        pdf_path.write_bytes(staged_pdf.read_bytes())
    for html_path, pdf_path, _, pages in generated:
        print(f"Session {pdf_path.stem.removeprefix('session_').removesuffix('_lecture')}: {pages} pages -> {pdf_path}")


if __name__ == "__main__":
    main()
