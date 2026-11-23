#!/usr/bin/env python3
"""Build the Session 3.3 student worksheet (Word) from template.docx.

Usage: python3 scripts/build_worksheet_3_3.py
Output: worksheets/Session_3_3_Worksheet.docx

The worksheet keeps the look of template.docx (styles, page setup, header
logo) and replaces the body with step-by-step instructions, copy-ready
prompts, worked examples (Leo), and blank cells for the student's results.
"""

from __future__ import annotations

from pathlib import Path

import docx
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "worksheets" / "Session_3_3_Worksheet.docx"

GRAY_BOX = "F2F2F2"   # prompt boxes
EXAMPLE_BOX = "EAF1FB"  # Leo's worked example
INPUT_BOX = "FFF8D6"  # cells the student fills in
HEAD_BOX = "D9E2F3"   # table headers
MUTED = RGBColor(0x59, 0x59, 0x59)

doc = docx.Document(str(ROOT / "template.docx"))
body = doc.element.body
for child in list(body):
    if child.tag != qn("w:sectPr"):
        body.remove(child)


# ---------------- helpers ----------------

def shade(cell, color: str) -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), color)
    tc_pr.append(shd)


def add_runs(par, text: str, size: float | None = None, italic: bool = False, color=None) -> None:
    """Add text where **bold** parts become bold runs."""
    parts = text.replace("`", "").split("**")
    for i, part in enumerate(parts):
        if not part:
            continue
        run = par.add_run(part)
        run.bold = i % 2 == 1
        run.italic = italic
        if size:
            run.font.size = Pt(size)
        if color is not None:
            run.font.color.rgb = color


def para(text: str = "", style: str = "Normal", **kw):
    p = doc.add_paragraph(style=style)
    add_runs(p, text, **kw)
    if text.startswith("**Example") or text.startswith("Why the order matters"):
        p.paragraph_format.keep_with_next = True
    return p


def bullets(items: list[str], numbered: bool = False) -> None:
    for i, item in enumerate(items, 1):
        p = doc.add_paragraph(style="Normal")
        p.paragraph_format.left_indent = Pt(18)
        p.paragraph_format.first_line_indent = Pt(-14)
        p.paragraph_format.space_after = Pt(2)
        add_runs(p, (f"{i}.  " if numbered else "•  ") + item)


def cell_text(cell, text: str, bold: bool = False, align: str = "center", size: float = 11,
              italic: bool = False, color=None) -> None:
    cell.text = ""
    lines = text.split("\n")
    for k, line in enumerate(lines):
        p = cell.paragraphs[0] if k == 0 else cell.add_paragraph()
        p.alignment = {"center": WD_ALIGN_PARAGRAPH.CENTER, "left": WD_ALIGN_PARAGRAPH.LEFT}[align]
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.0
        add_runs(p, f"**{line}**" if bold and line else line, size=size, italic=italic, color=color)
    cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER


def table(head: list[str], rows: list[list[str]], fill: str | None = None, align: list[str] | None = None,
          widths: list[float] | None = None, size: float = 11, height_pt: float | None = None,
          italic: bool = False, write: str | None = None):
    if write:
        write_badge(write)
    t = doc.add_table(rows=1 + len(rows), cols=len(head))
    if write:
        orange_border(t)
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    align = align or ["center"] * len(head)
    for j, h in enumerate(head):
        cell_text(t.rows[0].cells[j], h, bold=True, size=size)
        shade(t.rows[0].cells[j], HEAD_BOX)
    for i, row in enumerate(rows, 1):
        for j, value in enumerate(row):
            c = t.rows[i].cells[j]
            cell_text(c, value, align=align[j], size=size, italic=italic and bool(value))
            if fill and not value:
                shade(c, fill)
            elif fill == EXAMPLE_BOX:
                shade(c, fill)
        if height_pt:
            t.rows[i].height = Pt(height_pt)
    widths = widths or [451 / len(head)] * len(head)
    set_widths(t, widths)
    doc.add_paragraph().paragraph_format.space_after = Pt(0)
    return t


