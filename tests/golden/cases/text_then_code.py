"""A text block followed by a code block -- expect one blank line before the fence."""
import os

from cmx.backends.markdown import CommonMark

doc = CommonMark(filename=os.environ.get("CMX_GOLDEN_OUT", "text_then_code.md"))

doc @ "Here is some code:"
doc.pre("x = 1", lang="python")

doc.flush()
