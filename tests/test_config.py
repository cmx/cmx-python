"""Tests for ``cmx.doc.config`` script-relative output resolution.

These tests always write into ``tmp_path`` -- never into the repo.
"""
import os

import numpy as np

from cmx.backends.markdown import CommonMark


def _arr():
    # A tiny RGB image numpy array (PIL + numpy are installed).
    return np.zeros((2, 2, 3), dtype=np.uint8)


def test_config_script_path_derives_md_wd_and_figdir(tmp_path):
    script = str(tmp_path / "04_images.py")
    doc = CommonMark()
    doc.config(file=script)

    assert doc.filename == "04_images.md"
    assert doc.wd == str(tmp_path)
    assert os.path.join(doc.wd, doc.filename) == str(tmp_path / "04_images.md")
    # default figdir template is "{fname}" -> the md stem
    assert doc.figdir == "04_images"


def test_figdir_override_resolves_bare_image(tmp_path):
    script = str(tmp_path / "04_images.py")
    doc = CommonMark()
    doc.config(file=script, figdir="figures")

    assert doc.figdir == "figures"
    img = doc.image(_arr(), src="a.png")
    assert img.src == "figures/a.png"
    assert "figures/a.png" in img._md
    assert os.path.exists(tmp_path / "figures" / "a.png")


def test_default_figdir_uses_md_stem(tmp_path):
    script = str(tmp_path / "04_images.py")
    doc = CommonMark()
    doc.config(file=script)

    img = doc.image(_arr(), src="a.png")
    assert img.src == "04_images/a.png"
    assert "04_images/a.png" in img._md
    assert os.path.exists(tmp_path / "04_images" / "a.png")


def test_explicit_path_wins_over_figdir(tmp_path):
    script = str(tmp_path / "04_images.py")
    doc = CommonMark()
    doc.config(file=script)

    img = doc.image(_arr(), src="sub/a.png")
    assert img.src == "sub/a.png"
    assert "sub/a.png" in img._md
    assert os.path.exists(tmp_path / "sub" / "a.png")
    # NOT placed under the figdir
    assert not os.path.exists(tmp_path / "04_images" / "a.png")


def test_back_compat_filename_kwarg(tmp_path):
    out = str(tmp_path / "t.md")
    doc = CommonMark(filename=out)
    doc @ "hi"
    doc.flush()

    produced = (tmp_path / "t.md").read_text()
    assert "hi" in produced


def test_back_compat_md_positional(tmp_path):
    # The old positional was ``filename``; a ``.md`` ``file`` is treated as output.
    out = str(tmp_path / "t.md")
    doc = CommonMark()
    doc.config(out)
    doc @ "hi"
    doc.flush()
    assert (tmp_path / "t.md").read_text().strip() == "hi"


def test_explicit_wd_override(tmp_path):
    script = str(tmp_path / "nested" / "04_images.py")
    override = tmp_path / "elsewhere"
    override.mkdir()
    doc = CommonMark()
    doc.config(file=script, wd=str(override))

    assert doc.wd == str(override)
    img = doc.image(_arr(), src="a.png")
    assert img.src == "04_images/a.png"
    assert os.path.exists(override / "04_images" / "a.png")