def set_widths(t, widths: list[float]) -> None:
    t.autofit = False
    grid = t._tbl.tblGrid
    for j, col in enumerate(grid.findall(qn("w:gridCol"))):
        col.set(qn("w:w"), str(int(widths[j] * 20)))
    for row in t.rows:
        for j, w in enumerate(widths):
            row.cells[j].width = Pt(w)


def box(lines: list[str], color: str, label: str | None = None, mono: bool = False, size: float = 10.5) -> None:
    if label:
        p = para(f"**{label}**")
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
    t = doc.add_table(rows=1, cols=1)
    t.style = "Table Grid"
    c = t.rows[0].cells[0]
    shade(c, color)
    c.text = ""
    for k, line in enumerate(lines):
        p = c.paragraphs[0] if k == 0 else c.add_paragraph()
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.0
        if mono:
            run = p.add_run(line)
            run.font.name = "Consolas"
            run._element.rPr.rFonts.set(qn("w:eastAsia"), "Consolas")
            run.font.size = Pt(size)
        else:
            add_runs(p, line, size=size)
    doc.add_paragraph().paragraph_format.space_after = Pt(0)


def prompt(lines: list[str], label: str = "Copy and send this prompt:") -> None:
    box(lines, GRAY_BOX, label, mono=True)


def example(lines: list[str], label: str = "Example (Leo, Junior Customer Support Assistant)") -> None:
    box(lines, EXAMPLE_BOX, label, size=10.5)


WRITE_COLOR = "C55A11"
write_count = 0


def write_badge(title: str) -> None:
    """Orange 'WRITE HERE' badge that marks every place the student fills in."""
    global write_count
    write_count += 1
    p = doc.add_paragraph(style="Normal")
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(f" \u270f WRITE HERE {write_count} ")
    run.bold = True
    run.font.size = Pt(11)
    run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), WRITE_COLOR)
    run._element.get_or_add_rPr().append(shd)
    add_runs(p, f"  **{title}**", color=RGBColor(0xC5, 0x5A, 0x11))


def orange_border(t) -> None:
    tbl_pr = t._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), "12" if edge in ("top", "left", "bottom", "right") else "6")
        el.set(qn("w:color"), WRITE_COLOR)
        borders.append(el)
    tbl_pr.append(borders)


def answer(label: str, lines: int = 2) -> None:
    write_badge(label)
    t = doc.add_table(rows=1, cols=1)
    orange_border(t)
    t.style = "Table Grid"
    c = t.rows[0].cells[0]
    shade(c, INPUT_BOX)
    c.text = ""
    for _ in range(lines - 1):
        c.add_paragraph()
    doc.add_paragraph().paragraph_format.space_after = Pt(0)


def step(title: str, minutes: int, todo: list[str]) -> None:
    h = doc.add_paragraph(style="Heading 2")
    h.add_run(f"{title} ({minutes} min)")
    h.paragraph_format.keep_with_next = True
    p = para("**What to do:**")
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    bullets(todo, numbered=True)


def page_break() -> None:
    doc.add_paragraph().add_run().add_break(docx.enum.text.WD_BREAK.PAGE)


# ---------------- prompts ----------------

G1 = [
    "You are a strict reviewer of job descriptions. Grade the job description below with this rule only.",
    "Criteria (Pass or Fail):",
    "1. Duties: 3 to 5 concrete duties, each with a share of time, and the shares add up to 100%.",
    "2. Linked: every requirement names the duty it supports.",
    "3. Weighted: every requirement is marked Must-have (weight 2) or Nice-to-have (weight 1).",
    "4. Fair: no age, gender, nationality, appearance, or personality words, and no degree or years of experience unless a duty needs it.",
    "5. Checkable: every requirement says what evidence proves it.",
    "Grade: 5 passes = A, 4 = B, 3 = C, 2 = D, 0 or 1 = E.",
    "For each criterion, write Pass or Fail and quote the words from the job description that show it. Then give the grade.",
    "Job description:",
    "[paste the AI's job description here]",
]

