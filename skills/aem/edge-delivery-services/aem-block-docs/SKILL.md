---
name: aem-block-docs
description: Use when developer wants to document an AEM Edge Delivery Services block for the Sidekick Block Library, write block usage docs, or generate a block library entry. Triggers on: "document this block", "write block docs", "block library docs", "add to block library", "how do I author this block". Output is the AEM Sidekick Library plugin format — a .md file with working EDS table examples per variation, not narrative docs.
version: 1.1.0
---

# AEM Block Library Docs

Generate a Sidekick Block Library entry for an AEM Edge Delivery Services block.
Output is the `.md` format used by the Sidekick Library plugin — working EDS block
table examples per variation, exactly as a developer would author it in Word or Google Docs.

## Interaction Rule

**Use `AskUserQuestion` at every decision point.** Never ask for freeform "yes/no" text.
Each checkpoint must be a clickable prompt. Users always get "Other" automatically.

## Sample Images

Real images are provided in the `samples/` folder next to this SKILL.md. Use them in
generated block table examples wherever image placeholders are needed. Pick by block type:

| Image file | Dimensions | Use for |
|---|---|---|
| `samples/img-hero.jpg` | 1280 × 480 | Hero, Banner, Full-width feature |
| `samples/img-card.jpg` | 600 × 400 | Cards (variation 1), Teaser |
| `samples/img-card-2.jpg` | 600 × 400 | Cards (variation 2) |
| `samples/img-card-3.jpg` | 600 × 400 | Cards (variation 3) |
| `samples/img-teaser.jpg` | 800 × 600 | Columns, Teaser, Side-by-side |
| `samples/img-portrait.jpg` | 400 × 500 | Author, Person, Testimonial |
| `samples/img-square.jpg` | 400 × 400 | Product, Logo, Icon card |

**When writing image cells in EDS block tables**, use a relative path from the output
`.block-docs.md` to the samples folder. For example, if the output file is in
`blocks/cards/`, the image reference is:

```
![Sample card image](../../.skills/edge-delivery-services/aem-block-docs/samples/img-card.jpg)
```

Adjust the relative path depth to match where the output file is written.
If the skill path is unknown, use the filename only and note that the developer should
update the path: `![Sample card image](samples/img-card.jpg)`

## Output Format Reference

Single variation (Library Metadata header):
```
+---------------------+
| Library Metadata    |
+---------+-----------+
| name    | Cards     |
+---------+-----------+

+-------+
| Cards |
+--------------------------------------+------------------------+
| ![Sample card image](samples/img-card.jpg) | **Product Title**      |
|                                      | Description text here. |
+--------------------------------------+------------------------+
```

Multiple variations (section headings + separators):
```
## Cards w/ Images

+-------+
| Cards |
+--------------------------------------+------------------------+
| ![Sample card image](samples/img-card.jpg) | **Product Title**      |
|                                      | Short description.     |
+--------------------------------------+------------------------+

---

## Cards w/o Images

+----------------------------+
| Cards                      |
+----------------------------+
| **Product Title**          |
| Description text here.     |
+----------------------------+
```

## Guided Wizard

### START

**Step 1 — Auto-detect block**

Check if the current working directory matches `*/blocks/<name>/` and a file named
`<name>.js` exists.

- If YES: read `<name>.js` and `<name>.css` silently. Proceed to Step 2.
- If NO: ask the developer for the block folder path, then read the JS and CSS.

**Step 2 — Analyse code**

From the JS file, infer:
- **Variations**: scan for `block.classList.contains('<name>')`, `block.classList.includes`,
  or switch/if statements on class names. Each unique class name check = one variation.
- **Column count per variation**: scan `querySelectorAll(':scope > div > div')` patterns.
  Sliced to 2 elements or indexed [0]/[1] = 2-column. Only [0] used = 1-column.
- **Option strings**: look for `(option1, option2)` patterns in block name checks or
  table header parsing logic.

**Step 3 — Present findings + confirm**

Show the detected variation list in your message, then use `AskUserQuestion`:

