## AEM Doc Converter

Use these instructions when asked to convert a Markdown file to HTML or Word format,
make a document copy-paste ready for EDS authoring, or convert markdown.
Keywords: "convert to HTML", "convert to Word", "make this copy-paste ready",
"convert this doc", "convert this markdown", "I want to paste this into Word".

---

# AEM Doc Converter

Convert any Markdown file to HTML or Word format using local Python scripts.
Zero AI tokens used — scripts run entirely on your machine.

EDS block tables (Pull Quote, Metadata, Recommended Articles, Library Metadata, Columns)
are detected and rendered with proper HTML table structure so they paste correctly into
Word for document authoring.

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
- Exactly one `.md` file found → *"I found `<filename>.md` — using that as input. OK?"*
- Multiple `.md` files found → list them and ask which one
- No `.md` files found → *"What is the path to the Markdown file you want to convert?"*

**Step 2 — Preview structure**

Read the file and show:
> "Found in `<filename>.md`:
> - N headings (H1: [title], H2: [first two section names]...)
> - EDS block tables detected: [list block names e.g. Pull Quote, Metadata]
> - N sections total
>
> Any sections to exclude before converting? (say 'no' to include all)"

---

### MIDDLE

**Step 3 — EDS block tables**

If EDS block tables were detected:
> "I found EDS block tables. Render them with EDS-aware styling (blue header row, proper
> table structure for Word paste)? Recommended: Yes."

**Step 4 — Output format**

> "Output format: HTML / Word doc (.docx) / Both?"

If Word doc chosen:
> "Note: `md-to-docx.py` uses python-docx locally — zero AI tokens.
> HTML also pastes cleanly into Word if that works for your authoring workflow."

---

### END

1. Ask: *"Output filename? (Default: `<same-stem>.html` / `<same-stem>.docx`)"*

2. Run the script(s):
   ```bash
   # HTML
   python3 <path-to>/aem-doc-converter/scripts/md-to-html.py <input.md> <output.html>

   # Word doc
   python3 <path-to>/aem-doc-converter/scripts/md-to-docx.py <input.md> <output.docx>
   ```

3. Confirm: *"✓ Done. Open `<output>` — copy and paste into your EDS Word document."*
