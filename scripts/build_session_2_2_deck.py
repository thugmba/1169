#!/usr/bin/env python3
"""Build the Session 2.2 lecture-note deck (HTML + 16:9 PDF).

Reuses the layout helpers of the Session 2.1 builder. Prompts, reasons, report
items, and the file name are read from 1169.md so the deck stays in sync.
"""

from __future__ import annotations

import re
from pathlib import Path

from pypdf import PdfReader
from weasyprint import HTML

import build_session_2_1_deck as d
from chat_box import CHAT_CSS, chat

ROOT = Path(__file__).resolve().parents[1]
MD_PATH = ROOT / "1169.md"
HTML_PATH = ROOT / "slides" / "session_2_2_lecture.html"
PDF_PATH = ROOT / "slides" / "session_2_2_lecture.pdf"
COVER = "session_2_2_return_policy_hanji.png"
QUESTION = "Does this AI reply follow our return policy?"

POLICY = [
    ["1", "Unopened item, with receipt, returned within 14 days of delivery", "Refund"],
    ["2", "Item reported damaged within 7 days of delivery", "Replacement"],
    ["3", "Opened item that is not damaged", "Not eligible for a refund"],
    ["4", "Receipt or a needed detail is missing", "Information needed: ask for the order number"],
]


def section_text() -> str:
    md = MD_PATH.read_text(encoding="utf-8")
    start = md.index("#### Session 2.2:")
    return md[start:md.index("#### Session 2.3:")]


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
    emails = [re.match(r"^\s*\|\s*([A-D])\s*\|\s*([^|]+)\|\s*(\d+\.\d\d)\s*\|\s*([^|]+)\|", line)
              for line in section.splitlines()]
    emails = [[m.group(1), m.group(2).strip(), "$" + m.group(3), m.group(4).strip()] for m in emails if m]
    if len(emails) != 4:
        raise RuntimeError("Customer email table not found")

    pages = [f'<section class="cover"><img src="../images/{COVER}" alt="{d.esc(QUESTION)}"></section>']
    n = 2

    def add(kicker, title, subtitle, content):
        nonlocal n
        pages.append(d.slide(kicker, title, subtitle, content, n).replace("Session 2.1", "Session 2.2"))
        n += 1

    add("Problem first", "What problem are we solving?",
        "Root problem: Leo spends about two hours a day answering return emails.",
        '<div class="grid three">'
        + d.card("Root problem", "Too many return emails", d.ul([
            "Leo runs a small online phone accessory shop.",
            "He receives about 20 return emails a day.",
            "Answering them takes about two hours."]), "alert")
        + d.card("Leo's idea", "Let AI draft the replies", d.ul([
            "AI could write a first draft of each reply.",
            "Leo would only check and send.",
            "But every reply must follow the return policy."]))
        + d.card("What went wrong", "Friendly, but wrong", d.ul([
            'Leo asked: "Please reply to these customer emails."',
            "The AI promised refunds that break the policy.",
            "Two wrong promises were worth **$70.00**. The prompt did not include the policy."]))
        + "</div>")

    add("Goal and method", "Today's goal and a three-step method",
        "Learn how to improve an AI answer step by step until it follows the rules.",
        '<div class="grid three">'
        + d.card("Step 1", "Give the AI the rules", d.ul([
            "Paste the return policy.", 'Tell the AI to "use only" that policy.']))
        + d.card("Step 2", "Check every answer", d.ul([
            "Compare each AI result with the answer key.", "Write down one error."]))
        + d.card("Step 3", "Change one instruction", d.ul([
            "Fix only that error.", "Run the same emails again.", "Record it in a change log."]))
        + "</div>")

    add("Practice data", "Leo's return policy",
        "Fictional data created for this class. File: data/session_2_2_return_emails.csv",
        d.table(["Rule", "Situation", "Result"], POLICY)
        + '<p class="note">The AI must follow these four rules, not its own idea of what is fair.</p>')

    add("Practice data", "Four customer emails",
        "Each email asks for something. The policy decides the answer.",
        d.table(["Case", "Item", "Price", "Email"], emails))

    add("Part 1 | Policy words", "Return policy, refund, and replacement",
        "Before you ask an AI to answer customers, know what the policy words mean.",
        '<div class="grid three">'
        + d.card("Word 1", "Return policy", "<p>The shop's written rules about returns.</p>"
                 "<p>The AI must follow these rules, not its own idea of what is fair.</p>")
        + d.card("Word 2", "Refund", "<p>The customer gets the money back.</p>"
                 '<p class="formula">Phone case returned: $25.00 back</p>')
        + d.card("Word 3", "Replacement", "<p>The customer gets a new item instead of money.</p>"
                 "<p>Example: a cracked screen protector is replaced with a new one.</p>")
        + "</div>")

    add("Part 1 | Policy words", "Return window and order number",
        "Example: an item delivered on March 1.",
        '<div class="grid two">'
        + d.card("Word 4", "Return window", "<p>The number of days a customer has to ask.</p>"
                 '<p class="formula">Refund window: March 1 + 14 days = March 15</p>'
                 '<p class="formula">Damage window: March 1 + 7 days = March 8</p>')
        + d.card("Word 5", "Order number", "<p>The code that identifies a purchase, such as #4471.</p>"
                 + d.ul(["When a receipt is missing, the shop uses the order number to check the purchase.",
                         "The shop checks first, and decides after."]))
        + "</div>")

    add("Part 2 | Why the AI was wrong", '"Polite" and "correct" are different',
        "Compare what the AI promised with what the policy says.",
        d.table(["Case", "What the AI promised", "What the policy says", "Rule"], [
            ["A", "Refund", "Refund", "1"],
            ["B", "Refund", "Replacement", "2"],
            ["C", "Refund ($40.00)", "Not eligible for a refund", "3"],
            ["D", "Refund ($30.00)", "Information needed: ask for the order number", "4"]], {2: "low", 3: "low"})
        + '<div class="grid two after-table">'
        + d.card("Read the table", "Only one case is correct", d.ul([
            "Only Case A is correct. B, C, and D are wrong.",
            "C and D are refunds the shop should not promise."]))
        + d.card("The cost", "Two wrong refund promises", '<p class="formula">$40.00 + $30.00 = $70.00</p>'
                 + d.ul(["Without the policy, the AI used a general idea: say yes to the customer."]), "alert")
        + "</div>")

    add("Part 3 | The fix", "Improve the prompt one change at a time",
        "If you change many instructions at once, you do not know which change helped.",
        '<div class="grid two">'
        + d.card("Change log", "Record each test",
                 d.table(["Weakness", "One change", "Result"], [[
                     "The AI promised refunds to C and D",
                     'Added the policy and "Use only the policy below"',
                     "C became Not eligible; D became Information needed"]]))
        + d.card("Check before you send", "AI can still make mistakes", d.ul([
            "Change one instruction, run the same emails, compare.",
            "Compare each result with the policy before a reply goes to a customer."]), "good")
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
            add("Compare examples", title, "Same policy and emails. Compare what the prompt asks for.",
                '<div class="grid two">' + chat(ex["prompt"], kind, label) + f'<div class="stack">{side}</div></div>')
            continue
        add("Compare examples", title, (note + ". " if note else "") + "Copy this prompt exactly.",
            chat(ex["prompt"], kind, label, cols=visual_lines(ex["prompt"], 105) > 13))
        add("Compare examples", f"{reasons_title}: {title.lower()}", "Each part of the prompt matters.",
            f'<div class="grid one"><div class="stack">{side}</div></div>')

    add("Hour 2 | Exercise 1", "Exercise 1: Find the errors, then fix them",
        "Guided practice. Follow the five steps in order.",
        '<div class="grid one">' + d.card("Guided practice", "Steps", d.ol([
            "Open ChatGPT and start a **new chat**. Paste and send **Poor Prompt 1**. Write down the result the AI promised for each case.",
            "Compare the AI results with the answer key. Count the wrong cases, and add the prices of refunds the shop should not promise.",
            "Start another **new chat**. Paste and send **Improved Prompt 1**. Compare the AI table with the answer key and circle any wrong row.",
            "In the same chat, paste and send **Improved Prompt 2**. Check that the reply to Case D asks for the order number and does not promise a refund.",
            "For the Results section of your report, write one change log row: the weakness, the one change, and the result."])) + "</div>")

    add("Hour 2 | Exercise 1", "Answer key: the correct result for each email",
        "Use this table to check the AI.",
        d.table(["Case", "Correct result", "Rule", "Reason"], [
            ["A", "Refund", "1", "Unopened, receipt, 10 days after delivery (within 14)"],
            ["B", "Replacement", "2", "Reported damaged 1 day after delivery (within 7)"],
            ["C", "Not eligible", "3", "Opened and used, not damaged"],
            ["D", "Information needed", "4", "Receipt is missing; ask for the order number"]])
        + '<p class="note">Poor Prompt 1 usually gets B, C, and D wrong. The wrong refund promises for C and D cost $70.00.</p>')

    add("Hour 3 | Exercise 2", "Exercise 2: Test one change on a new email",
        "New emails keep arriving. Does the improved prompt still work?",
        '<div class="grid two">' + d.card("How it works", "Find one mistake, fix it with one instruction", d.ul([
            "Send the new email with the same policy.",
            "If the AI makes a mistake, name it.",
            "Add **one** new instruction that fixes it.",
            "Check the result against the policy."]))
        + chat(template, "plain", "Template - replace each [part], then send") + "</div>")

    add("Hour 3 | Exercise 2", "Part A: Worked example (run it)",
        "In the chat from Exercise 1, copy and send this completed prompt.",
        '<div class="grid two">' + chat(worked, "good", "Part A - copy and send")
        + d.card("Check the answer", "Case E", d.ul([
            "Result: **Information needed** (Rule 4).",
            "The receipt is missing, so the shop must first check order #4471.",
            "The reply says what the shop will check and does not promise a refund."]), "good") + "</div>")

    add("Hour 3 | Exercise 2", "Part B: Your turn (write it)",
        'Case F: "My power bank arrived 9 days ago. Today I noticed that the case is cracked. Can you send me a new one?"',
        '<div class="grid two">' + d.card("Your task", "Fill in the template yourself", d.ul([
            "In a test, the AI felt sorry for the customer and offered a replacement.",
            "Your prompt must include the email, the mistake, and one new instruction that fixes it.",
            "Send it in the same chat."]))
        + d.card("Check the answer", "Count the days", '<p class="formula">Reported 9 days after delivery</p>'
                 '<p class="formula">Limit in Rule 2: 7 days. 9 > 7</p>'
                 + d.ul(["Result: **Not eligible** under Rule 2. No replacement promise.",
                         'A fix that works: "Count the days since delivery and compare them with the limit in the rule before you decide."']),
                 "good") + "</div>")

    report = re.findall(r"(?m)^  - \*\*(Introduction|Method|Results|Conclusion):\*\* (.+)$", section)
    if [r[0] for r in report] != ["Introduction", "Method", "Results", "Conclusion"]:
        raise RuntimeError("Session 2.2 report sections not found in 1169.md")
    file_name = re.search(r"File name: `(\S+?\.docx)`", section).group(1)
    add("Session report", "Write your session report",
        f"Use Report_template.docx in Microsoft Word. Save it as {file_name} and upload it to iLearn by 23:59 on class day.",
        '<div class="grid one">' + d.card("Submit", "One report for this session",
                                          d.ul([f"**{name}:** {text}" for name, text in report])) + "</div>")

    success = re.search(r"(?m)^- \*\*Success check:\*\* (.+)$", section).group(1)
    add("Finish and verify", "How to know the work is complete", "Check your report before you hand it in.",
        '<div class="grid one">' + d.card("Verify", "Success check", d.ul([success]), "good") + "</div>")

    return ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<title>Session 2.2: Improve AI Results by Testing One Change - Lecture Notes</title>'
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
    print(f"Session 2.2: {len(reader.pages)} pages -> {PDF_PATH}")


if __name__ == "__main__":
    main()
