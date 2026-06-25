"""A text block followed by an image reference -- expect one blank line before it."""
import os

from cmx.backends.markdown import CommonMark

doc = CommonMark(filename=os.environ.get("CMX_GOLDEN_OUT", "text_then_image.md"))

doc @ "Here is a figure:"
doc.image(src="figures/x.png")

doc.flush()
