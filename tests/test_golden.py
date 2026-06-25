"""Golden-file test harness for the CMX markdown renderer.

Each ``tests/golden/cases/<name>.py`` is a self-contained script that builds one
markdown document and writes it to the path given by the ``CMX_GOLDEN_OUT`` env
var. This test runs every case into a temp file and asserts the produced output
matches the committed master at ``tests/golden/expected/<name>.md``.

Refresh the masters intentionally with ``UPDATE_GOLDEN=1``.
"""
import difflib
import os
import runpy

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
CASES_DIR = os.path.join(HERE, "golden", "cases")
EXPECTED_DIR = os.path.join(HERE, "golden", "expected")

CASES = sorted(f[:-3] for f in os.listdir(CASES_DIR) if f.endswith(".py") and not f.startswith("_"))


@pytest.mark.parametrize("name", CASES)
def test_golden(name, tmp_path):
    case_path = os.path.join(CASES_DIR, f"{name}.py")
    expected_path = os.path.join(EXPECTED_DIR, f"{name}.md")
    out_path = tmp_path / f"{name}.md"

    prior = os.environ.get("CMX_GOLDEN_OUT")
    os.environ["CMX_GOLDEN_OUT"] = str(out_path)
    try:
        runpy.run_path(case_path, run_name="__main__")
    finally:
        if prior is None:
            os.environ.pop("CMX_GOLDEN_OUT", None)
        else:
            os.environ["CMX_GOLDEN_OUT"] = prior

    produced = out_path.read_text()

    if os.environ.get("UPDATE_GOLDEN") == "1":
        with open(expected_path, "w") as fh:
            fh.write(produced)
        return

    with open(expected_path) as fh:
        expected = fh.read()

    if produced != expected:
        diff = "".join(
            difflib.unified_diff(
                expected.splitlines(keepends=True),
                produced.splitlines(keepends=True),
                fromfile=f"expected/{name}.md",
                tofile=f"produced/{name}.md",
            )
        )
        pytest.fail(f"golden mismatch for {name}:\n{diff}")
