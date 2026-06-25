"""A text block followed by a table -- expect one blank line before the table."""
import os

from cmx.backends.markdown import CommonMark

doc = CommonMark(filename=os.environ.get("CMX_GOLDEN_OUT", "text_then_table.md"))

doc @ "Here is a table of results:"
doc.table([{"name": "alpha", "score": 1}, {"name": "beta", "score": 2}])

doc.flush()