G2 = [
    "You are a strict hiring reviewer. Use only the requirement table and my facts below.",
    "Score rule for each requirement: 0 = no evidence, 0.5 = some evidence, 1 = clear evidence at job level.",
    "Give points only for a fact that matches the evidence the requirement asks for.",
    "Do not guess. Do not give points for facts that match no requirement.",
    "Show a table: Requirement | Weight | Fact you used (quote, or \"no evidence\") | Score | Points (weight x score).",
    "Then show: total points, maximum points, Match % = total / maximum x 100, and the grade: 85% or more = A, 70-84% = B, 55-69% = C, 40-54% = D, below 40% = E.",
    "Requirement table:",
    "[paste the table from your grade-A job description]",
    "My facts:",
    "1. [your fact 1]",
]


# ---------------- content ----------------

doc.add_paragraph("Session 3.3 Worksheet: My Dream Job", style="Title")
doc.add_paragraph("Build a job description, grade it, and grade how well you fit it", style="Author")

table(["First name", "Student ID", "Date"], [["", "", ""]], fill=INPUT_BOX, height_pt=22, write="Your name and student ID")

doc.add_paragraph("How to Use This Worksheet", style="Heading 1")
bullets([
    "Do the steps **in order**. Each step says what to do, gives a prompt to copy, and shows Leo's example.",
    "**Gray boxes** are prompts. Copy them into ChatGPT exactly. Change only the words in [square brackets].",
    "**Blue boxes** are Leo's example. Use them to see what a good answer looks like.",
    "**\u270f WRITE HERE** (orange label, yellow cells) marks every place you must fill in. There are 14 places. You do not write anywhere else.",
    "**The AI does all the grading.** You check the AI once in Step 6 and once in Step 10.",
    "Do not type your name, student ID, phone number, or address into ChatGPT.",
    "**Submit:** save this file as `FirstName_StudentID_W11_Worksheet.docx` (for example, "
    "`James_S1234567_W11_Worksheet.docx`) and upload it to **iLearn** by **23:59 today**.",
])

doc.add_paragraph("The Two Grading Rules", style="Heading 1")
para("You do not grade anything yourself. You paste these rules into ChatGPT, and the AI grades. "
     "Read them so that you understand the grade the AI gives.")
para("**Rule 1: Job description grade.** The AI checks five criteria. Each one is Pass or Fail.")
table(["#", "Criterion", "Pass when..."], [
    ["1", "Duties", "There are 3 to 5 concrete duties, each with a share of time, and the shares add up to 100%."],
    ["2", "Linked", "Every requirement names the duty it supports."],
    ["3", "Weighted", "Every requirement is marked Must-have (weight 2) or Nice-to-have (weight 1)."],
    ["4", "Fair", "No age, gender, nationality, appearance, or personality words. No degree or years of "
                  "experience unless a duty needs it."],
    ["5", "Checkable", "Every requirement says what evidence proves it."],
], align=["center", "center", "left"], widths=[30, 80, 341], size=10.5)
table(["Passes", "5", "4", "3", "2", "0 or 1"], [["Grade", "A", "B", "C", "D", "E"]], size=10.5)

para("**Rule 2: Fit grade.** The AI scores each requirement with your facts: **0** = no evidence, "
     "**0.5** = some evidence, **1** = clear evidence at job level. Points = weight × score.")
para("Match % = total points ÷ maximum points × 100. Example: 4.5 ÷ 8 × 100 = 56%.")
table(["Match %", "85% or more", "70-84%", "55-69%", "40-54%", "Below 40%"],
      [["Grade", "A", "B", "C", "D", "E"]], size=10.5)

para("**Words to know**")
bullets([
    "**Job description (JD):** a document that lists the duties of a job and the skills it needs.",
    "**Duty:** a task the person does. Example: answer customer emails (60% of the time).",
    "**Requirement:** a skill needed for a duty. Example: clear writing in English, for answering emails.",
    "**Evidence:** a fact with a number or a result. \"I am good at Excel\" is not evidence. "
    "\"I made a 50-row table with COUNTIF in a class project\" is evidence.",
])

# ---------- Part 1 ----------
doc.add_paragraph("Part 1 (Hour 2): Build Your Job Description to Grade A", style="Heading 1")
para("You will make your job description four times. Each prompt asks for a little more. "
     "After each one, the AI grades it with Rule 1. Watch the grade go up.")
