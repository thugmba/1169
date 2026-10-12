#!/usr/bin/env python3
"""Build the Session 2.3 lecture-note deck (HTML + 16:9 PDF).

Reuses the layout helpers of the Session 2.1 builder. Prompts, reasons, report
items, and the file name are read from 1169.md so the deck stays in sync.
"""

from __future__ import annotations

import csv
import re
from pathlib import Path

from pypdf import PdfReader
from weasyprint import HTML

import build_session_2_1_deck as d
from chat_box import CHAT_CSS, chat

ROOT = Path(__file__).resolve().parents[1]
MD_PATH = ROOT / "1169.md"
CSV_PATH = ROOT / "data" / "session_2_3_coffee_cart_costs.csv"
HTML_PATH = ROOT / "slides" / "session_2_3_lecture.html"
PDF_PATH = ROOT / "slides" / "session_2_3_lecture.pdf"
COVER = "session_2_3_coffee_cart_scope_hanji.png"
QUESTION = "What can we fit into $4,000 and eight weeks?"


def section_text() -> str:
    md = MD_PATH.read_text(encoding="utf-8")
    start = md.index("#### Session 2.3:")
    return md[start:md.index("#### Session 2.4:")]


def visual_lines(text: str, width: int) -> int:
    return sum(max(1, -(-len(line) // width)) for line in text.splitlines())


def money(value: str) -> str:
    return f"${float(value):,.2f}"


def build() -> str:
    section = section_text()
    examples = d.prompt_examples(section)
    titles = [e["title"].split(" (")[0] for e in examples]
    if titles != ["Poor prompt 1", "Poor prompt 2", "Improved prompt 1", "Improved prompt 2"]:
        raise RuntimeError(f"Unexpected prompt examples: {titles}")
    ex2 = section.split("**Exercise 2")[1]
    template, worked = [d.dedent_fence(f) for f in d.fences(ex2)][:2]
    rows = list(csv.DictReader(CSV_PATH.open(encoding="utf-8")))
    v1 = [r for r in rows if r["category"] == "Version 1 quote"]
    other = [r for r in rows if r["category"] != "Version 1 quote"]
    total = sum(float(r["cost_USD"]) for r in v1)
    if round(total, 2) != 3200.00:
        raise RuntimeError(f"Version 1 total changed: {total}")

    pages = [f'<section class="cover"><img src="../images/{COVER}" alt="{d.esc(QUESTION)}"></section>']
    n = 2

    def add(kicker, title, subtitle, content):
        nonlocal n
        pages.append(d.slide(kicker, title, subtitle, content, n).replace("Session 2.1", "Session 2.3"))
        n += 1

    add("Problem first", "What problem are we solving?",
        "Root problem: the coffee cart plan keeps growing.",
        '<div class="grid three">'
        + d.card("Root problem", "The plan keeps growing", d.ul([
            "A student club wants to open a coffee cart on campus.",
            "Limits: **$4,000**, **8 weeks**, **3 volunteers**.",
            "Every meeting, members add new ideas."]), "alert")
        + d.card("The club's idea", "Let AI write the plan", d.ul([
            "AI could write a full project plan quickly.",
            "But the plan must fit the club's limits."]))
        + d.card("What went wrong", "Professional, but over budget", d.ul([
            '"Write a complete plan for opening a coffee cart on campus."',
            "The AI added an espresso machine and promised opening in week 4.",
            "With the club's quotes: **$5,700**, which is **$1,700 over budget**."]))
        + "</div>")

    add("Goal and method", "Today's goal and a three-step method",
        "Use AI to set a project boundary, then test every new idea against it.",
        '<div class="grid three">'
        + d.card("Step 1", "State the boundary", d.ul([
            "Outcome, deadline, budget, team.", "What version 1 includes."]))
        + d.card("Step 2", "Sort and check", d.ul([
            "In scope, out of scope, TBD.", "Check the budget total yourself."]))
        + d.card("Step 3", "Test every change request", d.ul([
            "Cost, time, and approvals.", "Then accept, save for later, or replace."]))
        + "</div>")

    add("Practice data", "Project facts",
        "Fictional data created for this class. File: data/session_2_3_coffee_cart_costs.csv",
        '<div class="grid two">'
        + d.card("Limits", "What the club has", d.ul([
            "Budget: **$4,000** maximum.", "Target: open in **8 weeks**.", "Team: **3** student volunteers.",
            "Version 1 menu: drip coffee and tea."]))
        + d.card("Unknowns", "What the club does not know yet", d.ul([
            "Campus space approval and a food permit are required.",
            "The applications are not filed yet.",
            "The approval time is unknown (TBD)."]), "alert")
        + "</div>")

    add("Practice data", "Version 1 price quotes",
        "These eight items are the first version of the coffee cart.",
        d.table(["Item", "Cost"], [[r["item"], money(r["cost_USD"])] for r in v1] + [["**Total**", f"**{money(str(total))}**"]]))

    add("Practice data", "Other ideas and change requests",
        "These are not in version 1. Each one must be tested against the boundary.",
        d.table(["Item", "Cost", "Category"], [[r["item"], money(r["cost_USD"]), r["category"]] for r in other]))

    add("Part 1 | Project words", "Scope, budget, and buffer",
        "Before you ask an AI to plan a project, know what these words mean.",
        '<div class="grid two">'
        + d.card("Word 1", "Scope", "<p>The work included in this version of the project.</p>"
                 + d.ul(["In scope: drip coffee and tea.", "Out of scope: work saved for later, such as an espresso machine."]))
        + d.card("Word 2", "Budget and buffer", "<p>The budget is the most money the project can spend. "
                 "The buffer is the money left after the planned costs.</p>"
                 '<p class="formula">$4,000 - $3,200 = $800 buffer</p>')
        + "</div>")

    add("Part 1 | Project words", "Milestone, dependency, and TBD",
        "Each example uses the coffee cart.",
        '<div class="grid three">'
        + d.card("Word 3", "Milestone", "<p>A checkable result by a certain week.</p>"
                 '<p class="formula">Week 2: permit application submitted</p><p>You can answer yes or no.</p>')
        + d.card("Word 4", "Dependency", "<p>Something the team needs from another person or office.</p>"
                 "<p>The cart cannot open until the campus approves the space.</p>")
        + d.card("Word 5", "TBD", "<p>To be determined: a fact the team still needs to confirm.</p>"
                 "<p>TBD means \"find out,\" not \"guess.\"</p>")
        + "</div>")

    add("Part 2 | Why the AI was wrong", '"Looks complete" and "fits the project" are different',
        "Compare the AI plan with the project facts.",
        d.table(["AI plan said", "Project facts", "Problem"], [
            ["Buy an espresso machine", "Version 1 menu is drip coffee and tea", "Out of scope, +$2,500.00"],
            ["Open in week 4", "Target is week 8; approval time is unknown", "Invented date"],
            ['"Campus approval: week 1"', "Applications are not filed yet", "Unknown shown as fact"]], {0: "low"})
        + '<div class="grid two after-table">'
        + d.card("The math", "Over budget", '<p class="formula">$3,200 + $2,500 = $5,700</p>'
                 '<p class="formula">$5,700 - $4,000 = $1,700 over</p>', "alert")
        + d.card("Why", "The AI planned an ideal cart", d.ul([
            "Without the limits, it planned the best coffee cart, not the one the club can afford."]))
        + "</div>")

    add("Part 3 | The fix", "How the three-step method fixes the plan",
        "The instructor runs the prompts below and compares the answers.",
        '<div class="grid three">'
        + d.card("Step 1 fixes", "The boundary problem", d.ul([
            "The AI knows the budget, deadline, team, and version 1 menu."]))
        + d.card("Step 2 fixes", "The trust problem", d.ul([
            "A cost table with a total lets you check the math in one minute.",
            "AI tools can add numbers wrong. Always check the total."]))
        + d.card("Step 3 fixes", 'The "yes to everything" problem', d.ul([
            "Each new idea is checked for cost, time, and approvals.", "Unknowns stay TBD."]))
        + "</div>")

    for ex in examples:
        poor = ex["title"].startswith("Poor")
        kind = "weak" if poor else "good"
        title, _, note = ex["title"].partition(" (")
        note = note.rstrip(")")
        label = f"{title} - do not use" if poor else f"{title} - copy and send"
        reasons_title = "Why it is weak" if poor else "Why it works"
        side = ""
        if ex["often"]:
            side += d.card("What the AI often answers", "A typical result", f"<p>{d.inline(ex['often'])}</p>", "alert")
        side += d.card(reasons_title, "Reasons", d.ul(ex["reasons"]), "" if poor else "good")
        if visual_lines(ex["prompt"], 52) <= 13:
            add("Compare examples", title, "Same project facts. Compare what the prompt asks for.",
                '<div class="grid two">' + chat(ex["prompt"], kind, label) + f'<div class="stack">{side}</div></div>')
            continue
        add("Compare examples", title, (note + ". " if note else "") + "Copy this prompt exactly.",
            chat(ex["prompt"], kind, label, cols=visual_lines(ex["prompt"], 105) > 13))
        add("Compare examples", f"{reasons_title}: {title.lower()}", "Each part of the prompt matters.",
            f'<div class="grid one"><div class="stack">{side}</div></div>')

    add("Hour 2 | Exercise 1", "Exercise 1: Set the boundary",
        "Guided practice. Follow the five steps in order.",
        '<div class="grid one">' + d.card("Guided practice", "Steps", d.ol([
            "Open ChatGPT and start a **new chat**. Paste and send **Poor Prompt 1**. Write down three things the AI added that are not in the project facts.",
            "Start another **new chat**. Paste and send **Improved Prompt 1**.",
            "Check the total: $1,200 + $300 + $250 + $400 + $600 + $150 + $200 + $100 = $3,200. Buffer: $4,000 - $3,200 = $800. Compare the AI lists with the answer key.",
            "In the same chat, paste and send **Improved Prompt 2**. Check that no approval date appears and every milestone has a target week and a yes/no check.",
            "For the Results section of your report, write the three things Poor Prompt 1 added and why Improved Prompt 1 did not add them."])) + "</div>")

    add("Hour 2 | Exercise 1", "Answer key: three lists",
        "Use this table to check the AI.",
        d.table(["List", "Items"], [
            ["In scope (version 1)", "Used coffee cart, two drip coffee brewers, hot water dispenser, cups and lids, "
                                     "coffee beans and tea, signs and menu board, campus food permit fee, card reader. "
                                     "**Total $3,200.00; buffer $800.00**"],
            ["Out of scope (later)", "Espresso machine, fresh juice, mobile ordering app"],
            ["TBD (to confirm)", "Campus space approval date, food permit approval date, price of a mobile ordering app"]]))

    add("Hour 3 | Exercise 2", "Exercise 2: Test a change request",
        "Two weeks before opening, members send new requests.",
        '<div class="grid two">' + d.card("How it works", "Say yes only if it fits", d.ul([
            "Name the request and its extra costs.",
            "Compare the new total with $4,000.",
            "Check time, approvals, and people. Mark unknowns TBD.",
            "Recommend: accept now, save for version 2, or replace an item."]))
        + chat(template, "plain", "Template - replace each [part], then send") + "</div>")

    add("Hour 3 | Exercise 2", "Part A: Worked example (run it)",
        "In the chat from Exercise 1, copy and send this completed prompt.",
        '<div class="grid two">' + chat(worked, "good", "Part A - copy and send")
        + d.card("Check the answer", "Fresh juice", '<p class="formula">$350 + $600 + $300 = $1,250</p>'
                 '<p class="formula">$3,200 + $1,250 = $4,450</p>'
                 + d.ul(["**$450 over budget.** The food permit may also need to cover juice (TBD).",
                         "Recommendation: **save fresh juice for version 2**."]), "good") + "</div>")

    add("Hour 3 | Exercise 2", "Part B: Your turn (write it)",
        'A member asks: "Can we add hot chocolate? We only need cocoa powder for $120 a month."',
        '<div class="grid two">' + d.card("Your task", "Fill in the template yourself", d.ul([
            "Your prompt must name the request, the extra cost, and the three options.",
            "Send it in the same chat."]))
        + d.card("Check the answer", "Hot chocolate", '<p class="formula">$3,200 + $120 = $3,320</p>'
                 '<p class="formula">$4,000 - $3,320 = $680 buffer</p>'
                 + d.ul(["No new equipment. Add it to the permit application (confirm: TBD).",
                         "Recommendation: **accept now**."]), "good") + "</div>")

    report = re.findall(r"(?m)^  - \*\*(Introduction|Method|Results|Conclusion):\*\* (.+)$", section)
    if [r[0] for r in report] != ["Introduction", "Method", "Results", "Conclusion"]:
        raise RuntimeError("Session 2.3 report sections not found in 1169.md")
    file_name = re.search(r"File name: `(\S+?\.docx)`", section).group(1)
    add("Session report", "Write your session report",
        f"Use Report_template.docx in Microsoft Word. Save it as {file_name} and upload it to iLearn by 23:59 on class day.",
        '<div class="grid one">' + d.card("Submit", "One report for this session",
                                          d.ul([f"**{name}:** {text}" for name, text in report])) + "</div>")

    success = re.search(r"(?m)^- \*\*Success check:\*\* (.+)$", section).group(1)
    add("Finish and verify", "How to know the work is complete", "Check your report before you hand it in.",
        '<div class="grid one">' + d.card("Verify", "Success check", d.ul([success]), "good") + "</div>")

    return ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<title>Session 2.3: Set a Manageable Project Scope - Lecture Notes</title>'
            f"{d.STYLE}<style>{CHAT_CSS}</style></head><body>" + "".join(pages) + "</body></html>")


def main() -> None:
    HTML_PATH.write_text(build(), encoding="utf-8")
    HTML(filename=str(HTML_PATH), base_url=str(HTML_PATH.parent)).write_pdf(str(PDF_PATH))
    reader = PdfReader(str(PDF_PATH))
    for page_no, page in enumerate(reader.pages, start=1):
        box = page.mediabox
        if abs(float(box.width) - 1152) > 0.2 or abs(float(box.height) - 648) > 0.2:
            raise RuntimeError(f"Page {page_no}: unexpected page size {box}")
    if not reader.pages[0].images:
        raise RuntimeError("Cover illustration did not render")
    print(f"Session 2.3: {len(reader.pages)} pages -> {PDF_PATH}")


if __name__ == "__main__":
    main()
