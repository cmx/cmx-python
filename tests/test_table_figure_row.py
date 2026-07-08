from cmx.backends.components import Article, Image, Video
from cmx.backends.markdown import CommonMark


def test_figure_row():
    doc = Article()
    table = doc.table()
    row = table.figure_row()
    row.figure(src="some_file.png", title="some title", caption="some text")
    row.figure(src="some_file.png", title="some title", caption="some text")
    row.figure(src="some_file.png", title="some title", caption="some text")
    row.figure(src="some_file.png", title="some title", caption="some text")

    row = table.figure_row()
    row.figure(src="some_file.png", title="some title", caption="some text")
    row.figure(src="some_file.png", title="some title", caption="some text")
    row.figure(src="some_file.png", title="some title", caption="some text")
    row.figure(src="some_file.png", title="some title", caption="some text")

    print(table._md)
    assert table._md == """
| **some title** | **some title** | **some title** | **some title** |
|:--------------:|:--------------:|:--------------:|:--------------:|
| ![some_file.png](some_file.png) | ![some_file.png](some_file.png) | ![some_file.png](some_file.png) | ![some_file.png](some_file.png) |
| some text | some text | some text | some text |
| **some title** | **some title** | **some title** | **some title** |
| ![some_file.png](some_file.png) | ![some_file.png](some_file.png) | ![some_file.png](some_file.png) | ![some_file.png](some_file.png) |
| some text | some text | some text | some text |
"""[1:]


def test_mixed_text_and_media_row():
    """`row.column` text cells sit alongside figure/video cells; the band
    renders as a titles row, a cells row, and a captions row."""
    doc = Article()
    table = doc.table()
    row = table.figure_row()
    row.column(title="episode", text="`0000`")
    row.figure(src="frame.png", title="first frame", caption="step 0")
    row.video(src="rollout.gif", title="rollout", caption="preview")

    md = table._md
    lines = md.strip().split("\n")
    # titles band, separator, cells band, captions band
    assert len(lines) == 4
    assert lines[0] == "| **episode** | **first frame** | **rollout** |"
    assert "`0000`" in lines[2]
    assert "(frame.png)" in lines[2]
    assert "(rollout.gif)" in lines[2]
    # captions band: column footer omitted -> blank cell, then the two captions
    assert lines[3].count("|") == 4
    assert "step 0" in lines[3] and "preview" in lines[3]


def test_gif_renders_in_cell_mp4_is_html_video():
    """A `.gif` src becomes an Image (single-line, table-safe); any other
    extension becomes an HTML5 Video block, which is multi-line and therefore
    must not go inside a Markdown table cell."""
    doc = Article()
    row = doc.table().figure_row()
    row.video(src="preview.gif")
    row.video(src="full.mp4")

    gif_cell, mp4_cell = row.children
    assert isinstance(gif_cell, Image)
    assert isinstance(mp4_cell, Video)
    assert "\n" not in gif_cell._md.strip()
    assert "\n" in mp4_cell._md.strip()  # <video> block: never put in a cell


def test_empty_bands_are_dropped():
    """A band with no titles and no captions renders as just the cells row
    (plus the separator)."""
    doc = Article()
    table = doc.table()
    row = table.figure_row()
    row.figure(src="a.png")
    row.figure(src="b.png")

    lines = table._md.strip().split("\n")
    assert len(lines) == 2  # cells row + separator, no title/caption bands
    assert "(a.png)" in lines[0] and "(b.png)" in lines[0]


def test_link_only_cells_write_nothing(tmp_path):
    """src-only cells route through the default on_save with data=None, which
    does no I/O — the link renders now, the artifact can appear later."""
    doc = CommonMark()
    doc.config(file=str(tmp_path / "report.md"))

    table = doc.table()
    row = table.figure_row()
    row.column(title="episode", text="`0000`")
    row.figure(src="pending/frame.png", title="first frame")
    row.video(src="pending/rollout.gif", title="rollout")

    md = table._md
    assert "(pending/frame.png)" in md
    assert "(pending/rollout.gif)" in md
    # nothing was written for the placeholder links
    assert not (tmp_path / "pending").exists()

    doc.flush()
    assert (tmp_path / "report.md").exists()
    assert not (tmp_path / "pending").exists()
