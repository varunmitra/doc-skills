---
name: aem-block-docs
description: Use when developer wants to document an AEM Edge Delivery Services block for the Sidekick Block Library, write block usage docs, or generate a block library entry. Triggers on: "document this block", "write block docs", "block library docs", "add to block library", "how do I author this block". Output is the AEM Sidekick Library plugin format — a .md file with working EDS table examples per variation, not narrative docs.
version: 1.0.0
---

# AEM Block Library Docs

Generate a Sidekick Block Library entry for an AEM Edge Delivery Services block.
Output is the `.md` format used by the Sidekick Library plugin — working EDS block
table examples per variation, exactly as a developer would author it in Word or Google Docs.

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
+-------------+------------------------+
| ![Alt][img] | **Title**              |
|             | Description text here. |
+-------------+------------------------+
```

Multiple variations (section headings + separators):
```
## Cards w/ Images

+-------+
| Cards |
+-------------+------------------------+
| ![Alt][img] | **Title**              |
|             | Description            |
+-------------+------------------------+

---

## Cards w/o Images

+----------------------------+
| Cards                      |
+----------------------------+
| **Title**                  |
| Description text here.     |
+----------------------------+
```

## Guided Wizard

### START

**Step 1 — Auto-detect block**

Check if the current working directory matches `*/blocks/<name>/` and a file named `<name>.js` exists.

- If YES: read `<name>.js` and `<name>.css` silently. Proceed to Step 2.
- If NO: ask — *"What is the path to the block folder? (e.g., `blocks/hero-banner/`)"* — then read the JS and CSS.

**Step 2 — Analyse code**

From the JS file, infer:
- **Variations**: scan for `block.classList.contains('<name>')`, `block.classList.includes`, or switch/if statements on class names. Each unique class name check = one variation.
- **Column count per variation**: scan `querySelectorAll(':scope > div > div')` patterns. If result is sliced to 2 elements or indexed at [0] and [1], it's 2-column. If only [0] is used, it's 1-column.
- **Option strings**: look for `(option1, option2)` patterns in block name checks or table header parsing logic.

**Step 3 — Present findings**

Show a numbered variation list. Example:
> "I found these variations in `cards.js`:
> 1. Default — 2 columns (image + text)
> 2. `list` — 1 column (text only)
> 3. `list, view-switcher` — 2 columns with view toggle
>
> Does this look right? Reply with corrections or say 'yes' to continue."

Wait for confirmation before proceeding.

---

### MIDDLE — One variation per turn

For each variation in the confirmed list:

**A — Confirm block header row**

Show the proposed EDS table header. Example:
> "Variation 2 header row: `| Cards (list) |`
> Is the block name and option string correct?"

**B — Confirm column structure**

Show the inferred layout. Example:
> "This variation uses 1 column. Each row would be:
> `| content text |`
> Correct?"

**C — Generate example table**

Generate a working EDS block table with 3–4 rows of realistic placeholder content matching the column structure:
- Use `*eyebrow*` italic for eyebrow/label patterns inferred from CSS
- Use `**Title**` bold for heading patterns
- Use real-looking placeholder links if `<a>` elements appear in the JS output
- Keep content domain-relevant (e.g., product descriptions for cards, FAQ questions for accordion)

Show the full table in a fenced code block and ask:
> "Here's the example table for this variation — does it look right? Edit anything or say 'yes' to continue."

**D — Section heading**

Ask: *"Include a `## Variation Name` heading before this table? (Recommended for multi-variation blocks; skip only if this is the only variation.)"*

**After all variations — E — Library Metadata**

Ask: *"Include a `Library Metadata` table at the top with the block name? (Recommended for single-variation blocks; optional for multi-variation.)"*

---

### END

1. Ask: *"What should the output file be named? (Default: `<block-name>.block-docs.md`)"*
   Remind: avoid `README.md` — use a name patternable in `.gitignore`.

2. Ask: *"Output format: MD only / HTML only / Both?"*
   - **MD only**: write the `.md` file.
   - **HTML / Both**: write `.md`, then run:
     ```bash
     python3 <path-to>/aem-doc-converter/scripts/md-to-html.py <output.md> <output.html>
     ```

3. Write the file(s) and confirm: *"✓ Written to `<filename>`."*

## Notes

- Never fabricate block options not present in the JS/CSS.
- Never generate a `README.md`.
- If no variations are detectable, treat as single-variation (Library Metadata header format).
- Placeholder content should be realistic, not lorem ipsum.
