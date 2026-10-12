#!/usr/bin/env python3
"""Build a lecture-note deck for any session written in the standard format.

Usage: python3 scripts/build_standard_session_deck.py 3.1 [3.2 ...]

The session in 1169.md must follow the course session standard (problem,
practice data with bold subheadings, three-step method, Lecture Content parts,
2 poor + 2 improved prompts, Exercise 1 with an answer key, Exercise 2 with a
template, Part A, and Part B, Report, Success check). Every slide is built from
the Markdown, so editing 1169.md and rerunning keeps the deck in sync.
"""

from __future__ import annotations

import re
import sys
import textwrap
from pathlib import Path

from pypdf import PdfReader
from weasyprint import HTML

import build_session_2_1_deck as d
from build_lecture_notes_from_markdown import ART
from chat_box import CHAT_CSS, chat

ROOT = Path(__file__).resolve().parents[1]
MD_PATH = ROOT / "1169.md"


# ---------------- Markdown parsing ----------------

def session_text(num: str) -> tuple[str, str]:
    md = MD_PATH.read_text(encoding="utf-8")
    md = md[:md.index("<!-- Superseded")] if "<!-- Superseded" in md else md
    m = re.search(rf"(?m)^#### Session {re.escape(num)}: (.+)$", md)
    rest = md[m.end():]
    end = re.search(r"(?m)^(#### Session |### Module |---\s*$)", rest)
    return m.group(1).strip(), rest[:end.start()] if end else rest


def blocks(section: str) -> dict[str, str]:
    found = list(re.finditer(r"(?m)^- \*\*(.+?):\*\*[ \t]*(.*)$", section))
    out = {}
    for i, m in enumerate(found):
        end = found[i + 1].start() if i + 1 < len(found) else len(section)
        out[m.group(1)] = (m.group(2) + "\n" + section[m.end():end]).strip("\n")
    return out


def pick(bl: dict[str, str], prefix: str) -> str:
    for key, value in bl.items():
        if key.startswith(prefix):
            return value
    return ""


def dedent(text: str) -> str:
    lines = text.split("\n")
    first, rest = lines[0], textwrap.dedent("\n".join(lines[1:]))
    return (first + "\n" + rest).strip("\n")


def md_inline(text: str) -> str:
    """Escape, keep **bold**, turn `code` into plain text, links into their text."""
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = text.replace("`", "")
    return d.inline(text)


def parse_table(lines: list[str]) -> tuple[list[str], list[list[str]]]:
    rows = [[c.strip() for c in l.strip().strip("|").split("|")] for l in lines if l.strip().startswith("|")]
    rows = [r for r in rows if not all(re.fullmatch(r":?-{3,}:?", c) for c in r)]
    return rows[0], rows[1:]


def elements(text: str) -> list[tuple[str, object]]:
    """Split a dedented Markdown chunk into paragraphs, bullets, numbered items, tables, fences."""
    out: list[tuple[str, object]] = []
    lines = text.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        s = line.strip()
        if not s:
            i += 1
            continue
        if s.startswith("```"):
            j = i + 1
            while not lines[j].strip().startswith("```"):
                j += 1
            out.append(("fence", textwrap.dedent("\n".join(lines[i + 1:j]))))
            i = j + 1
            continue
        if s.startswith("|"):
            j = i
            while j < len(lines) and lines[j].strip().startswith("|"):
                j += 1
            out.append(("table", parse_table(lines[i:j])))
            i = j
            continue
        m = re.match(r"^(-|\d+\.)\s+(.*)$", s)
        if m:
            kind = "bullet" if m.group(1) == "-" else "number"
            item = m.group(2)
            j = i + 1
            while j < len(lines) and lines[j].strip() and not re.match(r"^\s*(-|\d+\.)\s+|^\s*\|", lines[j]):
                item += " " + lines[j].strip()
                j += 1
            out.append((kind, item))
            i = j
            continue
        para = s
        j = i + 1
        while j < len(lines) and lines[j].strip() and not re.match(r"^\s*(-|\d+\.|\||```)", lines[j]):
            para += " " + lines[j].strip()
            j += 1
        out.append(("para", para))
        i = j
    return out


def strip_check(text: str) -> str:
    text = re.sub(r"^Check the answer:\s*", "", text)
    return text[:1].upper() + text[1:]


def labeled(item: str) -> tuple[str, str] | None:
    m = re.match(r"^\*\*(.+?):?\*\*:?\s*(.*)$", item)
    return (m.group(1).rstrip(":"), m.group(2)) if m else None


# ---------------- deck building ----------------