para("**You need two kinds of chat:** Chat A builds the job description. A **new chat** grades it each time. "
     "Do not grade in Chat A: the AI often gives its own work a high grade.")

step("Step 1. Choose your job title", 5, [
    "Choose a job you would like after you graduate. If you are not sure, pick one from the list below.",
    "Write a company type, for example \"small online shop\" or \"international bank.\"",
    "Write one sentence about why you want this job.",
])
para("Entry-level jobs for business students: Marketing Assistant, Sales Associate, HR Assistant, "
     "Junior Accountant, Data Analyst Intern, Social Media Coordinator, E-commerce Operations Assistant, "
     "Supply Chain Assistant, Customer Support Assistant, Project Coordinator, Financial Analyst Intern, "
     "Event Coordinator.", size=10.5, color=MUTED)
example(["Job title: Junior Customer Support Assistant",
         "Company type: small online shop",
         "Why: I like helping people, and I want to learn how an online business works."])
table(["Job title", "Company type", "Why I want this job (one sentence)"], [["", "", ""]],
      fill=INPUT_BOX, height_pt=40, widths=[120, 110, 220], write="Step 1: your job")

step("Step 2. Poor Prompt 1, then grade it", 10, [
    "Open ChatGPT and start a new chat. This is **Chat A**. Send Poor Prompt 1 with your job title.",
    "Copy the AI's whole job description.",
    "Start a **new chat**. Copy the grading prompt G1 below, paste the job description at the end, and send it.",
    "Write the grade and the numbers of the criteria that failed in the table at the end of Step 5.",
])
prompt(["Write a job description for a [your job title]."], "Poor Prompt 1 (send in Chat A):")
prompt(G1, "Grading prompt G1 (send in a new chat each time you grade):")
example(["Leo sent: Write a job description for a Junior Customer Support Assistant.",
         "The AI wrote a typical ad: a bachelor's degree, 1-2 years of experience, \"energetic team player,\" "
         "and no share of time.",
         "Grade from G1: **E**. Failed criteria: 1, 2, 3, 4, 5."])

step("Step 3. Poor Prompt 2, then grade it", 10, [
    "Go back to **Chat A**. Send Poor Prompt 2.",
    "Copy the new job description. Grade it with G1 in a **new chat**.",
    "Write the grade and the failed criteria in the table.",
])
prompt(["Write a job description for a [your job title] at a [company type].",
        "List 3 to 5 duties with the share of time for each (total 100%).",
        "After each requirement, write the duty it supports in brackets."], "Poor Prompt 2 (send in Chat A):")
example(["Duties and shares of time are there, and each requirement names a duty.",
         "But there are no weights, and \"bachelor's degree\" is still there.",
         "Grade from G1: **D**. Failed criteria: 3, 4, 5."])

step("Step 4. Improved Prompt 1, then grade it", 10, [
    "In **Chat A**, send Improved Prompt 1. You do not need to change any words.",
    "Grade the new job description with G1 in a **new chat**. Write the result in the table.",
])
prompt(["Rewrite the job description. Keep the duties and the links.",
        "Mark each requirement \"Must-have (weight 2)\" or \"Nice-to-have (weight 1)\".",
        "Do not include age, gender, nationality, appearance, or personality words.",
        "Do not require a degree or years of experience unless a duty needs it."],
       "Improved Prompt 1 (send in Chat A):")
example(["Each requirement now has a weight. The degree and \"energetic\" are gone.",
         "Grade from G1: **B**. Failed criterion: 5 (no evidence for each requirement)."])

step("Step 5. Improved Prompt 2, then grade it", 10, [
    "In **Chat A**, send Improved Prompt 2.",
    "Grade the result with G1 in a **new chat**.",
    "If the grade is not A, tell Chat A which criterion failed and ask it to fix it. Example: "
    "\"Criterion 1 failed: the shares add up to 90%. Fix it.\" Grade it again.",
])
prompt(["Add one more column: the evidence that proves each requirement (for example, \"made a table with COUNTIF in a class project\").",
        "Show the final result as a table:",
        "Requirement | Duty | Must or Nice | Weight | Evidence that proves it"],
       "Improved Prompt 2 (send in Chat A):")
