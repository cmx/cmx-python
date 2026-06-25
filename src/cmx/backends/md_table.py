"""Pure-Python GitHub-flavored Markdown table renderer.

This module reproduces, byte-for-byte, the output of
``pandas.DataFrame.to_markdown(tablefmt="github", index=<bool>)`` for the slice
of behavior CMX relies on -- WITHOUT importing ``tabulate`` at runtime.

It is a faithful, narrow re-implementation of tabulate's GitHub format. The
algorithm mirrors tabulate's internals:

* Per-column type detection (least-generic type over the column's values).
  ``bool``/``str``/``bytes``/datetime columns are STRING (left-aligned); ``int``
  and ``float`` columns are NUMERIC (decimal-point aligned, which collapses to
  right-alignment).
* Number formatting matches tabulate defaults: ints via ``str``/``format("")``;
  floats via the ``g`` format. Missing values (None / NaN) render as ``""``.
* Width = ``max(len(header) + MIN_PADDING, max cell width)``; cells get one
  space of padding on each side; the separator row is plain dashes (no colons).
* ``index=True`` prepends the DataFrame index as a leading column (with the
  index name -- or an empty string -- as its header).

Only ``pandas``/``numpy`` are used, and only to introspect the frame's values;
they are already dependencies of the tables feature.

The reference for this implementation is tabulate 0.x's ``__init__.py``
(functions ``_type``, ``_column_type``, ``_format``, ``_align_column``,
``_align_header``, ``_format_table`` and the ``"github"`` ``TableFormat``).
"""

import math
from functools import reduce

# tabulate's MIN_PADDING constant: every column's minimum width is its header
# width plus this, before being expanded to fit the body cells.
MIN_PADDING = 2

# Numeric (right/decimal aligned) column types.
_NUMERIC_TYPES = (int, float)


def _is_missing(val):
    """True only for the values tabulate treats as missing (-> empty cell).

    NOTE: tabulate considers ONLY ``None`` and the empty string/bytes missing.
    A bare ``float('nan')`` (how pandas stores NaN in a numeric column) is NOT
    missing -- it is a numeric value that formats as the literal ``"nan"``.
    Only the Python ``None`` object (e.g. an object column with ``None``) yields
    an empty cell.
    """
    if val is None:
        return True
    if isinstance(val, (bytes, str)) and not val:
        return True
    return False


def _is_bool(val):
    return type(val) is bool or (isinstance(val, (bytes, str)) and val in ("True", "False"))


def _is_int(val):
    if type(val) is int:
        return True
    # numpy integer scalars (numpy.int64 etc.)
    if (hasattr(val, "is_integer") or hasattr(val, "__array__")) and str(type(val)).startswith("<class 'numpy.int"):
        return True
    if isinstance(val, (bytes, str)):
        try:
            int(val)
            return True
        except (ValueError, TypeError):
            return False
    return False


def _is_number(val):
    """Mirror tabulate._isnumber: could this be considered numeric?"""
    if type(val) in (float, int):
        return True
    try:
        f = float(val)
    except (ValueError, TypeError):
        return False
    if not isinstance(val, (str, bytes)):
        return True
    # numeric string: exclude over/underflow to +/-inf unless literally inf/nan.
    return (not (math.isinf(f) or math.isnan(f))) or val.lower() in ("inf", "-inf", "nan")


def _type(val):
    """Least-generic scalar type of a value (mirrors tabulate._type).

    Returns one of: ``type(None)``, ``bool``, ``int``, ``float``, ``bytes``,
    ``str``. Empty / missing values are treated as ``type(None)`` so they do not
    influence a column's deduced type.
    """
    if _is_missing(val):
        return type(None)
    if isinstance(val, (bytes, str)) and not val:
        return type(None)
    if hasattr(val, "isoformat"):  # datetime / date / time -> string column
        return str
    if _is_bool(val):
        return bool
    if _is_int(val):
        return int
    if _is_number(val):
        return float
    if isinstance(val, bytes):
        return bytes
    return str


# Generality ordering used to reduce a column's per-value types to one type.
_TYPE_RANK = {type(None): 0, bool: 1, int: 2, float: 3, bytes: 4, str: 5}
_RANK_TYPE = {v: k for k, v in _TYPE_RANK.items()}


def _more_generic(type1, type2):
    return _RANK_TYPE[max(_TYPE_RANK.get(type1, 5), _TYPE_RANK.get(type2, 5))]


def _column_type(values):
    """Least-generic type all of a column's values are convertible to."""
    return reduce(_more_generic, (_type(v) for v in values), bool)


