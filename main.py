import os
import re
import sys
from pdf_engine import PDFDocumentBuilder

def parse_frontmatter(content):
    metadata = {
        "title": "Study Notes & Summary",
        "subtitle": "Comprehensive Reference & Guide",
        "theme": "random",
        "author": "Vailism",
        "filename": "Generated_Document.pdf"
    }
    
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    body = content
    if match:
        fm_block = match.group(1)
        body = content[match.end():]
        for line in fm_block.split("\n"):
            line = line.strip()
            if ":" in line:
                key, val = line.split(":", 1)
                key = key.strip().lower()
                val = val.strip().strip('"').strip("'")
                if key in metadata:
                    metadata[key] = val
                    
    if not metadata["filename"].endswith(".pdf"):
        metadata["filename"] += ".pdf"
        
    return metadata, body


def convert_markdown_inline_to_html(text):
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"__(.+?)__", r"<b>\1</b>", text)
    text = re.sub(r"\*([^\*]+?)\*", r"<i>\1</i>", text)
    text = re.sub(r"_([^_]+?)_", r"<i>\1</i>", text)
    text = re.sub(r"`([^`]+?)`", r"<font face='Courier' color='#990000'>\1</font>", text)
    return text


def parse_markdown_table(lines):
    table_data = []
    for line in lines:
        line = line.strip()
        if not line.startswith("|") and not line.endswith("|"):
            continue
        cells = [c.strip() for c in line.split("|")[1:-1]]
        if all(re.match(r"^:?-+:?$", c) for c in cells):
            continue
        row = [convert_markdown_inline_to_html(c) for c in cells]
        table_data.append(row)
    return table_data


