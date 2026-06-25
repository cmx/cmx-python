"""Tests for the overridable ``end`` line-terminator on CMX text blocks.

Every text block added via ``doc("...")``, ``doc @ "..."``, or ``"..." | doc``
terminates with a configurable ``end`` string (default ``"\n"``). The default
keeps output byte-identical to before; the call form may override it.

Each test builds a fresh ``CommonMark`` rooted at ``tmp_path`` and asserts on
the rendered markdown via the document's ``_md`` property (the same mechanism
used by the other unit tests).
"""

from cmx.backends.markdown import CommonMark


def _doc(tmp_path):
    return CommonMark(filename=str(tmp_path / "t.md"))


def test_call_default_single_newline(tmp_path):
    doc = _doc(tmp_path)
    doc("x")
    assert doc._md == "x\n"


def test_at_operator_default_single_newline(tmp_path):
    doc = _doc(tmp_path)
    doc @ "x"
    assert doc._md == "x\n"


def test_pipe_operator_default_single_newline(tmp_path):
    doc = _doc(tmp_path)
    "x" | doc
    assert doc._md == "x\n"


def test_end_empty_no_trailing_newline(tmp_path):
    # The Span itself emits no terminator with end="". (The document-level
    # Article._md always normalizes the final document to end in a single
    # newline, so end="" is observable in the component, and in how an
    # end="" block butts directly against the next block's text.)
    from cmx.backends.components import Text

    assert Text("x", end="")._md == "x"

    doc = _doc(tmp_path)
    doc("x", end="")
    doc("y")
    # With no terminator on the first block, the two run together (a single
    # newline is inserted by Article only because "x" lacked a trailing \n).
    assert doc._md == "x\ny\n"


def test_end_double_newline_trailing_blank_line(tmp_path):
    from cmx.backends.components import Text

    assert Text("para", end="\n\n")._md == "para\n\n"

    doc = _doc(tmp_path)
    doc("para", end="\n\n")
    assert doc._md == "para\n\n"


def test_multiline_block_preserves_internal_newlines(tmp_path):
    doc = _doc(tmp_path)
    doc(
        "line one\n\nline three\n",
        dedent=False,
    )
    # Internal blank line preserved; trailing run of newlines collapses to one.
    assert doc._md == "line one\n\nline three\n"
