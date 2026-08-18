# Automated PDF Study Guide & Document Generator

This project allows you to provide information (raw notes, syllabus topics, study material, cheatsheets, or structured markdown) and transform it into a formatted, publication-ready PDF in the `output/` folder.

---

## 🚀 How to Use

### Method 1: Just Give Me the Information in Chat! (Recommended)
You can simply paste your raw notes, topic outline, syllabus, or lecture transcript here in chat. I will:
1. **Analyze and structure** the material into clear pedagogical sections.
2. **Extract & format**:
   - **Key Definitions** (`> [!DEFINITION] ...`)
   - **Real-Life Analogies** (`> [!ANALOGY] ...`)
   - **Memory Tricks & Mnemonics** (`> [!MEMORY_TRICK] ...`)
   - **Formulas & Equations** (`> [!FORMULA] ...`)
   - **Comparison Tables** (`| Col1 | Col2 |`)
   - **Exam / Q&A Cards** (`Q: ... A: ...`)
   - **Code Blocks & ASCII Diagrams**
3. Automatically generate and build your PDF directly into the `output/` folder!

---

### Method 2: Put Your Information in `input.md` & Run
1. Open [`input.md`](file:///Volumes/Coding%20/All%20codes/PDF%20GENERATION%20/input.md)
2. Paste or write your notes using the template:

```markdown
---
title: My Course / Topic Name
subtitle: Comprehensive Study Guide
theme: random
author: Vailism
filename: My_Document.pdf
---

# 1. Section Title
Your text goes here...

> [!DEFINITION] Concept Name: Definition text...
> [!ANALOGY] Real-life analogy explanation...
> [!MEMORY_TRICK] Mnemonic / trick...
> [!FORMULA] Equation here...

| Header 1 | Header 2 |
|---|---|
| Value 1 | Value 2 |

Q: Question text?
A: Answer text.
```

3. Run the generator:
```bash
python3 main.py
```
4. Find your generated PDF in the [`output/`](file:///Volumes/Coding%20/All%20codes/PDF%20GENERATION%20/output) folder!

---

## 🎨 Available Themes
Set `theme:` in the frontmatter of `input.md` or let it pick dynamically:
- `random` (Randomly picks a vibrant, harmonious palette)
- `orange` (Burnt Orange / Academic Red)
- `blue` (Deep Navy / Ocean Blue)
- `emerald` (Forest Tech Green)
- `purple` (Royal Purple / Violet)
- `slate` (Executive Slate / Charcoal)
- `crimson` (Deep Crimson / Burgundy)
- `teal` (Deep Sea Teal / Turquoise)
- `indigo` (Royal Indigo / Sapphire)
- `amber` (Warm Amber / Gold)
- `rose` (Rose / Berry)
