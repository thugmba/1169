#!/usr/bin/env python3
"""Build the Session 2.1 lecture-note deck (HTML + 16:9 PDF).

Session 2.1 has comparison tables, long prompts, and per-prompt reasons that the
generic builder flattens, so it has its own layout. Prompts, reasons, and data
are read from 1169.md and the CSV so the deck stays in sync with the main page.
"""

from __future__ import annotations

import csv
import html
import re
from pathlib import Path

from pypdf import PdfReader
from weasyprint import HTML

ROOT = Path(__file__).resolve().parents[1]
MD_PATH = ROOT / "1169.md"
CSV_PATH = ROOT / "data" / "session_2_1_bubble_tea_sales.csv"
HTML_PATH = ROOT / "slides" / "session_2_1_lecture.html"
PDF_PATH = ROOT / "slides" / "session_2_1_lecture.pdf"
COVER = "session_2_1_bubble_tea_menu_hanji.png"
QUESTION = "Which drink should we remove from the menu?"


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def inline(text: str) -> str:
    """Escape text and keep **bold** from the Markdown source."""
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", esc(text))


def section_text() -> str:
    md = MD_PATH.read_text(encoding="utf-8")
    start = md.index("#### Session 2.1:")
    return md[start:md.index("#### Session 2.2:")]


def fences(text: str) -> list[str]:
    return [m.group(1) for m in re.finditer(r"```text\n([\s\S]*?)\n[ \t>]*```", text)]


def dedent_fence(block: str) -> str:
    lines = [re.sub(r"^[ \t]*>?[ \t]?", "", line) if line.lstrip().startswith(">") else line
             for line in block.splitlines()]
    pad = min((len(l) - len(l.lstrip()) for l in lines if l.strip()), default=0)
    return "\n".join(l[pad:] for l in lines)


def prompt_examples(section: str) -> list[dict]:
    """Return the four quoted prompt examples with their answer notes and reasons."""
    blocks = re.split(r"(?m)^[ \t]*> \*\*((?:Poor|Improved) prompt \d[^*]*)\*\*[ \t]*$", section)
    examples = []
    for i in range(1, len(blocks), 2):
        title, body = blocks[i], blocks[i + 1]
        body = body.split("\n\n- **")[0]
        quoted = "\n".join(re.sub(r"^[ \t]*> ?", "", l) for l in body.splitlines() if l.strip().startswith(">"))
        prompt = dedent_fence(re.search(r"```text\n([\s\S]*?)\n```", quoted).group(1))
        often = re.search(r"\*\*What the AI often answers:\*\* (.+)", quoted)
        reasons = re.findall(r"(?m)^- (.+)$", quoted.split("```")[-1])
        examples.append({"title": title, "prompt": prompt,
                         "often": often.group(1) if often else "", "reasons": reasons})
    return examples


def slide(kicker: str, title: str, subtitle: str, content: str, number: int) -> str:
    return (f'<section class="slide"><header><div class="meta"><span>{esc(kicker)}</span>'
            f'<span>Session 2.1</span></div><div class="rule"></div>'
            f'<h1>{esc(title)}</h1><p class="subtitle">{esc(subtitle)}</p></header>'
            f'<main>{content}</main><footer><span>Business AI Tools | Lecture Notes</span>'
            f'<span>Session 2.1 | Slide {number}</span></footer></section>')


def card(tag: str, title: str, body: str, kind: str = "") -> str:
    return (f'<article class="card {kind}"><div class="tag">{esc(tag)}</div>'
            f'<h2>{esc(title)}</h2>{body}</article>')


def ul(items: list[str]) -> str:
    return "<ul>" + "".join(f"<li>{inline(x)}</li>" for x in items) + "</ul>"


def ol(items: list[str]) -> str:
    return "<ol>" + "".join(f"<li>{inline(x)}</li>" for x in items) + "</ol>"


def table(head: list[str], rows: list[list[str]], highlight: dict[int, str] | None = None) -> str:
    out = '<table class="data"><thead><tr>' + "".join(f"<th>{esc(h)}</th>" for h in head) + "</tr></thead><tbody>"
    for i, row in enumerate(rows):
        cls = f' class="{highlight[i]}"' if highlight and i in highlight else ""
        out += f"<tr{cls}>" + "".join(f"<td>{inline(c)}</td>" for c in row) + "</tr>"
    return out + "</tbody></table>"


