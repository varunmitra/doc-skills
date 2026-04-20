import pytest
from pathlib import Path

FIXTURES = Path(__file__).parent / "fixtures"

@pytest.fixture
def simple_md():
    return (FIXTURES / "simple.md").read_text()

@pytest.fixture
def eds_blog_md():
    return (FIXTURES / "eds-blog.md").read_text()

@pytest.fixture
def block_docs_md():
    return (FIXTURES / "block-docs.md").read_text()

@pytest.fixture
def training_md():
    return (FIXTURES / "training.md").read_text()

@pytest.fixture
def simple_md_path():
    return FIXTURES / "simple.md"

@pytest.fixture
def eds_blog_md_path():
    return FIXTURES / "eds-blog.md"

@pytest.fixture
def block_docs_md_path():
    return FIXTURES / "block-docs.md"

@pytest.fixture
def training_md_path():
    return FIXTURES / "training.md"
