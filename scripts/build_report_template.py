#!/usr/bin/env python3
"""Rewrite the guidance text in Report_template.docx.

Keeps the template's title block, header, footer, and styles. Replaces everything
after the student name with the four report sections and detailed guidance
written for beginner, non-native English speakers. Guidance is gray italic so
students can see what to delete.
"""

from __future__ import annotations

import re
import shutil
import tempfile
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
DOCX = ROOT / "Report_template.docx"

FONT = '<w:rFonts w:eastAsia="Malgun Gothic" w:cs="Times New Roman"/>'
GRAY = '<w:color w:val="595959"/>'


def run(text: str, bold=False, italic=True, mono=False, gray=True) -> str:
    props = FONT if not mono else '<w:rFonts w:ascii="Courier New" w:hAnsi="Courier New" w:cs="Courier New"/>'
    props += "<w:b/>" if bold else ""
    props += "<w:i/>" if italic else ""
    props += GRAY if gray else ""
    props += '<w:sz w:val="20"/><w:szCs w:val="20"/>' if mono else ""
    return f'<w:r><w:rPr>{props}</w:rPr><w:t xml:space="preserve">{escape(text)}</w:t></w:r>'


def para(*runs: str, indent=0, hanging=0, after=120, shade=False) -> str:
    ind = f'<w:ind w:left="{indent}" w:hanging="{hanging}"/>' if indent else '<w:ind w:firstLine="0"/>'
    shd = '<w:shd w:val="clear" w:color="auto" w:fill="F2F2F2"/>' if shade else ""
    return (f'<w:p><w:pPr>{shd}<w:spacing w:after="{after}"/>{ind}<w:jc w:val="left"/></w:pPr>'
            + "".join(runs) + "</w:p>")


def text(s: str) -> str:
    """Paragraph of guidance. **bold** marks a label."""
    parts = re.split(r"(\*\*.+?\*\*)", s)
    return para(*[run(p[2:-2], bold=True) if p.startswith("**") else run(p) for p in parts if p])


def item(s: str, mark: str = "-") -> str:
    parts = re.split(r"(\*\*.+?\*\*)", s)
    runs = [run(f"{mark}\t")] + [run(p[2:-2], bold=True) if p.startswith("**") else run(p) for p in parts if p]
    return para(*runs, indent=567, hanging=283, after=60)


def example(lines: list[str]) -> str:
    """One shaded paragraph; the lines are joined so Word wraps them naturally."""
    return para(run(" ".join(lines), italic=False), indent=284, after=120, shade=True)


def code(lines: list[str]) -> str:
    return "".join(para(run(l, italic=False, mono=True), indent=284, after=0, shade=True) for l in lines) + para(run(""), after=60)


def heading(template_heading: str, title: str) -> str:
    out = re.sub(r"<w:t>[^<]*</w:t>", f"<w:t>{escape(title)}</w:t>", template_heading)
    return re.sub(r' w14:(paraId|textId)="[^"]*"', "", out)


