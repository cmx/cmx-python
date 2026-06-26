import numpy as np

from cmx import doc
from cmx.backends.markdown import CommonMark


def _gradient_image(h=8, w=8, channels=3):
    """Deterministic gradient image as a uint8 numpy array (no randomness)."""
    rows = np.linspace(0, 255, h, dtype=np.uint8)[:, None]
    cols = np.linspace(0, 255, w, dtype=np.uint8)[None, :]
    plane = ((rows.astype(np.uint16) + cols.astype(np.uint16)) // 2).astype(np.uint8)
    if channels == 1:
        return plane
    return np.stack([plane] * channels, axis=-1)


def test_str():
    a = """
    here is a string
    """
    b = """
here is a string
"""
    doc @ a
    assert doc._md == b
    doc.children.clear()


def test_print():
    for i in range(2):
        doc.print(i, "<")

    target = """
```
0 <
1 <
```
"""[1:]
    print(doc._md)
    assert doc._md == target
    doc.children.clear()


def test_table():
    table = doc.table()

    with table.figure_row() as row:
        row.figure(src="some_file.png", title="some title", caption="some text")
        row.figure(src="some_file.png", title="some title", caption="some text")
        row.figure(src="some_file.png", title="some title", caption="some text")
        row.figure(src="some_file.png", title="some title", caption="some text")

    with table.figure_row() as row:
        row.figure(src="some_file.png", title="some title", caption="some text")
        row.figure(src="some_file.png", title="some title", caption="some text")
        row.figure(src="some_file.png", title="some title", caption="some text")
        row.figure(src="some_file.png", title="some title", caption="some text")

    # The bare ``some_file.png`` resolves through the (unconfigured) singleton's
    # figdir -> a shared "figures" directory, the same rule as doc.image / savefig.
    target = """
| **some title** | **some title** | **some title** | **some title** |
|:--------------:|:--------------:|:--------------:|:--------------:|
| ![figures/some_file.png](figures/some_file.png) | ![figures/some_file.png](figures/some_file.png) | ![figures/some_file.png](figures/some_file.png) | ![figures/some_file.png](figures/some_file.png) |
| some text | some text | some text | some text |
| **some title** | **some title** | **some title** | **some title** |
| ![figures/some_file.png](figures/some_file.png) | ![figures/some_file.png](figures/some_file.png) | ![figures/some_file.png](figures/some_file.png) | ![figures/some_file.png](figures/some_file.png) |
| some text | some text | some text | some text |
"""[1:]

    print(doc._md)

    assert doc._md == target
    doc.children.clear()


def test_image(tmp_path):
    local_doc = CommonMark(filename=str(tmp_path / "test_image.md"))

    img = _gradient_image()
    local_doc.image(img)
    # An inline image renders as a base64 data URI.
    assert "data:image/png;base64," in local_doc._md
    print(local_doc._md)
    local_doc.flush()
    assert (tmp_path / "test_image.md").exists()


def test_image_src(tmp_path):
    # root the document at tmp_path so relative image srcs are written there.
    local_doc = CommonMark(filename=str(tmp_path / "test_image_src.md"), root=str(tmp_path))

    img = _gradient_image(channels=1)
    src = f"figures/reach.png?ts={local_doc.now()}"
    local_doc.image(img, src)
    print(local_doc._md)
    local_doc.flush()
    # The image data is written to disk alongside the markdown document.
    assert (tmp_path / "figures" / "reach.png").exists()
    assert (tmp_path / "test_image_src.md").exists()


def test_figure_row(tmp_path):
    # root the logger at tmp_path so relative image srcs are written there.
    local_doc = CommonMark(filename=str(tmp_path / "test_figure_row.md"), root=str(tmp_path))

    local_doc @ """
    ## Test Figure Row
    """
    img = _gradient_image()

    with local_doc.table() as table:
        with table.figure_row() as row:
            row.figure(img, src=f"figures/reach.png?ts={local_doc.now()}", title="Before Init", caption="this is the details")
            row.figure(img, src=f"figures/reach.png?ts={local_doc.now()}", title="Before Init", caption="this is the details")
            row.figure(img, src=f"figures/reach.png?ts={local_doc.now()}", title="Before Init", caption="this is the details")
            row.figure(img, src=f"figures/reach.png?ts={local_doc.now()}", title="Before Init", caption="this is the details")

    local_doc.flush()
    assert (tmp_path / "figures" / "reach.png").exists()
    assert (tmp_path / "test_figure_row.md").exists()