def process_markdown_to_pdf(md_content, output_dir="output"):
    metadata, body = parse_frontmatter(md_content)
    
    builder = PDFDocumentBuilder(
        title=metadata["title"],
        subtitle=metadata["subtitle"],
        theme_name=metadata["theme"],
        author=metadata["author"]
    )
    
    lines = body.split("\n")
    i = 0
    total_lines = len(lines)
    
    while i < total_lines:
        line = lines[i]
        stripped = line.strip()
        
        if not stripped:
            i += 1
            continue
            
        if stripped in ["---pagebreak---", "\\pagebreak", "[PAGEBREAK]"] or stripped == "---":
            builder.add_pagebreak()
            i += 1
            continue
            
        if stripped.startswith("```"):
            code_lines = []
            i += 1
            while i < total_lines and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            i += 1
            builder.add_code("\n".join(code_lines))
            continue
            
        if stripped.startswith("|") and "|" in stripped[1:]:
            tbl_lines = []
            while i < total_lines and lines[i].strip().startswith("|"):
                tbl_lines.append(lines[i])
                i += 1
            tbl_data = parse_markdown_table(tbl_lines)
            if tbl_data:
                builder.add_table(tbl_data)
            continue
            
        if stripped.startswith("# "):
            builder.add_h1(convert_markdown_inline_to_html(stripped[2:].strip()))
            i += 1
            continue
        elif stripped.startswith("## "):
            builder.add_h2(convert_markdown_inline_to_html(stripped[3:].strip()))
            i += 1
            continue
        elif stripped.startswith("### "):
            builder.add_h3(convert_markdown_inline_to_html(stripped[4:].strip()))
            i += 1
            continue
            
        if stripped.startswith(">"):
            blockquote_lines = []
            while i < total_lines and lines[i].strip().startswith(">"):
                clean_line = re.sub(r"^>\s?", "", lines[i].strip())
                blockquote_lines.append(clean_line)
                i += 1
            full_quote = " ".join(blockquote_lines)
            
            if re.search(r"^\[!(DEFINITION|DEF)\]", full_quote, re.IGNORECASE):
                cleaned = re.sub(r"^\[!(DEFINITION|DEF)\]\s*", "", full_quote, flags=re.IGNORECASE)
                if ":" in cleaned:
                    label, desc = cleaned.split(":", 1)
                    builder.add_definition(label.strip(), convert_markdown_inline_to_html(desc.strip()))
                else:
                    builder.add_definition("KEY CONCEPT", convert_markdown_inline_to_html(cleaned))
            elif re.search(r"^\[!(ANALOGY)\]", full_quote, re.IGNORECASE):
                cleaned = re.sub(r"^\[!(ANALOGY)\]\s*", "", full_quote, flags=re.IGNORECASE)
                builder.add_analogy(convert_markdown_inline_to_html(cleaned))
            elif re.search(r"^\[!(MEMORY_TRICK|MNEMONIC|TRICK)\]", full_quote, re.IGNORECASE):
                cleaned = re.sub(r"^\[!(MEMORY_TRICK|MNEMONIC|TRICK)\]\s*", "", full_quote, flags=re.IGNORECASE)
                builder.add_memory_trick(convert_markdown_inline_to_html(cleaned))
            elif re.search(r"^\[!(FORMULA|MATH)\]", full_quote, re.IGNORECASE):
                cleaned = re.sub(r"^\[!(FORMULA|MATH)\]\s*", "", full_quote, flags=re.IGNORECASE)
                builder.add_formula(cleaned)
            elif re.search(r"^\[!(DIAGRAM)\]", full_quote, re.IGNORECASE):
                cleaned = "\n".join(blockquote_lines)
                cleaned = re.sub(r"^\[!(DIAGRAM)\]\s*", "", cleaned, flags=re.IGNORECASE)
                builder.add_diagram_box(cleaned)
            elif re.search(r"^\[!(QA|Q&A|QUESTION)\]", full_quote, re.IGNORECASE):
                cleaned = re.sub(r"^\[!(QA|Q&A|QUESTION)\]\s*", "", full_quote, flags=re.IGNORECASE)
                if "A:" in cleaned:
                    q_part, a_part = cleaned.split("A:", 1)
                    q_part = re.sub(r"^Q:\s*", "", q_part).strip()
                    builder.add_qa(convert_markdown_inline_to_html(q_part), convert_markdown_inline_to_html(a_part.strip()))
                else:
                    builder.add_qa("Question", convert_markdown_inline_to_html(cleaned))
            else:
                if full_quote.lower().startswith("definition:"):
                    label, desc = full_quote.split(":", 1)
                    builder.add_definition("CONCEPT", convert_markdown_inline_to_html(desc.strip()))
                elif full_quote.lower().startswith("analogy:"):
                    builder.add_analogy(convert_markdown_inline_to_html(full_quote.split(":", 1)[1].strip()))
                elif full_quote.lower().startswith("formula:"):
                    builder.add_formula(full_quote.split(":", 1)[1].strip())
                else:
                    builder.add_definition("NOTE", convert_markdown_inline_to_html(full_quote))
            continue

        if stripped.startswith("- ") or stripped.startswith("* ") or re.match(r"^\d+\.\s+", stripped):
            bullet_items = []
            while i < total_lines and (lines[i].strip().startswith("- ") or lines[i].strip().startswith("* ") or re.match(r"^\d+\.\s+", lines[i].strip())):
                b_text = re.sub(r"^[-*]\s+|\d+\.\s+", "", lines[i].strip())
                bullet_items.append(convert_markdown_inline_to_html(b_text))
                i += 1
            builder.add_bullets(bullet_items)
            builder.add_spacer(2)
            continue
            
        if stripped.startswith("Q:") or stripped.startswith("**Q:"):
            q_text = re.sub(r"^\**Q:\s*", "", stripped).rstrip("*").strip()
            a_text = ""
            i += 1
            if i < total_lines and (lines[i].strip().startswith("A:") or lines[i].strip().startswith("**A:")):
                a_text = re.sub(r"^\**A:\s*", "", lines[i].strip()).rstrip("*").strip()
                i += 1
            builder.add_qa(convert_markdown_inline_to_html(q_text), convert_markdown_inline_to_html(a_text))
            continue

        para_lines = []
        while i < total_lines and lines[i].strip() and not lines[i].strip().startswith(("#", "-", "*", ">", "|", "```", "---")):
            para_lines.append(lines[i].strip())
            i += 1
        paragraph_text = " ".join(para_lines)
        builder.add_paragraph(convert_markdown_inline_to_html(paragraph_text))
        
    out_path = os.path.join(output_dir, metadata["filename"])
    final_path = builder.build(out_path)
    return final_path, metadata, builder.selected_theme_name


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    
    input_file = os.path.join(base_dir, "input.md")
    
    if not os.path.exists(input_file):
        alt_input = os.path.join(base_dir, "input.txt")
        if os.path.exists(alt_input):
            input_file = alt_input
            
    if not os.path.exists(input_file):
        sample_template = """---
title: Operating Systems Study Guide
subtitle: CPU Scheduling Algorithms & Deadlocks
theme: random
author: Vailism
filename: OS_Unit3_Study_Guide.pdf
---

# 1. Overview & Core Concepts
CPU Scheduling is the process by which the operating system decides which of the ready processes is allocated the CPU for execution.

> [!DEFINITION] CPU Scheduling: The mechanism of allocating CPU time among ready-to-run processes to maximize system throughput and resource utilization.

> [!ANALOGY] Think of CPU Scheduling like an airport runway with multiple flights waiting to take off. The Air Traffic Controller (the OS Scheduler) determines which airplane (process) gets clearance on the runway (CPU).

# 2. Scheduling Criteria & Performance Metrics
To evaluate and compare different scheduling algorithms, standard performance metrics are used:

| Metric | Formula | Goal |
|---|---|---|
| Turnaround Time (TAT) | TAT = Completion Time - Arrival Time | Minimize |
| Waiting Time (WT) | WT = Turnaround Time - Burst Time | Minimize |
| Response Time (RT) | RT = First CPU Start Time - Arrival Time | Minimize |
| CPU Utilization | (Busy Time / Total Time) * 100 | Maximize |
| Throughput | Processes Completed / Total Time | Maximize |

> [!FORMULA] TAT = CT - AT  |  WT = TAT - BT  |  RT = First Start Time - AT

# 3. Necessary Conditions for Deadlock
A deadlock occurs when a set of processes are blocked because each process is holding a resource and waiting for another resource held by some other process.

- Mutual Exclusion: Resources cannot be shared simultaneously.
- Hold and Wait: A process holds at least one resource and is waiting for others.
- No Preemption: Resources cannot be forcibly seized from a process.
- Circular Wait: A closed loop of processes where each holds a resource needed by the next.

> [!MEMORY_TRICK] Remember **M-H-N-C**: **M**utual exclusion, **H**old & wait, **N**o preemption, **C**ircular wait. All 4 MUST hold simultaneously for deadlock!

# 4. Exam Template Questions & Answers

Q: Differentiate Deadlock Prevention, Avoidance, and Detection.
A: Prevention permanently eliminates at least one of the four necessary conditions. Avoidance dynamically checks resource requests to ensure system stays in a safe state (e.g. Banker's Algorithm). Detection permits deadlocks to occur, periodically audits resource graphs, and initiates recovery when found.
"""
        with open(input_file, "w", encoding="utf-8") as f:
            f.write(sample_template)
            
    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read()
        
    output_pdf_path, meta, selected_theme = process_markdown_to_pdf(content, output_dir=output_dir)
    print(f"File: {output_pdf_path}")
    print(f"Title: {meta['title']}")
    print(f"Subtitle: {meta['subtitle']}")
    print(f"Author: {meta['author']}")
    print(f"Theme: {selected_theme}")

if __name__ == "__main__":
    main()