def body(h: str) -> str:
    s = []
    s.append(text("**How to use this template** (delete this gray text before you submit)"))
    for t in [
        'Replace "Title" with the session number and session name. Example: "Session 2.1: Read Business Data Before Deciding."',
        'Replace "S1234567" with your student ID and "James" with your full name.',
        "Write your report in Microsoft Word. Save a copy with a new file name: FirstName_StudentID_W#_Keyword.docx. FirstName is your first name in English, StudentID is your student ID, W# is the week of the 16-week semester (W1 to W16), and Keyword is one English word you choose for the topic. Use underscores, not spaces. Example: James_S1234567_W5_Menu.docx.",
        "Upload the report to iLearn by 23:59 on the day of the class.",
        "Under each heading, the gray text tells you what to write. Read it, then delete it and write your own text in normal black font.",
        "Open the session on the course page and find its **Report** list. It tells you exactly what to put in each section for that session.",
        "Write in simple, clear English. Short sentences are good. You do not need difficult words. A clear, correct report is better than a long one.",
        "Expected length: about 2 to 4 pages, including prompts, tables, and screenshots.",
        "Never include real personal information, such as a real customer's name, phone number, or account number.",
    ]:
        s.append(item(t))

    s.append(h("Introduction"))
    s.append(text("**What this section is for:** Tell the reader what business problem you worked on and what you wanted to achieve. Someone who did not attend the class should understand the situation after reading it."))
    s.append(text("**Write one paragraph of 3 to 5 sentences that answers these questions:**"))
    for t in [
        "**Situation:** Who is the business, and what is happening? (1 to 2 sentences)",
        "**Problem:** What is going wrong, or what decision must be made? (1 sentence)",
        "**Goal:** What did you want to find out or produce with AI in this session? (1 sentence)",
    ]:
        s.append(item(t))
    s.append(text("**Tips:** Use your own words. Do not copy the course page. Include one or two key numbers from the case if they help the reader understand the problem."))
    s.append(text("**Example (Session 2.1):**"))
    s.append(example([
        "Mina runs a small bubble tea shop near a university. At lunch, the line is too long because staff",
        "must prepare five different drinks. Mina wants to remove one drink from the menu without losing",
        "much profit. My goal was to write prompts that help AI find the drink that loses the least gross",
        "profit, and to check whether the AI answer is correct.",
    ]))

    s.append(h("Method"))
    s.append(text("**What this section is for:** Show exactly what you asked the AI, so that another student could repeat your work and get a similar result."))
    s.append(text("**For every prompt you used, in the order you used it, write these four things:**"))
    for i, t in enumerate([
        '**Label:** "Prompt 1," "Prompt 2," and so on.',
        '**Where it was used:** the exercise and part. Example: "Exercise 1, Step 2."',
        "**The full prompt text:** copy it exactly. Do not shorten it or summarize it. Put it in a gray box or in Courier New font so the reader can see it is a prompt, not your own writing.",
        '**Why you wrote it this way:** one sentence. Example: "I gave the formula for gross profit so the AI would not use a different meaning of profit."',
    ], start=1):
        s.append(item(t, f"{i}."))
    s.append(text("**Tips:** If you changed a prompt after a bad answer, include both versions and write what you changed. Include the data you pasted into the prompt, or write the file name you attached."))
    s.append(text("**Example (Session 2.1):**"))
    s.append(example(["Prompt 2 (Exercise 1, Step 2: Improved Prompt 1)"]))
    s.append(code([
        "I run a small bubble tea shop. Below is one week of sales data.",
        "What each column means: ...",
        "(copy the full prompt here, not just the first lines)",
    ]))
    s.append(example(["Why: I explained each column and gave the gross profit formula so the AI would read the data",
                      "correctly and calculate the right measure."]))

    s.append(h("Results"))
    s.append(text("**What this section is for:** Show what the AI produced and prove that you checked it. This is the most important section. A report that only copies the AI answer, without any check, is not complete."))
    s.append(text("**For each prompt, show:**"))
    for t in [
        '**The AI answer:** paste only the important part, or add a screenshot. Do not paste the whole chat. Give each screenshot a number and a title below it. Example: "Figure 1: AI answer to Prompt 1."',
        '**Your check:** show how you checked the answer. Redo at least one calculation by hand, or compare the answer with the answer key or the source data. Write the calculation, not just "I checked it."',
        "**Errors:** if the AI made a mistake, write what the AI said, what the correct answer is, and how you found the mistake. Finding an AI error is a good result, not a bad one.",
    ]:
        s.append(item(t))
    s.append(text('**Tables:** give every table a number and a title above it. Example: "Table 1: Weekly gross profit by drink." In your text, refer to it by number: "As Table 1 shows, ..."'))
    s.append(text("**Example check (Session 2.1):**"))
    s.append(example([
        "I checked the Taro Smoothie row with a calculator: $6.00 - $4.80 = $1.20 per cup, and",
        "110 x $1.20 = $132.00. The AI table showed the same value. Poor Prompt 1 chose Mango Fruit Tea",
        "because it sold the fewest cups, but Table 1 shows that Mango Fruit Tea earns $336.00 per week,",
        "more than Taro Smoothie.",
    ]))

    s.append(h("Conclusion"))
    s.append(text("**What this section is for:** Give your final answer and say how sure you are. A good conclusion is short and honest."))
    s.append(text("**Write one paragraph of 4 to 6 sentences that includes:**"))
    for t in [
        "**Your recommendation or final answer** in one or two sentences.",
        "**One fact** from the data or the checked results that supports it.",
        "**One uncertainty:** something the data does not show that could change the answer.",
        "**One lesson about prompting:** what you will do differently the next time you ask AI about a similar problem.",
    ]:
        s.append(item(t))
    s.append(text("**Example (Session 2.1):**"))
    s.append(example([
        "Mina should remove Taro Smoothie from the lunch menu. It has the lowest weekly gross profit,",
        "$132.00, so removing it loses the least money. However, the data does not show how long each",
        "drink takes to make, so I cannot be sure this change will shorten the line the most. Next time,",
        "I will tell the AI my decision rule before I ask for a recommendation.",
    ]))

    s.append(text("**Before you submit, check every item** (then delete this list):"))
    for t in [
        "The title, your student ID, and your name are filled in.",
        "All four sections are written, and all gray guidance text is deleted.",
        "The file name follows FirstName_StudentID_W#_Keyword.docx, for example James_S1234567_W5_Menu.docx.",
        "You will upload the file to iLearn by 23:59 on the day of the class.",
        "Every prompt is copied in full, in the order you used it.",
        "At least one AI result is checked by you, and the check is written out.",
        "Every table and figure has a number and a title.",
        "The recommendation names one supporting fact and one uncertainty.",
    ]:
        s.append(item(t, "[ ]"))
    return "".join(s)


def main() -> None:
    with zipfile.ZipFile(DOCX) as z:
        files = {n: z.read(n) for n in z.namelist()}
    xml = files["word/document.xml"].decode("utf-8")
    paras = list(re.finditer(r"<w:p[ >].*?</w:p>", xml, flags=re.S))
    first_heading = next(p for p in paras if 'w:pStyle w:val="Heading1"' in p.group(0))
    template_heading = first_heading.group(0)
    sect = xml.index("<w:sectPr")
    xml = xml[:first_heading.start()] + body(lambda t: heading(template_heading, t)) + xml[sect:]
    files["word/document.xml"] = xml.encode("utf-8")
    tmp = Path(tempfile.mkstemp(suffix=".docx")[1])
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in files.items():
            z.writestr(name, data)
    shutil.move(tmp, DOCX)
    print(f"Updated {DOCX}")


if __name__ == "__main__":
    main()