def _format_value(val, coltype, missingval=""):
    """Format a single value as tabulate would (defaults: floatfmt='g')."""
    if val is None:
        return missingval
    if isinstance(val, (bytes, str)) and not val:
        return ""

    if coltype is str:
        return f"{val}"
    if coltype is int:
        return format(val, "")
    if coltype is bytes:
        try:
            return str(val, "ascii")
        except (TypeError, UnicodeDecodeError):
            return str(val)
    if coltype is float:
        if isinstance(val, str) and "," in val:
            val = val.replace(",", "")
        try:
            return format(float(val), "g")
        except (ValueError, TypeError):
            return f"{val}"
    return f"{val}"


def _afterpoint(string):
    """Count of symbols after the decimal point, -1 if there is none.

    Mirrors tabulate._afterpoint, used for decimal alignment of numeric columns.
    """
    if _is_number(string):
        if _is_int(string):
            return -1
        pos = string.rfind(".")
        if pos < 0:
            pos = string.lower().rfind("e")
        if pos >= 0:
            return len(string) - pos - 1
        return -1
    return -1


def _align_column(strings, alignment, minwidth):
    """Pad a column of pre-formatted strings to a common width.

    ``alignment`` is ``"left"`` for string columns or ``"decimal"`` for numeric
    columns. Returns the list of padded cell strings.
    """
    if alignment == "decimal":
        decimals = [_afterpoint(s) for s in strings]
        maxdecimals = max(decimals)
        strings = [s + (maxdecimals - d) * " " for s, d in zip(strings, decimals)]
        # decimal alignment then flushes right.
        maxwidth = max(max((len(s) for s in strings), default=0), minwidth)
        return [s.rjust(maxwidth) for s in strings]
    # "left": strip then flush left.
    strings = [s.strip() for s in strings]
    maxwidth = max(max((len(s) for s in strings), default=0), minwidth)
    return [s.ljust(maxwidth) for s in strings]


def _align_header(header, alignment, width):
    if alignment == "left":
        return header.ljust(width)
    # numeric ("decimal") headers flush right.
    return header.rjust(width)


def _extract_columns(df, index):
    """Return ``(headers, columns)`` from a DataFrame.

    ``columns`` is a list of per-column value lists (row-major transposed).
    When ``index`` is true the frame's index is prepended as a leading column,
    with the index name (or ``""``) as its header. Mirrors the DataFrame branch
    of tabulate._normalize_tabular_data.
    """
    headers = [str(k) for k in df.columns]
    columns = [list(df[col].values) for col in df.columns]

    if index:
        idx = df.index
        idx_name = idx.name
        if idx_name is not None:
            headers = [str(idx_name)] + headers
        else:
            headers = [""] + headers
        columns = [list(idx)] + columns

    return headers, columns


def render(df, index=False):
    """Render a pandas DataFrame as a GitHub-flavored Markdown table string.

    Reproduces ``df.to_markdown(tablefmt="github", index=index)`` exactly
    (without any trailing newline). Only pandas/numpy are used to read the
    frame; ``tabulate`` is never imported.
    """
    headers, columns = _extract_columns(df, index)

    coltypes = [_column_type(col) for col in columns]
    # Numeric columns align on the decimal point; others flush left.
    aligns = ["decimal" if ct in _NUMERIC_TYPES else "left" for ct in coltypes]

    # Format every cell to its string form.
    formatted = [[_format_value(v, ct) for v in col] for col, ct in zip(columns, coltypes)]

    # Minimum width per column: header width + MIN_PADDING (tabulate behavior).
    minwidths = [len(h) + MIN_PADDING for h in headers]

    # Pad body cells within each column to its aligned width.
    aligned_cols = [_align_column(col, a, mw) for col, a, mw in zip(formatted, aligns, minwidths)]

    # Final column content width = max(header+MIN_PADDING, widest body cell).
    colwidths = [
        max(mw, max((len(cell) for cell in col), default=0))
        for mw, col in zip(minwidths, aligned_cols)
    ]

    # Align headers to the final width.
    aligned_headers = [_align_header(h, a, w) for h, a, w in zip(headers, aligns, colwidths)]

    pad = 1  # github padding
    padded_widths = [w + 2 * pad for w in colwidths]

    def build_row(cells):
        padded = [(" " * pad) + c + (" " * pad) for c in cells]
        return ("|" + "|".join(padded) + "|").rstrip()

    def build_sep():
        cells = ["-" * w for w in padded_widths]
        return ("|" + "|".join(cells) + "|").rstrip()

    lines = [build_row(aligned_headers), build_sep()]
    # Re-align padded body cells back to colwidth (already are) and emit rows.
    rows = list(zip(*aligned_cols)) if aligned_cols else []
    for row in rows:
        lines.append(build_row(list(row)))

    return "\n".join(lines)