example(["Grade from G1: **A**. No failed criteria."])

para("**Example (Leo): grade record**")
table(["Step", "Prompt", "Grade", "Failed criteria"], [
    ["2", "Poor Prompt 1", "E", "1, 2, 3, 4, 5"],
    ["3", "Poor Prompt 2", "D", "3, 4, 5"],
    ["4", "Improved Prompt 1", "B", "5"],
    ["5", "Improved Prompt 2", "A", "None"],
], fill=EXAMPLE_BOX, size=10.5, widths=[50, 150, 100, 151])
table(["Step", "Prompt", "Grade (A-E)", "Failed criteria"], [
    ["2", "Poor Prompt 1", "", ""],
    ["3", "Poor Prompt 2", "", ""],
    ["4", "Improved Prompt 1", "", ""],
    ["5", "Improved Prompt 2", "", ""],
    ["5", "Extra fix (if needed)", "", ""],
], fill=INPUT_BOX, height_pt=20, widths=[50, 150, 100, 151],
      write="Steps 2-5: your grade after each prompt")

step("Step 6. Check the AI's grading", 5, [
    "In the last G1 answer, choose **one** criterion the AI marked Pass.",
    "Find the words the AI quoted. Are they really in your job description?",
    "Add the shares of time of your duties. Do they make 100%?",
])
example(["Criterion checked: 2 (Linked). The AI quoted \"Clear writing in English (Answer customer emails).\" "
         "It is in the job description: Yes.",
         "Shares of time: 60% + 30% + 10% = 100%."])
table(["Criterion I checked", "Is the quoted text in my JD? (Yes/No)", "Shares of time added up"],
      [["", "", "____ + ____ + ____ = ____%"]], fill=INPUT_BOX, height_pt=30, write="Step 6: your check of the AI")

# ---------- Part 2 ----------
doc.add_paragraph("Part 2 (Hour 3): Grade Your Fit and Find What to Improve", style="Heading 1").paragraph_format.page_break_before = True
para("Now you grade yourself against your grade-A job description. You add your facts **one at a time** "
     "and watch how the fit grade changes.")

step("Step 7. Copy your grade-A requirement table", 5, [
    "Copy the final table from Chat A (Step 5) into the yellow table below.",
    "Add up the Weight column. This is your **maximum points**.",
])
para("**Example (Leo): requirement table** (maximum points = 2 + 2 + 2 + 1 + 1 = 8)")
table(["Requirement", "Duty", "Must/Nice", "Weight", "Evidence that proves it"], [
    ["Clear writing in English", "Answer customer emails", "Must", "2", "Emails or reports written in English"],
    ["Careful recordkeeping", "Record case details", "Must", "2", "Kept a list or log for months without errors"],
    ["Basic Excel (sort, filter, COUNTIF)", "Record case details", "Must", "2", "Made a table using these functions"],
    ["Customer service experience", "Answer customer emails", "Nice", "1", "Worked with customers in a job"],
    ["Knowing when to ask for help", "Flag unresolved cases", "Nice", "1", "Reported a problem to a manager"],
], fill=EXAMPLE_BOX, align=["left", "left", "center", "center", "left"], size=10, widths=[110, 100, 55, 45, 141])
table(["Requirement", "Duty", "Must/Nice", "Weight", "Evidence that proves it"],
      [["", "", "", "", ""] for _ in range(6)], fill=INPUT_BOX, height_pt=22, size=10, widths=[110, 100, 55, 45, 141],
      write="Step 7: your grade-A requirement table")
table(["My maximum points (sum of weights)"], [[""]], fill=INPUT_BOX, height_pt=20, write="Step 7: your maximum points")

