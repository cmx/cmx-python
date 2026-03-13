"""
Unit tests for operator syntax variations in CMX.

This test file verifies that all operator syntaxes work correctly:
- doc @ "text" (prefix @, single line)
- doc @ '''text''' (prefix @, multi-line)
- "text" | doc (postfix |, single line)
- '''text''' | doc (postfix |, multi-line)
"""
import os
import tempfile
from cmx.backends.markdown import CommonMark


def test_prefix_at_single_line():
    """Test prefix @ operator with single-line string."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        temp_file = f.name

    try:
        test_doc = CommonMark(filename=temp_file, overwrite=True)

        with test_doc:
            test_doc @ "# Test Header"
            test_doc @ "This is a test paragraph."

        test_doc.flush()

        with open(temp_file, 'r') as f:
            content = f.read()

        assert "# Test Header" in content
        assert "This is a test paragraph." in content
        assert "```python" in content  # Should include the code block

    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)


def test_prefix_at_multiline():
    """Test prefix @ operator with multi-line string."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        temp_file = f.name

    try:
        test_doc = CommonMark(filename=temp_file, overwrite=True)

        with test_doc:
            test_doc @ """
# Multi-line Header

This is a multi-line text block.
It spans multiple lines.
"""

        test_doc.flush()

        with open(temp_file, 'r') as f:
            content = f.read()

        assert "# Multi-line Header" in content
        assert "This is a multi-line text block." in content
        assert "It spans multiple lines." in content

    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)


def test_postfix_pipe_single_line():
    """Test postfix | operator with single-line string."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        temp_file = f.name

    try:
        test_doc = CommonMark(filename=temp_file, overwrite=True)

        with test_doc:
            "# Pipe Header" | test_doc
            "This is piped text." | test_doc

        test_doc.flush()

        with open(temp_file, 'r') as f:
            content = f.read()

        assert "# Pipe Header" in content
        assert "This is piped text." in content
        assert "```python" in content

    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)


def test_postfix_pipe_multiline():
    """Test postfix | operator with multi-line string."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        temp_file = f.name

    try:
        test_doc = CommonMark(filename=temp_file, overwrite=True)

        with test_doc:
            """
# Multi-line Pipe Header

This is a multi-line piped text block.
It also spans multiple lines.
""" | test_doc

        test_doc.flush()

        with open(temp_file, 'r') as f:
            content = f.read()

        assert "# Multi-line Pipe Header" in content
        assert "This is a multi-line piped text block." in content
        assert "It also spans multiple lines." in content

    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)


def test_mixed_syntax():
    """Test mixing different syntax variations in one document."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        temp_file = f.name

    try:
        test_doc = CommonMark(filename=temp_file, overwrite=True)

        with test_doc:
            test_doc @ "# Mixed Syntax Test"
            "Using pipe operator" | test_doc
            test_doc("Using traditional call")
            test_doc @ "Back to @ operator"

        test_doc.flush()

        with open(temp_file, 'r') as f:
            content = f.read()

        assert "# Mixed Syntax Test" in content
        assert "Using pipe operator" in content
        assert "Using traditional call" in content
        assert "Back to @ operator" in content

    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)


def test_markdown_formatting():
    """Test that markdown output is properly formatted with correct spacing."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        temp_file = f.name

    try:
        test_doc = CommonMark(filename=temp_file, overwrite=True)

        with test_doc:
            test_doc @ "# Header"
            test_doc @ "Text before code block"

        test_doc.flush()

        with open(temp_file, 'r') as f:
            content = f.read()

        # Verify that text doesn't run into code blocks
        # There should be a newline between text and the following code block
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.strip() and not line.startswith('```') and i + 1 < len(lines):
                next_line = lines[i + 1]
                # If next line is a code block, current line should end properly
                if next_line.startswith('```python'):
                    # There should be proper separation
                    assert not line.endswith('```'), f"Text runs into code block at line {i}"

    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)


if __name__ == '__main__':
    test_prefix_at_single_line()
    print("✓ test_prefix_at_single_line passed")

    test_prefix_at_multiline()
    print("✓ test_prefix_at_multiline passed")

    test_postfix_pipe_single_line()
    print("✓ test_postfix_pipe_single_line passed")

    test_postfix_pipe_multiline()
    print("✓ test_postfix_pipe_multiline passed")

    test_mixed_syntax()
    print("✓ test_mixed_syntax passed")

    test_markdown_formatting()
    print("✓ test_markdown_formatting passed")

    print("\nAll tests passed!")
