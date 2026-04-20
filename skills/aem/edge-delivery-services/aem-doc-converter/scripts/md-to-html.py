#!/usr/bin/env python3
"""
md-to-html.py — Convert Markdown to EDS-aware standalone HTML.

EDS block table patterns (Pull Quote, Metadata, Recommended Articles,
Columns, Library Metadata) are detected and rendered as styled HTML
tables that copy cleanly into Word for document authoring.

Usage: python md-to-html.py <input.md> <output.html>
"""
import sys
import re
from pathlib import Path

try:
    import markdown
    from bs4 import BeautifulSoup
except ImportError:
    print("Error: Missing dependencies. Run: pip install markdown beautifulsoup4", file=sys.stderr)
    sys.exit(1)

EDS_BLOCK_NAMES = {
    "pull quote", "metadata", "recommended articles", "columns",
    "library metadata", "table",
}

INLINE_CSS = """
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
       max-width: 900px; margin: 40px auto; padding: 0 20px; color: #333; }
h1 { font-size: 2em; margin-bottom: 0.5em; }
h2 { font-size: 1.4em; margin-top: 2em; border-bottom: 1px solid #eee; padding-bottom: 6px; }
h3 { font-size: 1.1em; margin-top: 1.5em; }
p { line-height: 1.6; }
table { border-collapse: collapse; width: 100%; margin: 1.5em 0; }
th, td { border: 1px solid #ccc; padding: 8px 12px; vertical-align: top; text-align: left; }
th { background: #f5f5f5; font-weight: 600; }
.eds-block-header td { background: #1473e6; color: white; font-weight: bold;
                        font-size: 0.9em; text-transform: uppercase; letter-spacing: 0.05em; }
code { background: #f4f4f4; padding: 2px 5px; border-radius: 3px; font-size: 0.9em; }
pre { background: #f4f4f4; padding: 16px; border-radius: 6px; overflow-x: auto; }
pre code { background: none; padding: 0; }
blockquote { border-left: 4px solid #1473e6; margin: 0; padding: 0 16px; color: #555; }
a { color: #1473e6; }
hr { border: none; border-top: 1px solid #ddd; margin: 2em 0; }
"""


def parse_eds_table(text):
    """
    Parse an EDS pipe-table block (lines starting with + or |) into
    a list of rows, where each row is a list of cell strings.
    Returns (block_name, rows) or (None, None) if not an EDS block.
    """
    lines = [l for l in text.strip().splitlines() if l.strip()]
    if not lines:
        return None, None

    rows = []
    current_row = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("+") and set(stripped) <= set("+-=|"):
            if current_row:
                rows.append([c.strip() for c in current_row])
                current_row = []
        elif stripped.startswith("|"):
            cells = [c.strip() for c in stripped.split("|")[1:-1]]
            if current_row:
                for i, c in enumerate(cells):
                    if i < len(current_row):
                        if c:
                            current_row[i] = (current_row[i] + " " + c).strip()
                    else:
                        current_row.append(c)
            else:
                current_row = cells

    if current_row:
        rows.append([c.strip() for c in current_row])

    if not rows:
        return None, None

    block_name = rows[0][0].strip() if rows else ""
    return block_name, rows


def render_eds_table_html(block_name, rows):
    """Render parsed EDS table rows as styled HTML table."""
    header_class = ""
    block_lower = block_name.lower().split("(")[0].strip()
    if block_lower in EDS_BLOCK_NAMES:
        header_class = ' class="eds-block-header"'

    html = ['<table>']
    for i, row in enumerate(rows):
        html.append("<tr" + (header_class if i == 0 else "") + ">")
        tag = "th" if i == 0 else "td"
        if len(row) == 1:
            html.append(f'<{tag} colspan="2">{_md_inline(row[0])}</{tag}>')
        else:
            for cell in row:
                html.append(f"<{tag}>{_md_inline(cell)}</{tag}>")
        html.append("</tr>")
    html.append("</table>")
    return "\n".join(html)


def _md_inline(text):
    """Convert inline markdown (bold, italic, links) to HTML."""
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    text = re.sub(r'(?<!["\(])(https?://[^\s<]+)', r'<a href="\1">\1</a>', text)
    return text


def convert(input_path, output_path):
    source = Path(input_path).read_text(encoding="utf-8")
    body_parts = []

    lines = source.splitlines(keepends=True)
    in_table = False
    table_lines = []
    md_lines = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("+") and re.match(r'^\+[-=+|]+', stripped):
            if not in_table:
                if md_lines:
                    body_parts.append(("md", "".join(md_lines)))
                    md_lines = []
                in_table = True
            table_lines.append(line)
        elif in_table and (stripped.startswith("|") or stripped.startswith("+")):
            table_lines.append(line)
        else:
            if in_table:
                table_text = "".join(table_lines)
                block_name, rows = parse_eds_table(table_text)
                if block_name and rows:
                    body_parts.append(("eds_table", (block_name, rows)))
                else:
                    body_parts.append(("md", table_text))
                table_lines = []
                in_table = False
            md_lines.append(line)

    if in_table and table_lines:
        table_text = "".join(table_lines)
        block_name, rows = parse_eds_table(table_text)
        if block_name and rows:
            body_parts.append(("eds_table", (block_name, rows)))
        else:
            body_parts.append(("md", table_text))
    if md_lines:
        body_parts.append(("md", "".join(md_lines)))

    html_parts = []
    md_ext = markdown.Markdown(extensions=["tables", "fenced_code", "extra"])
    for part_type, content in body_parts:
        if part_type == "eds_table":
            block_name, rows = content
            html_parts.append(render_eds_table_html(block_name, rows))
        else:
            md_ext.reset()
            html_parts.append(md_ext.convert(content))

    body_html = "\n".join(html_parts)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Document</title>
<style>
{INLINE_CSS}
</style>
</head>
<body>
{body_html}
</body>
</html>"""

    Path(output_path).write_text(html, encoding="utf-8")


def main():
    if len(sys.argv) != 3:
        print("Usage: md-to-html.py <input.md> <output.html>", file=sys.stderr)
        sys.exit(1)

    input_path = Path(sys.argv[1])
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    convert(input_path, sys.argv[2])
    print(f"✓ Converted to {sys.argv[2]}")


if __name__ == "__main__":
    main()