def table_html(head: list[str], rows: list[list[str]]) -> str:
    out = '<table class="data"><thead><tr>' + "".join(f"<th>{md_inline(h)}</th>" for h in head) + "</tr></thead><tbody>"
    for row in rows:
        out += "<tr>" + "".join(f"<td>{md_inline(c)}</td>" for c in row) + "</tr>"
    return out + "</tbody></table>"


def ul(items: list[str]) -> str:
    return "<ul>" + "".join(f"<li>{md_inline(x)}</li>" for x in items) + "</ul>"


def ol(items: list[str]) -> str:
    return "<ol>" + "".join(f"<li>{md_inline(x)}</li>" for x in items) + "</ol>"


def card(tag: str, title: str, body: str, kind: str = "") -> str:
    return (f'<article class="card {kind}"><div class="tag">{d.esc(tag)}</div>'
            f"<h2>{md_inline(title)}</h2>{body}</article>")


def visual_lines(text: str, width: int) -> int:
    return sum(max(1, -(-len(line) // width)) for line in text.splitlines())


def build(num: str) -> str:
    title, section = session_text(num)
    slug = num.replace(".", "_")
    cover, question = ART[slug]
    bl = blocks(section)
    pages = [f'<section class="cover"><img src="../images/{cover}" alt="{d.esc(question)}"></section>']
    n = 2

    def add(kicker, heading, subtitle, content):
        nonlocal n
        pages.append(d.slide(kicker, heading, subtitle, content, n)
                     .replace("Session 2.1", f"Session {num}"))
        n += 1

    # Problem and goal
    problem = bl["Problem"].strip()
    goal = bl["Goal"].strip()
    add("Problem first", "What problem are we solving?", goal,
        '<div class="grid one">' + card("The situation", "The problem", f"<p>{md_inline(problem)}</p>", "alert") + "</div>")

    # Method
    method_key = next(k for k in bl if k.startswith("Three-step method"))
    steps = [labeled(t) for k, t in elements(dedent(bl[method_key])) if k == "number"]
    add("Goal and method", "Today's goal and a three-step method", goal,
        '<div class="grid three">' + "".join(
            card(f"Step {i}", name, f"<p>{md_inline(text)}</p>") for i, (name, text) in enumerate(steps, 1)) + "</div>")

    # Practice data
    practice = dedent(pick(bl, "Practice data"))
    groups: list[tuple[str, list]] = []
    intro = ""
    current: list = []
    heading = None
    for kind, value in elements(practice):
        if kind == "para" and re.fullmatch(r"\*\*(.+)\*\*", value):
            if heading is not None:
                groups.append((heading, current))
            heading, current = re.fullmatch(r"\*\*(.+)\*\*", value).group(1), []
        elif heading is None:
            intro += " " + value
        else:
            current.append((kind, value))
    if heading is not None:
        groups.append((heading, current))
    files = re.findall(r"\((data/[^)]+)\)", practice)
    subtitle = "Fictional data created for this class." + (f" File: {files[0]}" if files else "")
    for gname, items in groups:
        tables = [v for k, v in items if k == "table"]
        bullets = [v for k, v in items if k in ("bullet", "number")]
        paras = [v for k, v in items if k == "para"]
        body = ""
        for head, rows in tables:
            for start in range(0, len(rows), 9):
                chunk = rows[start:start + 9]
                extra = f" ({start + 1}-{start + len(chunk)} of {len(rows)})" if len(rows) > 9 else ""
                add("Practice data", gname + extra, subtitle, table_html(head, chunk)
                    + "".join(f'<p class="note">{md_inline(p)}</p>' for p in paras))
        if not tables:
            body = ul(bullets) if bullets else "".join(f"<p>{md_inline(p)}</p>" for p in paras)
            add("Practice data", gname, subtitle, '<div class="grid one">' + card("Case facts", gname, body) + "</div>")

    # Lecture parts
    lecture = pick(bl, "Lecture Content")
    parts = list(re.finditer(r"(?m)^  - \*\*Part (\d+): (.+?)(?: \(\d+ min\))?:\*\*[ \t]*$", lecture))
    for i, m in enumerate(parts):
        end = parts[i + 1].start() if i + 1 < len(parts) else len(lecture)
        body_md = textwrap.dedent(lecture[m.end():end])
        els = elements(body_md)
        ptitle = m.group(2)
        kicker = f"Part {m.group(1)}"
        paras = [v for k, v in els if k == "para"]
        tables = [v for k, v in els if k == "table"]
        items = [v for k, v in els if k in ("bullet", "number")]
        lab = [labeled(x) for x in items]
        sub = paras[0] if paras else ""
        later_paras = paras[1:]
        if tables:
            head, rows = tables[0]
            below = ""
            plain = [x for x, l in zip(items, lab) if not l] + later_paras
            cards_lab = [l for l in lab if l]
            if plain:
                below += card("Key points", "What the table shows", ul(plain))
            for name, text in cards_lab:
                below += card("Key point", name, f"<p>{md_inline(text)}</p>")
            text_lines = sum(-(-len(x) // 110) for x in plain) + sum(-(-len(t) // 55) + 1 for _, t in cards_lab)
            if below and len(rows) + text_lines > 9:
                add(kicker, ptitle, sub, table_html(head, rows))
                add(kicker, ptitle + " (key points)", sub, f'<div class="grid two">{below}</div>'
                    if len(cards_lab) + bool(plain) > 1 else f'<div class="grid one">{below}</div>')
            else:
                add(kicker, ptitle, sub, table_html(head, rows)
                    + (f'<div class="grid two after-table">{below}</div>' if below else ""))
            continue
        if lab and all(lab):
            per = 2 if any(len(t) > 260 for _, t in lab) else 3
            for start in range(0, len(lab), per):
                chunk = lab[start:start + per]
                cls = {1: "one", 2: "two", 3: "three"}[len(chunk)]
                add(kicker, ptitle if start == 0 else ptitle + " (continued)", sub,
                    f'<div class="grid {cls}">' + "".join(
                        card("Key idea", name, f"<p>{md_inline(text)}</p>") for name, text in chunk) + "</div>")
            continue
        add(kicker, ptitle, sub, '<div class="grid one">' + card("Key ideas", ptitle, ul(items + later_paras)) + "</div>")

    # Prompt examples
    examples = d.prompt_examples(section)
    names = [e["title"].split(" (")[0] for e in examples]
    if names != ["Poor prompt 1", "Poor prompt 2", "Improved prompt 1", "Improved prompt 2"]:
        raise RuntimeError(f"Session {num}: unexpected prompt examples {names}")
    for ex in examples:
        poor = ex["title"].startswith("Poor")
        kind = "weak" if poor else "good"
        ptitle, _, note = ex["title"].partition(" (")
        note = note.rstrip(")")
        label = f"{ptitle} - do not use" if poor else f"{ptitle} - copy and send"
        rtitle = "Why it is weak" if poor else "Why it works"
        side = ""
        if ex["often"]:
            side += card("What the AI often answers", "A typical result", f"<p>{md_inline(ex['often'])}</p>", "alert")
        side += card(rtitle, "Reasons", ul(ex["reasons"]), "" if poor else "good")
        if visual_lines(ex["prompt"], 52) <= 13:
            add("Compare examples", ptitle, "Same case. Compare what the prompt asks for.",
                '<div class="grid two">' + chat(ex["prompt"], kind, label) + f'<div class="stack">{side}</div></div>')
            continue
        add("Compare examples", ptitle, (note + ". " if note else "") + "Copy this prompt exactly.",
            chat(ex["prompt"], kind, label, cols=visual_lines(ex["prompt"], 105) > 13))
        add("Compare examples", f"{rtitle}: {ptitle.lower()}", "Each part of the prompt matters.",
            f'<div class="grid one"><div class="stack">{side}</div></div>')

    # Exercise 1
    ex1_key = next(k for k in bl if k.startswith("Exercise 1"))
    ex1_title = ex1_key.split(":")[-1].split("(")[0].strip()
    ex1 = dedent(bl[ex1_key])
    steps_md, _, key_md = ex1.partition("**Answer key:**")
    steps1 = [v for k, v in elements(steps_md) if k == "number"]
    add("Hour 2 | Exercise 1", f"Exercise 1: {ex1_title[0].upper() + ex1_title[1:]}",
        "Guided practice. Follow the steps in order.",
        '<div class="grid one">' + card("Guided practice", "Steps", ol(steps1)) + "</div>")
    key_els = elements(key_md)
    key_tables = [v for k, v in key_els if k == "table"]
    key_notes = [v for k, v in key_els if k == "para"]
    if key_tables:
        add("Hour 2 | Exercise 1", "Answer key", "Use this table to check the AI.",
            table_html(*key_tables[0]) + "".join(f'<p class="note">{md_inline(p)}</p>' for p in key_notes))

    # Exercise 2
    ex2_key = next(k for k in bl if k.startswith("Exercise 2"))
    ex2_title = ex2_key.split(":")[-1].split("(")[0].strip()
    ex2 = dedent(bl[ex2_key])
    before_a, _, after_a = ex2.partition("**Part A")
    part_a, _, part_b = after_a.partition("**Part B")
    intro_els = elements(before_a)
    intro_paras = [v for k, v in intro_els if k == "para"]
    fences = [v for k, v in intro_els if k == "fence"]
    template = fences[0] if fences else ""
    add("Hour 3 | Exercise 2", f"Exercise 2: {ex2_title[0].upper() + ex2_title[1:]}", "Applied practice with a template.",
        '<div class="grid two">' + card("How it works", "Read first", ul(intro_paras))
        + chat(template, "plain", "Template - fill in, then send") + "</div>")

    a_els = elements(part_a)
    a_fence = next(v for k, v in a_els if k == "fence")
    a_check = [v for k, v in a_els if k == "para" and v.startswith("Check the answer")]
    head_text = re.sub(r"^\s*-\s*Worked example \(run it\):\*\*\s*", "", part_a.split("```")[0]).strip()
    a_intro = [" ".join(head_text.split())] if head_text else []
    a_intro = [v for v in a_intro if v and not v.startswith("In the chat from Exercise 1")]
    add("Hour 3 | Exercise 2", "Part A: Worked example (run it)", "Copy and send this completed prompt in the same chat.",
        '<div class="grid two">' + chat(a_fence, "good", "Part A - copy and send")
        + card("Check the answer", "Expected result",
               "".join(f"<p><b>Case:</b> {md_inline(v)}</p>" for v in a_intro)
               + "".join(f"<p>{md_inline(strip_check(c))}</p>" for c in a_check), "good") + "</div>")

    b_els = elements("**Part B" + part_b)
    b_task = [v for k, v in b_els if k == "para" and not v.startswith("Check the answer")]
    b_task = [re.sub(r"^\*\*Part B[^*]*\*\*\s*", "", t) for t in b_task]
    b_check = [v for k, v in b_els if k == "para" and v.startswith("Check the answer")]
    add("Hour 3 | Exercise 2", "Part B: Your turn (write it)", "Fill in the template yourself and send it.",
        '<div class="grid two">' + card("Your task", "Write your own prompt", "".join(f"<p>{md_inline(t)}</p>" for t in b_task))
        + card("Check the answer", "Expected result",
               "".join(f"<p>{md_inline(strip_check(c))}</p>" for c in b_check), "good") + "</div>")

    # Report and success check
    report = re.findall(r"(?m)^  - \*\*(Introduction|Method|Results|Conclusion):\*\* (.+)$", section)
    if [r[0] for r in report] != ["Introduction", "Method", "Results", "Conclusion"]:
        raise RuntimeError(f"Session {num}: report sections not found")
    file_name = re.search(r"File name: `(\S+?\.docx)`", section).group(1)
    add("Session report", "Write your session report",
        f"Use Report_template.docx in Microsoft Word. Save it as {file_name} and upload it to iLearn by 23:59 on class day.",
        '<div class="grid one">' + card("Submit", "One report for this session",
                                        ul([f"**{k}:** {v}" for k, v in report])) + "</div>")
    success = bl["Success check"].strip()
    add("Finish and verify", "How to know the work is complete", "Check your report before you hand it in.",
        '<div class="grid one">' + card("Verify", "Success check", ul([success]), "good") + "</div>")

    return ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            f"<title>Session {num}: {d.esc(title)} - Lecture Notes</title>"
            f"{d.STYLE}<style>{CHAT_CSS}</style></head><body>" + "".join(pages) + "</body></html>")


def main(nums: list[str]) -> None:
    for num in nums:
        slug = num.replace(".", "_")
        html_path = ROOT / "slides" / f"session_{slug}_lecture.html"
        pdf_path = ROOT / "slides" / f"session_{slug}_lecture.pdf"
        html_path.write_text(build(num), encoding="utf-8")
        HTML(filename=str(html_path), base_url=str(html_path.parent)).write_pdf(str(pdf_path))
        reader = PdfReader(str(pdf_path))
        for page_no, page in enumerate(reader.pages, start=1):
            box = page.mediabox
            if abs(float(box.width) - 1152) > 0.2 or abs(float(box.height) - 648) > 0.2:
                raise RuntimeError(f"Session {num} page {page_no}: unexpected page size {box}")
        if not reader.pages[0].images:
            raise RuntimeError(f"Session {num}: cover illustration did not render")
        print(f"Session {num}: {len(reader.pages)} pages -> {pdf_path}")


if __name__ == "__main__":
    main(sys.argv[1:])
