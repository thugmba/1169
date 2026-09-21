import re
import json

def parse_markdown(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split into sessions
    session_pattern = r'####\s+Session\s+(\d+\.\d+):?\s*([^\n\r]+)'
    matches = list(re.finditer(session_pattern, content))
    
    sessions = []
    for i, match in enumerate(matches):
        sess_num = match.group(1)
        sess_title = match.group(2).strip()
        # Clean title if it has markdown links
        sess_title = re.sub(r'\[.*?\]\(.*?\)', '', sess_title).strip()
        sess_title = re.sub(r'&nbsp;.*', '', sess_title).strip()
        
        start_pos = match.start()
        end_pos = matches[i+1].start() if i+1 < len(matches) else len(content)
        sess_block = content[start_pos:end_pos]
        
        # Module lookup
        mod_num = int(sess_num.split('.')[0])
        mod_titles = {
            1: "Module 1: Mastering ChatGPT Fundamentals",
            2: "Module 2: Business Data, Evaluation & Project Planning",
            3: "Module 3: Hands-On Business Functions",
            4: "Module 4: Everyday Workflows & Your AI Portfolio"
        }
        mod_title = mod_titles.get(mod_num, f"Module {mod_num}")

        # Goal
        goal_m = re.search(r'-\s+\*\*Goal:\*\*\s*([^\n\r]+)', sess_block)
        goal = goal_m.group(1).strip() if goal_m else ""

        # Hour parts
        part1_m = re.search(r'-\s+\*\*Part 1:\s*([^(\n\r]+)(?:\(\d+\s*min\))?:\*\*\s*([\s\S]*?)(?=-\s+\*\*Part 2:)', sess_block)
        part2_m = re.search(r'-\s+\*\*Part 2:\s*([^(\n\r]+)(?:\(\d+\s*min\))?:\*\*\s*([\s\S]*?)(?=-\s+\*\*Part 3:)', sess_block)
        part3_m = re.search(r'-\s+\*\*Part 3:\s*([^(\n\r]+)(?:\(\d+\s*min\))?:\*\*\s*([\s\S]*?)(?=-\s+\*\*Part 4:)', sess_block)
        part4_m = re.search(r'-\s+\*\*Part 4:\s*([^(\n\r]+)(?:\(\d+\s*min\))?:\*\*\s*([\s\S]*?)(?=-\s+\*\*Public Data Source:)', sess_block)

        # Public Data & Reference
        data_m = re.search(r'-\s+\*\*Public Data Source:\*\*\s*([^\n\r]+)', sess_block)
        public_data = data_m.group(1).strip() if data_m else ""

        ref_m = re.search(r'-\s+\*\*Reference:\*\*\s*([^\n\r]+)', sess_block)
        reference = ref_m.group(1).strip() if ref_m else ""

        # Weak and Strong prompts
        weak_m = re.search(r'-\s+\*\*Weak Prompt Example[^\n\r]*:\*\*\s*```(?:text)?\s*([\s\S]*?)```[\s\S]*?\*Why it fails:\*\s*([^\n\r]+)', sess_block)
        strong_m = re.search(r'-\s+\*\*Strong Prompt Example[^\n\r]*:\*\*\s*```(?:text)?\s*([\s\S]*?)```[\s\S]*?\*Why it succeeds:\*\s*([^\n\r]+)', sess_block)

        # Exercises
        ex1_m = re.search(r'-\s+\*\*Exercise 1\s*\(([^)]+)\):\*\*([\s\S]*?)(?=-\s+\*\*Exercise 2|\Z)', sess_block)
        ex2_m = re.search(r'-\s+\*\*Exercise 2\s*\(([^)]+)\):\*\*([\s\S]*?)(?=\n####|\Z)', sess_block)

        sessions.append({
            'session_num': sess_num,
            'title': sess_title,
            'module_title': mod_title,
            'goal': goal,
            'part1': {'title': part1_m.group(1).strip() if part1_m else "Theoretical Foundations", 'body': part1_m.group(2).strip() if part1_m else ""},
            'part2': {'title': part2_m.group(1).strip() if part2_m else "Strategic Framework", 'body': part2_m.group(2).strip() if part2_m else ""},
            'part3': {'title': part3_m.group(1).strip() if part3_m else "Enterprise Risk & Governance", 'body': part3_m.group(2).strip() if part3_m else ""},
            'part4': {'title': part4_m.group(1).strip() if part4_m else "Instructor Live Demonstration", 'body': part4_m.group(2).strip() if part4_m else ""},
            'weak_prompt': weak_m.group(1).strip() if weak_m else "",
            'weak_why': weak_m.group(2).strip() if weak_m else "",
            'strong_prompt': strong_m.group(1).strip() if strong_m else "",
            'strong_why': strong_m.group(2).strip() if strong_m else "",
            'public_data': public_data,
            'reference': reference,
            'ex1': {'type': ex1_m.group(1).strip() if ex1_m else "Guided Lab", 'body': ex1_m.group(2).strip() if ex1_m else ""},
            'ex2': {'type': ex2_m.group(1).strip() if ex2_m else "Applied Challenge", 'body': ex2_m.group(2).strip() if ex2_m else ""}
        })
    return sessions

if __name__ == '__main__':
    sessions = parse_markdown('d:/Projects/1169/1169.md')
    print(f"Parsed {len(sessions)} sessions successfully.")
    for s in sessions:
        print(f"Session {s['session_num']}: {s['title']} | Goal len: {len(s['goal'])} | Weak prompt len: {len(s['weak_prompt'])} | Strong prompt len: {len(s['strong_prompt'])}")