```
AskUserQuestion({
  questions: [{
    question: "Do these variations look right?",
    header: "Variations",
    multiSelect: false,
    options: [
      { label: "Yes, continue", description: "Proceed to generate docs for each variation" },
      { label: "Edit the list", description: "Tell me what's missing or incorrect" }
    ]
  }]
})
```

Wait for response before proceeding.

---

### MIDDLE — One variation per turn

For each variation in the confirmed list, run checkpoints A → D.

**A — Block header row**

Show the proposed EDS table header in your message, then:

```
AskUserQuestion({
  questions: [{
    question: "Is the block name and option string correct for this variation?",
    header: "Header row",
    multiSelect: false,
    options: [
      { label: "Correct, continue", description: "Use this header row as-is" },
      { label: "Change it", description: "Tell me the correct name or option string" }
    ]
  }]
})
```

**B — Column structure**

Show the inferred column layout in your message, then:

```
AskUserQuestion({
  questions: [{
    question: "Does this column layout match the block's intended authoring structure?",
    header: "Columns",
    multiSelect: false,
    options: [
      { label: "Correct, continue", description: "Use this layout for the example table" },
      { label: "Change layout", description: "Tell me the actual column structure" }
    ]
  }]
})
```

**C — Example table**

Generate a working EDS block table with 3–4 rows of realistic placeholder content:
- `*eyebrow*` italic for eyebrow/label patterns inferred from CSS
- `**Title**` bold for heading patterns
- Real-looking placeholder links if `<a>` elements appear in JS
- Domain-relevant content (product descriptions for cards, FAQ for accordion)

Show the full table in a fenced code block, then:

```
AskUserQuestion({
  questions: [{
    question: "Does this example table look right for the block library?",
    header: "Example table",
    multiSelect: false,
    options: [
      { label: "Looks good", description: "Use this table in the output" },
      { label: "Edit content", description: "I'll tell you what to change" },
      { label: "Regenerate", description: "Try again with different placeholder content" }
    ]
  }]
})
```

**D — Section heading**

```
AskUserQuestion({
  questions: [{
    question: "Include a ## heading before this variation's table?",
    header: "Section heading",
    multiSelect: false,
    options: [
      { label: "Yes, include heading", description: "Recommended for multi-variation blocks" },
      { label: "Skip heading", description: "Use for single-variation blocks only" }
    ]
  }]
})
```

**After all variations — E — Library Metadata**

```
AskUserQuestion({
  questions: [{
    question: "Include a Library Metadata table at the top with the block name?",
    header: "Lib Metadata",
    multiSelect: false,
    options: [
      { label: "Yes, include it", description: "Recommended for single-variation blocks" },
      { label: "Skip", description: "Optional for multi-variation blocks" }
    ]
  }]
})
```

---

### END

**Filename + format** — ask both together in one `AskUserQuestion` call:

```
AskUserQuestion({
  questions: [
    {
      question: "What should the output file be named?",
      header: "Filename",
      multiSelect: false,
      options: [
        { label: "Use default", description: "<block-name>.block-docs.md — safe to gitignore by pattern" },
        { label: "Custom name", description: "I'll type the filename" }
      ]
    },
    {
      question: "Which output format do you need?",
      header: "Output format",
      multiSelect: false,
      options: [
        { label: "MD only", description: "Markdown file only" },
        { label: "HTML only", description: "Run md-to-html.py — renders EDS block tables with styling" },
        { label: "Both", description: "Write .md then generate .html" }
      ]
    }
  ]
})
```

If HTML or Both selected, run:
```bash
python3 <path-to>/aem-doc-converter/scripts/md-to-html.py <output.md> <output.html>
```

Write the file(s) and confirm: *"✓ Written to `<filename>`."*

## Notes

- Never fabricate block options not present in the JS/CSS.
- Never generate a `README.md`.
- If no variations are detectable, treat as single-variation (Library Metadata header format).
- Placeholder content should be realistic, not lorem ipsum.
