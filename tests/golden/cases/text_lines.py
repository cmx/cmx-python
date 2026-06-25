"""Several consecutive single-line text blocks -- expect them to stay tight."""
import os

from cmx.backends.markdown import CommonMark

doc = CommonMark(filename=os.environ.get("CMX_GOLDEN_OUT", "text_lines.md"))

doc @ "first line"
doc @ "second line"
doc @ "third line"

doc.flush()