def pre(text: str, kind: str, cols: bool = False) -> str:
    return f'<div class="prompt {kind}{" cols" if cols else ""}"><pre>{esc(text)}</pre></div>'


def build() -> str:
    section = section_text()
    rows = list(csv.reader(CSV_PATH.open(encoding="utf-8")))
    examples = prompt_examples(section)
    if [e["title"].split(" (")[0] for e in examples] != ["Poor prompt 1", "Poor prompt 2", "Improved prompt 1", "Improved prompt 2"]:
        raise RuntimeError(f"Unexpected prompt examples: {[e['title'] for e in examples]}")
    exercise_fences = [dedent_fence(f) for f in fences(section.split("**Exercise 2")[1])]
    template, worked = exercise_fences[0], exercise_fences[1]

    pages = [f'<section class="cover"><img src="../images/{COVER}" alt="{esc(QUESTION)}"></section>']
    n = 2

    def add(kicker, title, subtitle, content):
        nonlocal n
        pages.append(slide(kicker, title, subtitle, content, n))
        n += 1

    add("Problem first", "What problem are we solving?",
        "Root problem: the lunch line at Mina's bubble tea shop is too long.",
        '<div class="grid three">'
        + card("Root problem", "The lunch line is too long", ul([
            "Many students arrive at lunch at the same time.",
            "Staff must prepare five different drinks, so each order takes longer.",
            "Customers wait too long for their drinks."]), "alert")
        + card("Mina's idea", "Remove one drink from the menu", ul([
            "Fewer drinks means faster preparation and a shorter line.",
            "But the shop must not lose much profit.",
            "So which drink should go?"]))
        + card("What went wrong", "AI chose the wrong drink", ul([
            'Mina asked ChatGPT: "Which drink should I remove?"',
            'ChatGPT: "Remove Mango Fruit Tea, because it sells the fewest cups."',
            "But Mango Fruit Tea earns the **most** money per cup. The question did not tell the AI what matters."]))
        + "</div>")

    add("Goal and method", "Today's goal and a three-step method",
        "Learn how to give business data to an AI tool so it reads the data correctly.",
        '<div class="grid three">'
        + card("Step 1", "Explain the data", ul([
            "What each column means.", "What unit it uses.", "How to calculate the measure you care about."]))
        + card("Step 2", "Get a table, then check one row", ul([
            "Ask the AI to show results in a table.", "Check one row yourself with a calculator."]))
        + card("Step 3", "Ask for a decision", ul([
            "State your goal.", "Ask for facts and guesses separately.", "Then ask for the recommendation."]))
        + "</div>")

    add("Practice data", "One week of sales at Mina's shop",
        "Fictional data created for this class. File: data/session_2_1_bubble_tea_sales.csv",
        table(rows[0], rows[1:])
        + '<p class="note">USD means United States dollars. Every value is per cup, except cups_sold, which is the total for the week.</p>')

    add("Part 1 | Business words", "Price, ingredient cost, and revenue",
        "Before you ask an AI to analyze sales, know what the numbers mean. Example: one cup of Brown Sugar Milk Tea.",
        '<div class="grid three">'
        + card("Word 1", "Price", '<p>What one customer pays for one cup.</p><p class="big">$5.00</p>')
        + card("Word 2", "Ingredient cost", '<p>What the shop pays for the tea, milk, sugar, and cup used to make one cup.</p><p class="big">$2.40</p>')
        + card("Word 3", "Revenue", '<p>All the money customers paid.</p><p class="formula">Revenue = cups sold x price</p>'
               '<p class="formula">420 x $5.00 = $2,100.00</p><p>Revenue is <b>not</b> the money the shop keeps. Ingredients still have to be paid for.</p>')
        + "</div>")

    add("Part 1 | Business words", "Gross profit: the money left after ingredients",
        "This is the measure Mina needs. It is the key idea of this session.",
        '<div class="grid two">'
        + card("Word 4", "Gross profit",
               '<p class="formula">Gross profit per cup = price - ingredient cost</p>'
               '<p class="formula">$5.00 - $2.40 = $2.60 per cup</p>'
               '<p class="formula">Weekly gross profit = cups sold x gross profit per cup</p>'
               '<p class="formula">420 x $2.60 = $1,092.00</p>')
        + card("Be careful", "Gross profit is not final profit", ul([
            "Gross profit subtracts **only** ingredient cost.",
            "It does not subtract rent or staff wages.",
            "So it is not the same as the money Mina takes home.",
            "This data can support gross profit, and nothing more."]), "alert")
        + "</div>")

    add("Part 2 | Why the AI was wrong", '"Sells the most" and "earns the most" are different',
        "Compare two drinks from the table.",
        table(["Drink", "Cups sold", "Gross profit per cup", "Weekly gross profit"], [
            ["Mango Fruit Tea", "80 (fewest)", "$4.20 (highest)", "$336.00"],
            ["Taro Smoothie", "110", "$1.20 (lowest)", "$132.00 (lowest)"]])
        + '<div class="grid two after-table">'
        + card("Read the table", "What it shows", ul([
            "Mango sells the fewest cups, but each cup earns $4.20.",
            "Taro sells more cups, but its ingredients are expensive. Each cup earns only $1.20."]))
        + card("The decision", "What Mina loses each week", ul([
            "Remove Mango: lose **$336.00** of gross profit.",
            "Remove Taro: lose only **$132.00**."]), "good")
        + "</div>")

    add("Part 3 | The fix", "How the three-step method fixes the question",
        "When a question gives no rule for deciding, AI often uses the easiest number to see. The question was incomplete.",
        '<div class="grid three">'
        + card("Step 1 fixes", "The definition problem", ul([
            'The AI now knows that "profit" means gross profit.', "It knows how to calculate it."]))
        + card("Step 2 fixes", "The trust problem", ul([
            "One shown calculation lets you check the math in one minute.",
            "AI tools can make arithmetic mistakes. Always check at least one row."]))
        + card("Step 3 fixes", "The decision problem", ul([
            "The AI knows the goal: shorter line, least profit lost.",
            "It must say what it is guessing, such as how long each drink takes to make."]))
        + "</div>")

    for idx, ex in enumerate(examples):
        poor = ex["title"].startswith("Poor")
        kind = "weak" if poor else "good"
        label = "Prompt to avoid" if poor else "Prompt to use"
        title, _, note = ex["title"].partition(" (")
        note = note.rstrip(")")
        if len(ex["prompt"].splitlines()) > 12:
            add("Compare examples", title, (note + ". " if note else "") + "Copy this prompt exactly.",
                pre(ex["prompt"], kind, cols=True))
            add("Compare examples", f"Why {title.lower()} works", "Each part of the prompt solves one problem.",
                '<div class="grid one">' + card("Why it works", "What each part does", ul(ex["reasons"]), "good") + "</div>")
            continue
        right = ""
        if ex["often"]:
            right += card("What the AI often answers", "A typical result", f"<p>{inline(ex['often'])}</p>", "alert")
        right += card("Why it is weak" if poor else "Why it works", "Reasons", ul(ex["reasons"]), kind if not poor else "")
        add("Compare examples", title, "Same bubble tea data. Compare what the prompt asks for.",
            '<div class="grid two">' + card(label, "The prompt", pre(ex["prompt"], kind), "")
            + f'<div class="stack">{right}</div></div>')

    add("Hour 2 | Exercise 1", "Exercise 1: Compare a poor prompt with an improved prompt",
        "Guided practice. Follow the five steps in order.",
        '<div class="grid one">' + card("Guided practice", "Steps", ol([
            "Open ChatGPT and start a **new chat**. Paste and send **Poor Prompt 1**. Write down the drink the AI chose and its reason.",
            "Start another **new chat**, so the first answer does not affect the second. Paste and send **Improved Prompt 1**.",
            "Check the Taro Smoothie row with a calculator: $6.00 - $4.80 = $1.20 per cup, and 110 x $1.20 = $132.00. Compare the AI table with the answer key. Circle any wrong row.",
            "In the same chat, paste and send **Improved Prompt 2**.",
            "For the Results section of your report, write the drink chosen by Poor Prompt 1, the drink chosen by Improved Prompt 2, and one sentence that explains why they are different."])) + "</div>")

    add("Hour 2 | Exercise 1", "Answer key: weekly gross profit",
        "Use this table to check the AI. Sorted from highest to lowest weekly gross profit.",
        table(["Drink", "Revenue", "Gross profit per cup", "Weekly gross profit"], [
            ["Classic Milk Tea", "$1,710.00", "$2.90", "$1,102.00"],
            ["Brown Sugar Milk Tea", "$2,100.00", "$2.60", "$1,092.00"],
            ["Matcha Latte", "$880.00", "$3.40", "$544.00"],
            ["Mango Fruit Tea", "$440.00", "$4.20", "$336.00"],
            ["Taro Smoothie", "$660.00", "$1.20", "$132.00"]], {4: "low"})
        + '<p class="note">Notice: Brown Sugar Milk Tea has the highest revenue, but Classic Milk Tea has the highest weekly gross profit.</p>')

    add("Hour 3 | Exercise 2", "Exercise 2: One number changes",
        "The price of milk goes up. Does Mina's decision still hold?",
        '<div class="grid two">' + card("The change", "Milk costs more", ul([
            "Four drinks use milk: Brown Sugar Milk Tea, Classic Milk Tea, Matcha Latte, and Taro Smoothie.",
            "Their ingredient cost rises by **$0.50 per cup**.",
            "Mango Fruit Tea has no milk. Its cost does not change."]))
        + card("Prompt template", "Replace each part in [square brackets]", pre(template, "plain")) + "</div>")

    add("Hour 3 | Exercise 2", "Part A: Worked example (run it)",
        "In the chat from Exercise 1, copy and send this completed prompt.",
        '<div class="grid two">' + card("Completed template", "The prompt", pre(worked, "good"))
        + card("Check the answer", "Taro Smoothie row", '<p class="formula">$6.00 - $5.30 = $0.70 per cup</p>'
               '<p class="formula">110 x $0.70 = $77.00</p>'
               + ul(["Taro Smoothie is still the lowest, so the decision holds.",
                     "Total weekly gross profit falls from $3,206.00 to $2,671.00, a drop of $535.00."]), "good") + "</div>")

    add("Hour 3 | Exercise 2", "Part B: Your turn (write it)",
        "Mina's friend says: \"Do not remove Taro Smoothie. Raise its price from $6.00 to $7.00 instead.\"",
        '<div class="grid two">' + card("Your task", "Fill in the template yourself", ul([
            "Keep the milk cost increase from Part A.",
            "Your prompt must name: the change, the drink, the values to recalculate, and the row to check.",
            "Send it in the same chat."]))
        + card("Check the answer", "Taro Smoothie at $7.00", '<p class="formula">$7.00 - $5.30 = $1.70 per cup</p>'
               '<p class="formula">110 x $1.70 = $187.00</p>'
               + ul(["Still the lowest of the five drinks.",
                     "A good AI answer lists a **guess**: the data does not show whether 110 customers will still buy Taro Smoothie at the higher price."]), "good") + "</div>")

    report = re.findall(r"(?m)^  - \*\*(Introduction|Method|Results|Conclusion):\*\* (.+)$", section)
    if [r[0] for r in report] != ["Introduction", "Method", "Results", "Conclusion"]:
        raise RuntimeError("Session 2.1 report sections not found in 1169.md")
    add("Session report", "Write your session report",
        "Use Report_template.docx in Microsoft Word. Save it as " + re.search(r"File name: `(\S+?\.docx)`", section).group(1) + " and upload it to iLearn by 23:59 on class day.",
        '<div class="grid one">' + card("Submit", "One report for this session",
            ul([f"**{name}:** {text}" for name, text in report])) + "</div>")

    add("Finish and verify", "How to know the work is complete",
        "Check your report before you hand it in.",
        '<div class="grid one">' + card("Verify", "Success check", ul([
            'You can explain in one sentence why "remove the drink with the lowest sales" was the wrong rule for Mina\'s shop.',
            "Your Part B prompt produces a table you checked with a calculator."]), "good") + "</div>")

    return ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<title>Session 2.1: Read Business Data Before Deciding - Lecture Notes</title>'
            f"{STYLE}</head><body>" + "".join(pages) + "</body></html>")


