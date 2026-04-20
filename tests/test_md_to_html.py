import subprocess
import sys
from pathlib import Path
import pytest

SCRIPT = Path(__file__).parents[1] / "skills/aem/edge-delivery-services/aem-doc-converter/scripts/md-to-html.py"


def run_script(input_path, output_path):
    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(input_path), str(output_path)],
        capture_output=True, text=True
    )
    return result


def test_simple_headings_converted(simple_md_path, tmp_path):
    out = tmp_path / "out.html"
    result = run_script(simple_md_path, out)
    assert result.returncode == 0
    html = out.read_text()
    assert "<h1>" in html
    assert "<h2>" in html
    assert "<strong>" in html
    assert "<em>" in html


def test_output_is_standalone_html(simple_md_path, tmp_path):
    out = tmp_path / "out.html"
    run_script(simple_md_path, out)
    html = out.read_text()
    assert "<!DOCTYPE html>" in html
    assert "<style>" in html


def test_eds_pull_quote_block_rendered(eds_blog_md_path, tmp_path):
    out = tmp_path / "out.html"
    run_script(eds_blog_md_path, out)
    html = out.read_text()
    assert "Pull Quote" in html
    assert "<table" in html


def test_eds_metadata_block_rendered(eds_blog_md_path, tmp_path):
    out = tmp_path / "out.html"
    run_script(eds_blog_md_path, out)
    html = out.read_text()
    assert "Metadata" in html
    assert "Test Author" in html


def test_eds_recommended_articles_rendered(eds_blog_md_path, tmp_path):
    out = tmp_path / "out.html"
    run_script(eds_blog_md_path, out)
    html = out.read_text()
    assert "Recommended Articles" in html
    assert "culture-tecture.adobe.com" in html


def test_block_library_table_preserved(block_docs_md_path, tmp_path):
    out = tmp_path / "out.html"
    run_script(block_docs_md_path, out)
    html = out.read_text()
    assert "Library Metadata" in html
    assert "Cards" in html


def test_missing_input_exits_nonzero(tmp_path):
    out = tmp_path / "out.html"
    result = run_script(tmp_path / "nonexistent.md", out)
    assert result.returncode != 0
