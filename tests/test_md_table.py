"""Byte-for-byte parity tests: our pure-Python renderer vs. tabulate.

These assert ``cmx.backends.md_table.render(df, index=...)`` produces the exact
same string as ``df.to_markdown(tablefmt="github", index=...)`` (which renders
via tabulate) across a broad matrix of DataFrames.

tabulate is the reference oracle here; if it is ever fully removed from the dev
environment these tests self-skip via ``importorskip``.
"""

import pandas as pd
import pytest

from cmx.backends.md_table import render

pytest.importorskip("tabulate")


# Each case: (id, dict-or-DataFrame builder). We build DataFrames lazily so that
# index/dtype intent is preserved.
def _df(data, **kw):
    return pd.DataFrame(data, **kw)


CASES = {
    # --- all int ---
    "all_int": _df({"a": [1, 2, 3], "b": [10, 20, 30]}),
    "int_negatives": _df({"a": [-1, 22, -333], "b": [0, -5, 5]}),
    "int_single_row": _df({"a": [1], "b": [2]}),
    "int_single_col": _df({"only": [1, 2, 3, 4]}),
    # --- all float (incl. scientific + trailing-zero trimming) ---
    "float_trim": _df({"a": [1.0, 0.5, 100.0, 1234567.0]}),
    "float_basic": _df({"x": [3.14159, 2.71828, 1.41421]}),
    "float_sci": _df({"x": [1e-9, 1e9, 1.5e12]}),
    "float_negatives": _df({"a": [-1.5, 2.25, -300.0]}),
    "float_ints_as_float": _df({"a": [1.0, 22.0, 333.0]}),
    "float_mixed_magnitude": _df({"a": [0.1, 10.0, 1000.5, 0.001]}),
    # --- all string ---
    "all_string": _df({"name": ["alpha", "beta", "gamma"], "tag": ["x", "yy", "zzz"]}),
    "string_single": _df({"word": ["hello"]}),
    # --- mixed text + number ---
    "mixed_text_num": _df({"m": [1, "two", 3]}),
    "mixed_float_str": _df({"m": [1.5, "txt", 2.25]}),
    # --- NaN / None ---
    "int_with_nan": _df({"n": [1, None, 3]}),
    "float_with_nan": _df({"a": [1.5, None, 300.25]}),
    "string_with_none": _df({"s": ["a", None, "c"]}),
    "mixed_with_nan": _df({"m": [1, None, "txt"]}),
    "all_nan": _df({"z": [None, None]}),
    # --- bool (string column in tabulate) ---
    "bool_col": _df({"flag": [True, False, True]}),
    # --- wide vs narrow headers ---
    "header_wider_than_values": _df({"a_really_long_header_name": [1, 2]}),
    "values_wider_than_header": _df({"h": ["a_really_long_value_here", "x"]}),
    "header_wider_numeric": _df({"this_is_a_long_numeric_header": [1, 2, 3]}),
    # --- unicode / long strings ---
    "unicode": _df({"name": ["café", "naïve", "Москва"], "v": [1, 2, 3]}),
    "long_strings": _df({"text": ["x" * 40, "short", "y" * 10]}),
    # --- combined / realistic ---
    "realistic": _df({"name": ["alpha", "beta"], "score": [1, 2]}),
    "multi_type": _df(
        {"name": ["alpha", "beta", "gamma"], "score": [1.0, 0.5, 100.0], "count": [10, 20, 30]}
    ),
    # --- custom (string) index ---
    "string_index": _df({"v": [1, 2]}, index=["row_one", "row_two"]),
    "named_index": _df({"v": [1, 2]}, index=pd.Index(["a", "b"], name="key")),
}


@pytest.mark.parametrize("name", list(CASES))
@pytest.mark.parametrize("index", [False, True], ids=["noindex", "index"])
def test_parity(name, index):
    df = CASES[name]
    expected = df.to_markdown(tablefmt="github", index=index)
    actual = render(df, index=index)
    assert actual == expected, (
        f"\ncase={name} index={index}\n--- expected (tabulate) ---\n{expected}\n"
        f"--- actual (render) ---\n{actual}\n"
    )