step("Step 8. Write your facts and guess your grade", 8, [
    "Write 4 or 5 facts about yourself: classes, projects, part-time jobs, clubs, certificates, tools, languages.",
    "Write each fact as **what you did + how much + the result**. Use numbers.",
    "Add **one** fact that has nothing to do with the job (for example, a hobby).",
    "Before the AI grades you, guess your fit grade.",
])
example(["Good fact: \"Wrote 10 customer emails in English for a class project (Business English, grade B).\"",
         "Weak fact: \"I am good at English.\" (no number, no result)",
         "Leo's facts: 1. Worked as a cafe cashier for 6 months. 2. Wrote 10 customer emails in English for a "
         "class project (Business English, grade B). 3. Kept the member list of my club (40 members) for one "
         "year. 4. Once reported a refund problem to the store manager. 5. I like traveling.",
         "Leo's guess: B"])
table(["#", "My fact (what + how much + result)"], [[str(i), ""] for i in range(1, 7)],
      fill=INPUT_BOX, align=["center", "left"], widths=[30, 421], height_pt=24, write="Step 8: your facts")
table(["My guess of my fit grade (A-E)"], [[""]], fill=INPUT_BOX, height_pt=20, write="Step 8: your guess")

step("Step 9. Add your facts one at a time", 12, [
    "Start a **new chat**. Copy G2, paste your requirement table, write only **fact 1**, and send it.",
    "Write the Match % and grade in the yellow table.",
    "In the same chat, send the \"Add a fact\" prompt with fact 2. Write the result. Repeat for each fact.",
    "In the last column, write why the grade changed or did not change.",
])
prompt(G2, "Grading prompt G2 (send in a new chat):")
prompt(["Add this fact and grade again with the same rule. Show the full table, the new total, Match %, and grade.",
        "New fact: [number]. [your next fact]"], "Add a fact (send in the same chat, once for each fact):")
para("**Example (Leo): fit record**")
table(["#", "Fact added", "Total points", "Match %", "Grade", "Why it changed (or not)"], [
    ["1", "Cafe cashier, 6 months", "1.0", "13%", "E", "Matches customer service (Nice, 1 x 1)"],
    ["2", "10 English emails", "3.0", "38%", "E", "Matches clear writing (Must, 2 x 1)"],
    ["3", "Club member list, 1 year", "4.0", "50%", "D", "Some evidence for recordkeeping (2 x 0.5)"],
    ["4", "Reported a refund problem", "4.5", "56%", "C", "Some evidence for asking for help (1 x 0.5)"],
    ["5", "I like traveling", "4.5", "56%", "C", "No change: matches no requirement"],
], fill=EXAMPLE_BOX, align=["center", "left", "center", "center", "center", "left"], size=10, widths=[25, 120, 50, 50, 45, 161])
table(["#", "Fact added", "Total points", "Match %", "Grade", "Why it changed (or not)"],
      [[str(i), "", "", "", "", ""] for i in range(1, 7)], fill=INPUT_BOX, height_pt=24, size=10, widths=[25, 120, 50, 50, 45, 161],
      write="Step 9: your grade after each fact")

step("Step 10. Check the AI's math", 5, [
    "Look at the AI's last table. Add the Points column yourself with a calculator.",
    "Divide by your maximum points and multiply by 100.",
    "If your number is different, send: \"Your total is wrong. Add the Points column again.\"",
    "If a row has points but no quoted fact, send: \"Row [requirement] has no quoted fact. Score it again.\"",
])
example(["Leo: 2 + 1 + 0 + 1 + 0.5 = 4.5. 4.5 ÷ 8 × 100 = 56%. Same as the AI: Yes."])
table(["My total points", "÷ maximum points", "× 100 = Match %", "Same as the AI? (Yes/No)"],
      [["", "", "", ""]], fill=INPUT_BOX, height_pt=22, write="Step 10: your math check")

step("Step 11. Improvement ladder: fix one gap at a time", 15, [
    "In the same chat, send **Ladder prompt 1**. The AI names **one** requirement to improve and one action.",
    "Send **Ladder prompt 2** with the planned fact. The AI grades you again as if you finished the action.",
    "Write the round in the yellow table: the requirement, lost points, action and deadline, planned fact, new Match %, and new grade.",
    "Repeat for the next round. Stop when your grade is **A** or after **3 rounds**.",
])
para("**Ladder rules:** (1) Improve one thing at a time. (2) Start with the most lost points; if two are equal, "
     "start with the Must-have. (3) The action must create the kind of evidence your job description asks for, "
     "with a number and a deadline. (4) A planned fact is marked \"(planned)\": it shows the grade you **can** reach, "
     "not the grade you have now.")
