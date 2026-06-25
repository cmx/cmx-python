"""Code content containing a 3-backtick run -- expect a 4-backtick outer fence."""
import os

from cmx.backends.markdown import CommonMark

doc = CommonMark(filename=os.environ.get("CMX_GOLDEN_OUT", "nested_fence.md"))

doc.pre("here:\n```python\nx=1\n```", lang="markdown")

doc.flush()
