"""Tests for ``doc.savefig`` and figure tables (``table.figure_row().savefig``).

These use a stub logger that records the calls instead of touching matplotlib,
so they verify the routing of keyword arguments without a real plotting backend.
"""

from cmx.backends.components import Article, attrs


class RecordingLogger:
    """Stand-in logger that records ``savefig`` calls instead of writing files."""

    def __init__(self):
        self.calls = []

    def savefig(self, filename, **kwargs):
        self.calls.append((filename, kwargs))


def test_savefig_forwards_matplotlib_kwargs_only_to_logger():
    logger = RecordingLogger()
    doc = Article()
    doc.logger = logger

    fig = doc.savefig("figures/loss.png?ts=123", dpi=150, bbox_inches="tight")

    # The matplotlib kwargs reach the logger, with the ?query stripped from the path.
    assert logger.calls == [("figures/loss.png", {"dpi": 150, "bbox_inches": "tight"})]

    # ...but they never leak into the rendered markup.
    md = fig._md
    assert "dpi" not in md
    assert "bbox-inches" not in md
    assert 'width="None"' not in md
    assert "figures/loss.png?ts=123" in md  # the ?query stays in the src reference


def test_savefig_keeps_display_kwargs():
    logger = RecordingLogger()
    doc = Article()
    doc.logger = logger

    fig = doc.savefig("figures/p.png", caption="a caption", dpi=72)

    md = fig._md
    assert "a caption" in md
    # Only the matplotlib kwarg was forwarded; the caption is a display concern.
    assert logger.calls == [("figures/p.png", {"dpi": 72})]


def test_figure_row_savefig_builds_table():
    logger = RecordingLogger()
    doc = Article()
    doc.logger = logger

    table = doc.table()
    with table.figure_row() as row:
        row.savefig("figures/a.png", title="Plot A", caption="cap a", dpi=100)
        row.savefig("figures/b.png", title="Plot B", caption="cap b", dpi=100)

    md = table._md
    assert "**Plot A**" in md and "**Plot B**" in md
    assert "figures/a.png" in md and "figures/b.png" in md
    assert "cap a" in md and "cap b" in md
    # dpi went to matplotlib for both figures, not into the table cells.
    assert [c[0] for c in logger.calls] == ["figures/a.png", "figures/b.png"]
    assert all(call[1] == {"dpi": 100} for call in logger.calls)
    assert "dpi" not in md


def test_attrs_drops_none_values():
    # ``attrs`` should skip None-valued attributes entirely.
    assert attrs(width=None, height=None) == ""
    assert attrs(width=320) == 'width="320"'
