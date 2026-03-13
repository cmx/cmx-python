# Installation

**Questions**
- How do I install CMX?
- What are the system requirements?
- How do I verify the installation?

**Objectives**
- Install CMX using pip
- Verify the installation works

## Requirements

CMX requires Python 3.7 or later.

## Install from PyPI

```bash
pip install cmx
```

## Verify Installation

Create a test script to verify CMX is working:

```python
from cmx import doc

doc.config(filename="test.md")

with doc:
    doc @ "# Installation Test"
    doc.print("CMX is working!")

doc.flush()
```

Run the script and check that `test.md` is created.

## Key Points

- CMX requires Python 3.7+
- Install with `pip install cmx`
- Verify by creating a simple document

## Next Steps

- [Overview](overview.md) - Learn the basic workflow
- [Markdown](markdown.md) - Add text to documents
