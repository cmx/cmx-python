from cmx import doc


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

    target = """
| **some title** | **some title** | **some title** | **some title** |
|:--------------:|:--------------:|:--------------:|:--------------:|
| ![some_file.png](some_file.png) | ![some_file.png](some_file.png) | ![some_file.png](some_file.png) | ![some_file.png](some_file.png) |
| some text | some text | some text | some text |
| **some title** | **some title** | **some title** | **some title** |
| ![some_file.png](some_file.png) | ![some_file.png](some_file.png) | ![some_file.png](some_file.png) | ![some_file.png](some_file.png) |
| some text | some text | some text | some text |
"""[1:]

    print(doc._md)

    assert doc._md == target
    doc.children.clear()


def test_image():
    from skimage import data

    img = data.astronaut()
    doc.image(img)
    print(doc._md)
    doc.flush()


def test_image_src():
    from skimage import data

    img = data.camera()
    doc.image(img, f"figures/reach.png?ts={doc.now()}")
    print(doc._md)
    doc.flush()


def test_figure_row():
    doc @ """
    ## Test Figure Row
    """
    with doc:
        from skimage import data

        img = data.coins()

    with doc, doc.table() as table:
        with table.figure_row() as row:
            row.figure(img, src=f"figures/reach.png?ts={doc.now()}", title="Before Init", caption="this is the details")
            row.figure(img, src=f"figures/reach.png?ts={doc.now()}", title="Before Init", caption="this is the details")
            row.figure(img, src=f"figures/reach.png?ts={doc.now()}", title="Before Init", caption="this is the details")
            row.figure(img, src=f"figures/reach.png?ts={doc.now()}", title="Before Init", caption="this is the details")
