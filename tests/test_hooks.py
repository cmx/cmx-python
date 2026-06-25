"""Tests for the lifecycle-hooks system on ``CommonMark``.

Hooks are methods on the document with local-disk defaults. They are overridden
either by binding a plain function on the instance (one-off) or by subclassing.
Each test uses a fresh ``CommonMark`` rooted under ``tmp_path``.
"""

import numpy as np

from cmx.backends.markdown import CommonMark


def _img(h=8, w=8, c=3):
    return np.zeros((h, w, c), dtype=np.uint8)


def test_default_writes_md_and_assets(tmp_path):
    doc = CommonMark(filename=str(tmp_path / "r.md"))
    doc @ "# Title"
    doc.image(_img(), src="a.png")
    doc.flush()

    md = (tmp_path / "r.md").read_text()
    assert "# Title" in md
    # bare asset placed under the figdir (md stem == "r")
    assert "![r/a.png](r/a.png)" in md
    assert (tmp_path / "r" / "a.png").exists()


def test_one_off_binding_on_save(tmp_path):
    doc = CommonMark(filename=str(tmp_path / "r.md"))
    doc.on_save = lambda *, data, path, **kw: "http://cdn/x.png"

    doc.image(_img(), src="a.png")
    doc.flush()

    md = (tmp_path / "r.md").read_text()
    assert "http://cdn/x.png" in md
    # the default local file write is bypassed
    assert not (tmp_path / "r" / "a.png").exists()


def test_subclass_override_on_save_with_super(tmp_path):
    written = {}

    class MyDoc(CommonMark):
        def on_save(self, *, data, path, kind, dest, doc, **kw):
            # keep the default local write...
            super().on_save(data=data, path=path, kind=kind, dest=dest, doc=doc, **kw)
            written["path"] = path
            # ...but return a custom link.
            return "https://host/" + path

    doc = MyDoc(filename=str(tmp_path / "r.md"))
    img = doc.image(_img(), src="a.png")
    doc.flush()

    assert img.src == "https://host/r/a.png"
    assert "https://host/r/a.png" in (tmp_path / "r.md").read_text()
    # super().on_save still wrote the bytes locally.
    assert (tmp_path / "r" / "a.png").exists()
    assert written["path"] == "r/a.png"


def test_on_mount_return_becomes_dest_and_threads(tmp_path):
    seen = {}

    class MountDoc(CommonMark):
        def on_mount(self, *, filename, wd, figdir, doc, **kw):
            return "s3://bucket/" + filename

        def on_save(self, *, data, path, kind, dest, doc, **kw):
            seen["save_dest"] = dest
            return path

        def on_flush(self, *, text, path, dest, doc, **kw):
            seen["flush_dest"] = dest
            # do not write locally (remote dest)

    doc = MountDoc(filename=str(tmp_path / "r.md"))
    assert doc.dest == "s3://bucket/r.md"

    doc.image(_img(), src="a.png")
    doc.flush()
    assert seen["save_dest"] == "s3://bucket/r.md"
    assert seen["flush_dest"] == "s3://bucket/r.md"


def test_on_flush_receives_rendered_chunk(tmp_path):
    chunks = []
    doc = CommonMark(filename=str(tmp_path / "r.md"))
    _default = doc.on_flush
    doc.on_flush = lambda *, text, **kw: (chunks.append(text), _default(text=text, **kw))[1]

    doc @ "# Title"
    doc.flush()
    assert chunks and "# Title" in chunks[0]


def test_on_close_full_text_and_fires_once(tmp_path):
    calls = []
    doc = CommonMark(filename=str(tmp_path / "r.md"))
    doc.on_close = lambda *, full_text, **kw: calls.append(full_text)

    doc @ "# Title"
    doc.flush()
    doc.close()
    doc.close()  # idempotent -- second call is a no-op

    assert len(calls) == 1
    assert "# Title" in calls[0]


def test_on_error_fires_and_propagates(tmp_path):
    errors = []
    doc = CommonMark(filename=str(tmp_path / "r.md"))
    doc.on_error = lambda *, exc, **kw: errors.append(exc)

    raised = False
    try:
        with doc:
            raise ValueError("boom")
    except ValueError:
        raised = True

    assert raised, "the exception must still propagate"
    assert len(errors) == 1
    assert isinstance(errors[0], ValueError)


def test_on_block_fires_with_kinds(tmp_path):
    blocks = []
    doc = CommonMark(filename=str(tmp_path / "r.md"))
    doc.on_block = lambda *, kind, node, **kw: blocks.append(kind)

    doc @ "some text"
    doc.table([{"a": 1, "b": 2}])

    assert "text" in blocks
    assert "table" in blocks


def test_on_hide_fires(tmp_path):
    events = []
    doc = CommonMark(filename=str(tmp_path / "r.md"))
    doc.on_hide = lambda *, doc, **kw: events.append("hide")

    with doc.hide:
        pass

    assert events == ["hide"]


def test_on_skip_fires(tmp_path):
    events = []
    doc = CommonMark(filename=str(tmp_path / "r.md"))
    doc.on_skip = lambda *, doc, **kw: events.append("skip")

    # ``on_skip`` fires when the ``doc.skip`` property is read (before the
    # frame-tracing context manager skips the body).
    cm = doc.skip
    assert events == ["skip"]
    with cm:
        # body is skipped by the tracer; nothing here runs.
        events.append("should-not-run")

    assert events == ["skip"]
