"""
# Introducing CMX

> use Python Scripts as live documents.

## See CMX In Action
"""
from cmx import doc
import matplotlib.pyplot as plt

doc.config("README.md")
doc(__doc__)

doc("""
this works just like a standard jupyter notebook. Only code you include in 
an `cm` block would be shown.
""")
with doc:
    for i in range(10):
        doc.print(i, end=' ')

doc("""
## Installation

You can install this package from PyPI under the `cmx` package name.

``` python
pip install mdx
```
## Developing Plugins

You can develop plug-ins under the `cmx-<>` prefix

## Discussion

Can we have a `travel-back-in-time` debugger that saves the stack
at each frame?

## To-dos

- [ ] advanced layout
- [ ] saving matplotlib figures
- [ ] video component

    ``` python
    cm.video(url="https://")
    ```

- [ ] image component
- [ ] table component
- [ ] scope inspection component

### Tomorrow

### Done

- [x] simple text output
""")