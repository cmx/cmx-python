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
    # With a known script/output name, figdir defaults to the per-document
    # "{fname}" folder -> the md stem.
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


def test_filename_kwarg_py_postfix_swapped(tmp_path):
    # Regression: a .py path (e.g. doc.config(filename=__file__)) must NOT be used
    # verbatim as the output -- that would overwrite the source script. The .py
    # postfix is swapped to .md.
    script = tmp_path / "report.py"
    script.write_text("print('source')\n")

    doc = CommonMark()
    doc.config(filename=str(script))

    assert doc.filename == "report.md"
    doc @ "hello"
    doc.flush()

    assert (tmp_path / "report.md").read_text().strip() == "hello"
    # the source script is left untouched
    assert script.read_text() == "print('source')\n"


def test_swap_py_suffix_helper():
    from cmx.backends.markdown import _swap_py_suffix

    assert _swap_py_suffix("a/b/script.py") == "a/b/script.md"
    assert _swap_py_suffix("report.md") == "report.md"
    assert _swap_py_suffix("noext") == "noext"
    assert _swap_py_suffix("") == ""


def test_default_figdir_is_figures_without_a_name(tmp_path):
    # A document with no resolved script/output name falls back to a shared
    # "figures" directory instead of a per-document folder.
    doc = CommonMark()
    doc.config(wd=str(tmp_path))  # working dir only, no script/output name

    assert doc.figdir == "figures"
    img = doc.image(_arr(), src="a.png")
    assert img.src == "figures/a.png"
    assert "figures/a.png" in img._md
    assert os.path.exists(tmp_path / "figures" / "a.png")


def test_naming_a_document_upgrades_figdir_to_stem(tmp_path):
    # Re-configuring with a script/output name switches the default away from the
    # "figures" fallback to the per-document "{fname}" folder.
    doc = CommonMark()
    doc.config(wd=str(tmp_path))
    assert doc.figdir == "figures"

    doc.config(file=str(tmp_path / "report.py"))
    assert doc.figdir == "report"


def test_explicit_figdir_overrides_figures_default(tmp_path):
    # An explicit figdir still wins, even with no script/output name.
    doc = CommonMark()
    doc.config(wd=str(tmp_path), figdir="assets")
    assert doc.figdir == "assets"


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
