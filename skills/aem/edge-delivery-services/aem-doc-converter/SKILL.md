---
name: aem-doc-converter
description: Use when developer has an existing Markdown file and wants to convert it to HTML (for copy-paste into Word for AEM Edge Delivery Services document authoring) or a Word .docx file. Triggers on: "convert to HTML", "convert to Word", "make this copy-paste ready", "convert this doc", "convert this markdown", "I want to paste this into Word".
version: 1.1.0
---

# AEM Doc Converter

Convert any Markdown file to HTML or Word format using local Python scripts.
Zero AI tokens used — scripts run entirely on your machine.

EDS block tables (Pull Quote, Metadata, Recommended Articles, Library Metadata, Columns)
are detected and rendered with proper HTML table structure so they paste correctly into
Word for document authoring.

## Interaction Rule

**Use `AskUserQuestion` at every decision point.** Never ask for freeform "yes/no" text.
Each checkpoint must be a clickable prompt. Users always get "Other" automatically.

## Scripts

All scripts live in `skills/aem/edge-delivery-services/aem-doc-converter/scripts/`.

| Script | Output | Dependencies |
|---|---|---|
| `md-to-html.py` | Standalone HTML (inline styles, no external deps) | `markdown`, `beautifulsoup4` |
| `md-to-docx.py` | Word `.docx` | `python-docx` |
| `md-to-pptx.py` | PowerPoint `.pptx` | `python-pptx` |

Install all: `pip3 install -r skills/aem/edge-delivery-services/aem-doc-converter/scripts/requirements.txt`

## Guided Wizard

### START

**Step 1 — Detect input file**

Check for `.md` files in the current working directory:

- **Exactly one** `.md` file found → present it by name and ask:

```
AskUserQuestion({
  questions: [{
    question: "I found <filename>.md — use this as the input?",
    header: "Input file",
    multiSelect: false,
    options: [
      { label: "Yes, use this file", description: "Convert <filename>.md" },
      { label: "Different file", description: "I'll type the path to the file I want" }
    ]
  }]
})
```

- **Multiple** `.md` files found → list them and ask the developer to pick one (use "Other"
  to type a path not in the list).

- **No** `.md` files → ask the developer for the file path as plain text.

**Step 2 — Preview structure**

Read the file and show a summary in your message:
> Found in `<filename>.md`:
> - N headings (H1: [title], H2: [first two section names]...)
> - EDS block tables detected: [list block names or "none"]
> - N sections total

Then ask:

```
AskUserQuestion({
  questions: [{
    question: "Any sections to exclude before converting?",
    header: "Sections",
    multiSelect: false,
    options: [
      { label: "Include everything", description: "Convert the full document" },
      { label: "Exclude some sections", description: "I'll tell you which headings to skip" }
    ]
  }]
})
```

---

### MIDDLE

**Step 3 — EDS block table styling** (only ask if EDS block tables were detected)

```
AskUserQuestion({
  questions: [{
    question: "Render EDS block tables with EDS-aware styling?",
    header: "Block styling",
    multiSelect: false,
    options: [
      { label: "Yes (recommended)", description: "Blue header row, proper table structure — pastes cleanly into Word" },
      { label: "Plain tables", description: "Standard HTML table styling" }
    ]
  }]
})
```

**Step 4 — Output format**

```
AskUserQuestion({
  questions: [{
    question: "Which output format do you need?",
    header: "Output format",
    multiSelect: false,
    options: [
      { label: "HTML", description: "Standalone HTML — paste into Word for EDS authoring (recommended)" },
      { label: "Word doc (.docx)", description: "Direct .docx via python-docx — zero AI tokens" },
      { label: "Both", description: "Generate both .html and .docx" }
    ]
  }]
})
```

---

### END

```
AskUserQuestion({
  questions: [{
    question: "What should the output file be named?",
    header: "Filename",
    multiSelect: false,
    options: [
      { label: "Use default", description: "Same stem as input: <name>.html / <name>.docx" },
      { label: "Custom name", description: "I'll type the output filename" }
    ]
  }]
})
```

Run the script(s):
```bash
# HTML
python3 <path-to>/aem-doc-converter/scripts/md-to-html.py <input.md> <output.html>

# Word doc
python3 <path-to>/aem-doc-converter/scripts/md-to-docx.py <input.md> <output.docx>
```

Confirm: *"✓ Done. Open `<output>` — copy and paste into your EDS Word document."*
