#!/usr/bin/env python3
"""Build the Session 2.4 lecture-note deck (HTML + 16:9 PDF).

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
CSV_PATH = ROOT / "data" / "session_2_4_interview_notes.csv"
HTML_PATH = ROOT / "slides" / "session_2_4_lecture.html"
PDF_PATH = ROOT / "slides" / "session_2_4_lecture.pdf"
COVER = "session_2_4_budget_app_profiles_hanji.png"
QUESTION = "What do our users really need from this app?"


def section_text() -> str:
    md = MD_PATH.read_text(encoding="utf-8")
    start = md.index("#### Session 2.4:")
    return md[start:md.index("### Module 3:")]


def visual_lines(text: str, width: int) -> int:
    return sum(max(1, -(-len(line) // width)) for line in text.splitlines())


def build() -> str:
    section = section_text()
    examples = d.prompt_examples(section)
    titles = [e["title"].split(" (")[0] for e in examples]
    if titles != ["Poor prompt 1", "Poor prompt 2", "Improved prompt 1", "Improved prompt 2"]:
        raise RuntimeError(f"Unexpected prompt examples: {titles}")
    ex2 = section.split("**Exercise 2")[1]
    template, worked = [d.dedent_fence(f) for f in d.fences(ex2)][:2]
    notes = list(csv.DictReader(CSV_PATH.open(encoding="utf-8")))
    if len(notes) != 6:
        raise RuntimeError("Expected six interview notes")

    pages = [f'<section class="cover"><img src="../images/{COVER}" alt="{d.esc(QUESTION)}"></section>']
    n = 2

    def add(kicker, title, subtitle, content):
        nonlocal n
        pages.append(d.slide(kicker, title, subtitle, content, n).replace("Session 2.1", "Session 2.4"))
        n += 1

    add("Problem first", "What problem are we solving?",
        "Root problem: few people try the team's budgeting app.",
        '<div class="grid three">'
        + d.card("Root problem", "Few people try the app", d.ul([
            "A student team is building a budgeting app.",
            "**60** students saw the ad. Only **12** tried the app.",
            'The ad said "Take control of your money!" and spoke to no real need.']), "alert")
        + d.card("The team's idea", "Let AI create personas", d.ul([
            "AI could describe the customers and write better ads.",
            "But the profiles must come from real evidence."]))
        + d.card("What went wrong", "An invented customer", d.ul([
            'ChatGPT created "Sarah, 24, marketing assistant, earns $3,500, loves yoga, syncs her bank accounts."',
            "None of it came from the six interviews.",
            "The ad promised **bank syncing**, which the app does not have."]))
        + "</div>")

    add("Goal and method", "Today's goal and a three-step method",
        "Use AI to build customer profiles from evidence, not from imagination.",
        '<div class="grid three">'
        + d.card("Step 1", "Give the AI the evidence", d.ul([
            "Paste the interview notes and product facts.", 'Tell the AI to "use only" them.']))
        + d.card("Step 2", "Require a note for every detail", d.ul([
            "Each need and barrier cites a note ID.", "Check each citation yourself."]))
        + d.card("Step 3", "Check every message", d.ul([
            "Use only available features.", 'Label untested claims "Hypothesis."']))
        + "</div>")

    add("Practice data", "Product facts",
        "Fictional data created for this class. File: data/session_2_4_interview_notes.csv",
        '<div class="grid two">'
        + d.card("Available", "What the app can do", d.ul([
            "Manual expense entry", "A weekly spending view", "Bill reminders"]), "good")
        + d.card("Not available", "What the app cannot do (yet)", d.ul([
            "Bank account linking", "Price: not set yet"]), "alert")
        + "</div>")

    add("Practice data", "Six interview notes",
        "This is the evidence. Every profile detail must point to one of these notes.",
        d.table(["Note", "What the person said"], [[r["note_id"], r["interview_note"]] for r in notes]))

    add("Part 1 | Customer words", "Evidence, need, and barrier",
        "Before you ask an AI to describe customers, know what these words mean.",
        '<div class="grid three">'
        + d.card("Word 1", "Evidence", "<p>What real people said or did.</p><p>Here: the six interview notes, N1 to N6.</p>")
        + d.card("Word 2", "Need", "<p>The progress a person wants to make.</p>"
                 '<p class="formula">N1: know how much I can spend before Friday</p>')
        + d.card("Word 3", "Barrier", "<p>What stops a person from trying a product.</p>"
                 '<p class="formula">N6: no bank connection</p>')
        + "</div>")

    add("Part 1 | Customer words", "Customer profile and hypothesis",
        "Each example uses the budgeting app.",
        '<div class="grid two">'
        + d.card("Word 4", "Customer profile", "<p>A short summary of one group with the same need, supported by "
                 "<b>at least two notes</b>.</p>"
                 '<p class="formula">Pay changes, wants safe weekly spending (N1, N2)</p>')
        + d.card("Word 5", "Hypothesis", "<p>A claim the team believes but has not tested yet.</p>"
                 "<p>Example: \"A weekly spending view will help people with changing pay.\" "
                 "Label it as a hypothesis, not a fact.</p>")
        + "</div>")

    add("Part 2 | Why the AI was wrong", '"Sounds real" and "comes from evidence" are different',
        "Check each detail of the AI persona against the notes.",
        d.table(["AI persona detail", "Supporting note", "Result"], [
            ["Sarah, 24", "None", "Invented"],
            ["Marketing assistant", "None", "Invented"],
            ["Earns $3,500 a month", "None", "Invented"],
            ["Loves yoga", "None", "Invented"],
            ["Syncs her bank accounts", "N6 says the opposite; the app has no bank linking", "Wrong"]], {4: "low"})
        + '<div class="grid two after-table">'
        + d.card("Evidence count", "0 of 5 details", '<p class="formula">0 of 5 details come from the interviews</p>'
                 + d.ul(["One detail goes against the evidence."]), "alert")
        + d.card("Why", "Typical, not real", d.ul([
            "Without notes, the AI filled the profile with typical marketing details.",
            "The bank-syncing ad promised a feature the app does not have."]))
        + "</div>")

    add("Part 3 | The fix", "How the three-step method fixes the profile",
        "The instructor runs the prompts below and compares the answers.",
        '<div class="grid three">'
        + d.card("Step 1 fixes", "The evidence problem", d.ul([
            "The AI can only use what people actually said."]))
        + d.card("Step 2 fixes", "The trust problem", d.ul([
            "Every need and barrier has a note ID you can check in seconds.",
            "A detail with no note becomes a question for the next interview."]))
        + d.card("Step 3 fixes", "The false-promise problem", d.ul([
            "Each message names the feature it uses.", "Unavailable features cannot appear."]))
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
            add("Compare examples", title, "Same notes and product facts. Compare what the prompt asks for.",
                '<div class="grid two">' + chat(ex["prompt"], kind, label) + f'<div class="stack">{side}</div></div>')
            continue
        add("Compare examples", title, (note + ". " if note else "") + "Copy this prompt exactly.",
            chat(ex["prompt"], kind, label, cols=visual_lines(ex["prompt"], 105) > 13))
        add("Compare examples", f"{reasons_title}: {title.lower()}", "Each part of the prompt matters.",
            f'<div class="grid one"><div class="stack">{side}</div></div>')

    add("Hour 2 | Exercise 1", "Exercise 1: Build profiles from evidence",
        "Guided practice. Follow the five steps in order.",
        '<div class="grid one">' + d.card("Guided practice", "Steps", d.ol([
            "Open ChatGPT and start a **new chat**. Paste and send **Poor Prompt 1**. Count the details in each persona and how many come from the notes.",
            "Start another **new chat**. Paste and send **Improved Prompt 1**.",
            "Check every note ID: open the note and confirm it says what the AI claims. Compare with the answer key.",
            "In the same chat, paste and send **Improved Prompt 2**. Check that no message mentions bank syncing, savings, or a price.",
            'For the Results section of your report, write the evidence count (for example, "0 of 5 details from notes") and the two profiles with note IDs.'])) + "</div>")

    add("Hour 2 | Exercise 1", "Answer key: two profiles",
        "Use this table to check the AI. N5 and N6 can apply to both profiles if the note ID is cited.",
        d.table(["Profile", "Need", "Notes", "Barrier", "Feature that fits"], [
            ["A", "Pay changes; wants to know safe spending for the week", "N1, N2",
             "Tracking must take less time than a spreadsheet (N5)", "Weekly spending view"],
            ["B", "Forgets bill dates; wants a reminder before the due date", "N3, N4",
             "Does not want to connect a bank account (N6)", "Bill reminders, with manual entry and no bank linking"]]))

    add("Hour 3 | Exercise 2", "Exercise 2: Place new interview notes",
        "The team runs two more interviews. Where does each new note belong?",
        '<div class="grid two">' + d.card("How it works", "Fit, or wait for more evidence", d.ul([
            "Compare the new note with each profile's notes.",
            "A profile needs at least **two** notes with the same need.",
            'If no feature meets the need, write "Not available."',
            "Never promise a feature the app does not have."]))
        + chat(template, "plain", "Template - replace each [part], then send") + "</div>")

    add("Hour 3 | Exercise 2", "Part A: Worked example (run it)",
        "In the chat from Exercise 1, copy and send this completed prompt.",
        '<div class="grid two">' + chat(worked, "good", "Part A - copy and send")
        + d.card("Check the answer", "N7: splitting costs", d.ul([
            "Fits **neither** profile: the need does not match N1-N2 or N3-N4.",
            "Only one note, so it cannot be a new profile yet.",
            "Splitting costs is **Not available**. Ask about it in the next interviews."]), "good") + "</div>")

    add("Hour 3 | Exercise 2", "Part B: Your turn (write it)",
        'N8: "I tutor and work at a cafe, so my pay comes on different days. On Friday I decide if I can go out."',
        '<div class="grid two">' + d.card("Your task", "Fill in the template yourself", d.ul([
            "Include the note ID and text.",
            "Include the rule about two notes.",
            "Send it in the same chat."]))
        + d.card("Check the answer", "N8 fits Profile A", d.ul([
            "Like N1 and N2, pay comes on different days, and the person wants to know weekly spending.",
            "Profile A now has three notes: **N1, N2, N8**.",
            "Feature that fits: **weekly spending view**."]), "good") + "</div>")

    report = re.findall(r"(?m)^  - \*\*(Introduction|Method|Results|Conclusion):\*\* (.+)$", section)
    if [r[0] for r in report] != ["Introduction", "Method", "Results", "Conclusion"]:
        raise RuntimeError("Session 2.4 report sections not found in 1169.md")
    file_name = re.search(r"File name: `(\S+?\.docx)`", section).group(1)
    add("Session report", "Write your session report",
        f"Use Report_template.docx in Microsoft Word. Save it as {file_name} and upload it to iLearn by 23:59 on class day.",
        '<div class="grid one">' + d.card("Submit", "One report for this session",
                                          d.ul([f"**{name}:** {text}" for name, text in report])) + "</div>")

    success = re.search(r"(?m)^- \*\*Success check:\*\* (.+)$", section).group(1)
    add("Finish and verify", "How to know the work is complete", "Check your report before you hand it in.",
        '<div class="grid one">' + d.card("Verify", "Success check", d.ul([success]), "good") + "</div>")

    return ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<title>Session 2.4: Build Customer Profiles from Evidence - Lecture Notes</title>'
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
    print(f"Session 2.4: {len(reader.pages)} pages -> {PDF_PATH}")


if __name__ == "__main__":
    main()
