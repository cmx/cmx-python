"""A heading, a table, a text block, and a code block -- several separations."""
import os

from cmx.backends.markdown import CommonMark

doc = CommonMark(filename=os.environ.get("CMX_GOLDEN_OUT", "mixed.md"))

doc @ "# Report"
doc.table([{"name": "alpha", "score": 1}, {"name": "beta", "score": 2}])
doc @ "Summary of the run:"
doc.pre("total = 3", lang="python")

doc.flush()
