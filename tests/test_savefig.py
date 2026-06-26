"""Tests for ``doc.savefig`` and figure tables (``table.figure_row().savefig``).

These bind a recording ``on_save`` hook instead of touching matplotlib, so they
verify keyword-argument routing without a real plotting backend: matplotlib
kwargs (``dpi``, ``bbox_inches`` ...) must reach ``on_save`` and stay out of the
rendered ``<img>`` markup, while display kwargs (caption, width ...) render.
"""

from cmx.backends.markdown import CommonMark
from cmx.backends.components import attrs


class _Recorder:
    """Records ``on_save`` calls and returns the path as the rendered link."""

    def __init__(self):
        self.calls = []

    def __call__(self, *, data=None, path=None, kind=None, dest=None, doc=None, **kwargs):
        self.calls.append((path, kind, kwargs))
        return path


def _doc():
    doc = CommonMark()
    rec = _Recorder()
    doc.on_save = rec
    return doc, rec


def test_savefig_forwards_matplotlib_kwargs_only_to_on_save():
    doc, rec = _doc()

    fig = doc.savefig("figures/loss.png", dpi=150, bbox_inches="tight")

    # The matplotlib kwargs reach on_save as a "figure" save.
    assert len(rec.calls) == 1
    path, kind, kwargs = rec.calls[0]
    assert kind == "figure"
    assert kwargs.get("dpi") == 150 and kwargs.get("bbox_inches") == "tight"

    # ...but they never leak into the rendered markup.
    md = fig._md
    assert "dpi" not in md
    assert "bbox-inches" not in md
    assert 'width="None"' not in md
    assert "figures/loss.png" in md


def test_savefig_keeps_display_kwargs():
    doc, rec = _doc()

    fig = doc.savefig("figures/p.png", caption="a caption", dpi=72)

    md = fig._md
    assert "a caption" in md
    # Only the matplotlib kwarg was forwarded; the caption is a display concern.
    assert rec.calls[0][2] == {"dpi": 72}
    assert "dpi" not in md


def test_figure_row_savefig_builds_table():
    doc, rec = _doc()

    table = doc.table()
    with table.figure_row() as row:
        row.savefig("figures/a.png", title="Plot A", caption="cap a", dpi=100)
        row.savefig("figures/b.png", title="Plot B", caption="cap b", dpi=100)

    md = table._md
    assert "**Plot A**" in md and "**Plot B**" in md
    assert "figures/a.png" in md and "figures/b.png" in md
    assert "cap a" in md and "cap b" in md
    # The caption lives in the captions band only -- it must not also be rendered
    # inside the image cell (a regression that duplicated it).
    assert md.count("cap a") == 1 and md.count("cap b") == 1
    # dpi went to on_save for both figures, not into the table cells.
    assert [c[0] for c in rec.calls] == ["figures/a.png", "figures/b.png"]
    assert all(c[2] == {"dpi": 100} for c in rec.calls)
    assert "dpi" not in md


def test_figure_row_bare_names_resolve_under_figdir():
    # An unconfigured doc falls back to a shared "figures" figdir; a bare name in
    # a figure row lands there, while a slashed name is used as-is -- the same
    # rule as top-level doc.savefig / doc.image.
    doc, rec = _doc()

    table = doc.table()
    with table.figure_row() as row:
        row.savefig("plot.png", title="Bare")
        row.savefig("sub/explicit.png", title="Slashed")

    assert [c[0] for c in rec.calls] == ["figures/plot.png", "sub/explicit.png"]


def test_attrs_drops_none_values():
    # ``attrs`` should skip None-valued attributes entirely.
    assert attrs(width=None, height=None) == ""
    assert attrs(width=320) == 'width="320"'
