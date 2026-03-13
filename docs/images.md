# Images

**Questions**
- How do I display images in documentation?
- How do I save and reference images?
- How do I arrange images side-by-side?

**Objectives**
- Display numpy arrays as images
- Save images to specific paths
- Arrange images horizontally

## Basic Image Display

Display a numpy array as an image:

```python
from cmx import doc
import numpy as np

doc.config(filename="output.md")

with doc:
    doc @ "## Random Image"

    # Create RGB image (height, width, 3)
    image = np.random.rand(100, 100, 3)
    image = (image * 255).astype(np.uint8)

    doc.image(image, src="figures/random.png")

doc.flush()
```

The image is saved to `figures/random.png` and displayed in the markdown.

## Multiple Images

Display several images:

```python
with doc:
    doc @ "## Results"

    doc.image(input_image, src="figures/input.png")
    doc.image(output_image, src="figures/output.png")
```

## Side-by-Side Layout

Use `doc.row()` to arrange images horizontally:

```python
with doc:
    doc @ "## Comparison"

    with doc.row():
        doc.image(before, src="figures/before.png")
        doc.image(after, src="figures/after.png")
```

## Key Points

- Use `doc.image(array, src="path.png")` to display images
- Images are saved to the specified path
- Use `doc.row()` to arrange images side-by-side
- Images must be numpy arrays (height, width, 3) for RGB

## Next Steps

- [Tables](tables.md) - Display data tables
- [YAML](yaml.md) - Display configuration
