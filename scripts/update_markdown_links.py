import re

src = "1169.md"

with open(src, "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    new_lines.append(line)
    
    m = re.match(r'^####\s+Session\s+(\d+\.\d+):', line.strip())
    if m:
        sess_num = m.group(1)
        x, y = sess_num.split('.')
        pdf_path = f"slides/session_{x}_{y}_lecture.pdf"
        
        # Check if already present in next 3 lines
        already_has = False
        for offset in range(1, min(4, len(lines) - i)):
            if "Lecture Presentation" in lines[i + offset]:
                already_has = True
                break
        
        if not already_has:
            # Determine line ending from current line
            newline = "\r\n" if line.endswith("\r\n") else "\n"
            new_lines.append(newline)
            new_lines.append(f"* **Lecture Presentation:** [Download Slides (PDF)]({pdf_path}){newline}")
    i += 1

with open(src, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("Line-by-line update complete.")