prompt(["Look at my latest table. Find the ONE requirement with the most lost points (weight x (1 - score)).",
        "If two are equal, choose the Must-have. Suggest ONE action I can finish this semester, and write the fact I will be able to write after it, with a number, in the form of the evidence this requirement asks for."],
       "Ladder prompt 1 (send in the same chat):")
prompt(["Add this planned fact and grade again with the same rule. Mark it \"(planned)\".",
        "Show the full table, the new total, Match %, and grade.",
        "Planned fact: [the fact the AI suggested, or your own version]"],
       "Ladder prompt 2 (send in the same chat):")
para("**Example (Leo): improvement ladder** (start: 4.5 of 8 = 56%, grade C)")
table(["#", "Requirement", "Lost points", "Action and deadline", "Planned fact", "New Match %", "New grade"], [
    ["1", "Basic Excel (Must)", "2.0", "Excel class project, by December",
     "Made a 50-row case table with sort, filter, and COUNTIF", "81%", "B"],
    ["2", "Careful recordkeeping (Must)", "1.0", "Keep the club's money record every week, by June",
     "Kept the club's money record every week for 16 weeks with no errors", "94%", "A"],
    ["3", "Stop: grade A", "", "", "", "", ""],
], fill=EXAMPLE_BOX, align=["center", "left", "center", "left", "left", "center", "center"], size=9.5,
   widths=[35, 75, 40, 95, 126, 45, 35])
para("Why the order matters: if Leo first improved \"Knowing when to ask for help\" (Nice-to-have, 0.5 lost points), "
     "he would gain only 0.5 points: 5 of 8 = 63%, still grade C.", size=10.5, color=MUTED)
table(["#", "Requirement", "Lost points", "Action and deadline", "Planned fact", "New Match %", "New grade"],
      [[str(i), "", "", "", "", "", ""] for i in range(1, 4)], fill=INPUT_BOX, height_pt=40, size=9.5,
      widths=[35, 75, 40, 95, 126, 45, 35], write="Step 11: your improvement ladder")

doc.add_paragraph("Step 12. My Conclusion (5 min)", style="Heading 2")
para("Write three sentences in your own words. Do not copy the AI's words.")
example(["1. I guessed B, but my fit grade now is C (56%).",
         "2. My roadmap is Excel first, then recordkeeping, because Excel has the most lost points (2.0) and is a Must-have.",
         "3. If I finish both by June, my grade can rise from C to A (94%)."])
answer("Step 12: my guess and my real fit grade now", 2)
answer("Step 12: my roadmap (what first, what next) and why in this order", 2)
answer("Step 12: the grade I can reach if I finish my roadmap, and by when", 2)

doc.add_paragraph("Before You Submit", style="Heading 1")
bullets([
    "☐  My grade record (Step 5) ends with grade A.",
    "☐  I checked the AI's grading (Step 6) and the AI's math (Step 10).",
    "☐  My fit record (Step 9) has one row for each fact.",
    "☐  My improvement ladder (Step 11) improves one requirement per round and ends with grade A or 3 rounds.",
    "☐  I wrote my three conclusion sentences (Step 12) in my own words.",
    "☐  The file name is `FirstName_StudentID_W11_Worksheet.docx`, and I uploaded it to iLearn by 23:59 today.",
])

for t in doc.tables:
    for row in t.rows:
        tr_pr = row._tr.get_or_add_trPr()
        cant = OxmlElement("w:cantSplit")
        tr_pr.append(cant)
    for row in t.rows[:-1]:
        for cell in row.cells:
            for par in cell.paragraphs:
                par.paragraph_format.keep_with_next = True

print(f"Write-here places: {write_count}")
OUT.parent.mkdir(exist_ok=True)
doc.save(str(OUT))
print(f"Saved {OUT}")