STYLE = r'''
<style>
@page { size: 16in 9in; margin: 0; }
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; color: #172033; font-family: Arial, Helvetica, sans-serif; }
body { background: #fff; }
.cover { width: 16in; height: 9in; display: flex; align-items: center; justify-content: center; overflow: hidden; background: #f8f5ed; page-break-after: always; }
.cover img { width: 100%; height: 100%; object-fit: contain; display: block; }
.slide { width: 16in; height: 9in; padding: .45in .8in .4in; display: flex; flex-direction: column; overflow: hidden; background: #fff; page-break-after: always; }
header { flex-shrink: 0; margin-bottom: .18in; }
.meta { display: flex; justify-content: space-between; color: #475569; font-size: 17px; font-weight: bold; letter-spacing: .08em; text-transform: uppercase; }
.meta span:first-child { color: #991b1b; }
.rule { height: 5px; background: #991b1b; margin: 8px 0 10px; }
h1 { margin: 0; font: bold 50px/1.08 Georgia, 'Times New Roman', serif; }
.subtitle { margin: 8px 0 0; color: #334155; font-size: 25px; line-height: 1.22; }
main { flex: 1; min-height: 0; display: flex; flex-direction: column; margin-bottom: .25in; }
.grid { display: flex; gap: 18px; flex: 1; min-height: 0; }
.grid > * { flex: 1 1 0; min-width: 0; }
.grid.after-table { margin-top: 18px; }
.stack { display: block; }
.stack > .card { margin-bottom: 14px; overflow: visible; }
.card { border: 1px solid #cbd5e1; border-radius: 14px; padding: 18px 22px; background: #fbfbfa; overflow: hidden; }
.card.alert { border-color: #fda4af; background: #fff7f7; }
.card.good { border-color: #86efac; background: #f4fdf8; }
.tag { margin: 0 0 6px; color: #991b1b; font-size: 17px; font-weight: 800; letter-spacing: .08em; text-transform: uppercase; }
h2 { margin: 0 0 10px; font: bold 28px/1.12 Georgia, 'Times New Roman', serif; }
p, li { font-size: 24px; line-height: 1.3; }
p { margin: 0 0 10px; }
ul, ol { margin: 0; padding-left: 28px; }
li { margin: 0 0 8px; }
.big { font: bold 54px/1.1 Georgia, serif; color: #991b1b; margin-top: 14px; }
.formula { font: bold 24px/1.3 'Courier New', monospace; background: #f1f5f9; border: 1px solid #cbd5e1; border-radius: 8px; padding: 8px 12px; }
.note { margin-top: 14px; color: #334155; font-size: 21px; }
.prompt { border: 1px solid #94a3b8; border-radius: 10px; background: #f1f5f9; padding: 12px 16px; }
.prompt.weak { border-color: #fda4af; background: #fff1f2; }
.prompt.good { border-color: #86efac; background: #ecfdf5; }
.prompt.cols { flex: 1; column-count: 2; column-gap: 34px; column-rule: 1px solid #a7f3d0; }
.prompt pre { margin: 0; white-space: pre-wrap; overflow-wrap: anywhere; font: 20px/1.24 'Courier New', monospace; color: #172033; }
table.data { width: 100%; border-collapse: collapse; font-size: 24px; }
table.data th { background: #172033; color: #fff; text-align: left; font-size: 21px; padding: 10px 12px; }
table.data td { border: 1px solid #cbd5e1; padding: 10px 12px; }
table.data tr:nth-child(even) td { background: #f1f5f9; }
table.data tr.low td { background: #fff1f2; font-weight: bold; }
footer { height: .42in; flex-shrink: 0; border-top: 1px solid #cbd5e1; padding-top: 8px; display: flex; justify-content: space-between; color: #475569; font-size: 16px; }
</style>'''


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
    print(f"Session 2.1: {len(reader.pages)} pages -> {PDF_PATH}")


if __name__ == "__main__":
    main()
