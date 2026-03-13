# CMX Components Skill

This skill provides detailed guidance on using CMX's rich components for creating comprehensive documentation.

## Component Overview

CMX provides several component types for different content:

- **Text & Print**: Text output
- **Table**: Tabular data from DataFrames or CSV
- **Image**: Image embedding with auto-save
- **Video**: Video and GIF embedding
- **Figure**: Images with captions and titles
- **YAML**: Structured data display
- **Layout**: Row containers for horizontal arrangement

## Text Components

### Print Component

Works like Python's built-in `print()`:

```python
from cmx import doc

with doc:
    doc.print("Single line")
    doc.print("Multiple", "arguments", sep="-")
    doc.print("No newline", end='')
    doc.print(" continues here")
```

Output:
```
Single line
Multiple-arguments
No newline continues here
```

### Markdown Text

Add raw markdown using `doc()` or `doc.md()`:

```python
with doc:
    doc("# Heading 1")
    doc("## Heading 2")
    doc("**Bold** and *italic* text")
    doc("- List item 1")
    doc("- List item 2")
```

## Table Component

Display DataFrames or CSV data as markdown tables:

```python
import pandas as pd
from cmx import doc

# From DataFrame
df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'Score': [95, 87, 92]
})

with doc:
    doc("# Results Table")
    doc.table(df, show_index=False)
```

Output:
```markdown
| Name    | Age | Score |
|---------|-----|-------|
| Alice   | 25  | 95    |
| Bob     | 30  | 87    |
| Charlie | 35  | 92    |
```

## Image Component

Save and display images:

```python
import numpy as np
from cmx import doc

# Create or load image data
image = np.random.rand(100, 100, 3)  # RGB image

with doc:
    # Save and display
    doc.image(image, src="figures/random.png")

    # With normalization
    doc.image(image, src="figures/normalized.png", normalize=True)

    # Just display existing image
    doc.image(src="figures/existing.png", width="50%")
```

### Image Attributes

- `image`: NumPy array (optional if `src` points to existing file)
- `src`: Path to save/load image
- `normalize`: Normalize pixel values to [0, 255]
- `width`, `height`: Size attributes (CSS values like "50%" or "300px")

## Figure Component

Images with titles and captions:

```python
from cmx import doc
import matplotlib.pyplot as plt

# Create a plot
plt.figure(figsize=(8, 6))
plt.plot([1, 2, 3, 4], [1, 4, 9, 16])
plt.xlabel('X axis')
plt.ylabel('Y axis')

with doc:
    doc.figure(
        src="figures/plot.png",
        title="Quadratic Function",
        caption="Plot showing y = x²",
        width="80%"
    )
```

### Using Savefig

Directly save the current matplotlib figure:

```python
import matplotlib.pyplot as plt
from cmx import doc

plt.plot([1, 2, 3], [1, 2, 3])

with doc:
    doc.savefig("figures/simple.png", caption="A simple line plot")
```

## Video Component

Embed videos and GIFs:

```python
import numpy as np
from cmx import doc

# Create video frames (T, H, W, C)
frames = np.random.randint(0, 255, (30, 100, 100, 3), dtype=np.uint8)

with doc:
    # Save and display as GIF
    doc.video(frames, src="videos/animation.gif")

    # Display existing video
    doc.video(src="videos/demo.mp4", width="640", height="480")
```

### Video Formats

- `.gif`: Displays as an image (works everywhere)
- `.mp4`, `.webm`: Displays as HTML5 video (HTML backend only)

## YAML Component

Display structured data in YAML format:

```python
from cmx import doc

config = {
    'model': {
        'name': 'ResNet50',
        'layers': 50,
        'pretrained': True
    },
    'training': {
        'batch_size': 32,
        'learning_rate': 0.001,
        'epochs': 100
    }
}

with doc:
    doc("# Configuration")
    doc.yaml(config)
```

Output:
```yaml
model:
  name: ResNet50
  layers: 50
  pretrained: true
training:
  batch_size: 32
  learning_rate: 0.001
  epochs: 100
```

## Layout Components

### Row Layout

Arrange components horizontally (HTML backend):

```python
import numpy as np
from cmx import doc

img1 = np.random.rand(100, 100, 3)
img2 = np.random.rand(100, 100, 3)

with doc:
    doc("# Side-by-side Images")
    with doc.row:
        doc.image(img1, src="img1.png")
        doc.image(img2, src="img2.png")
```

Note: Row layouts use HTML and work best in rendered markdown or HTML output.

## Advanced Usage

### Combining Components

```python
from cmx import doc
import pandas as pd
import matplotlib.pyplot as plt

# Data
data = pd.DataFrame({
    'x': range(10),
    'y': [i**2 for i in range(10)]
})

# Plot
plt.figure(figsize=(10, 6))
plt.plot(data['x'], data['y'])

with doc:
    doc("# Analysis Results")

    doc("## Data Table")
    doc.table(data)

    doc("## Visualization")
    doc.savefig("figures/analysis.png", caption="Quadratic growth pattern")

    doc("## Summary Statistics")
    doc.yaml(data.describe().to_dict())
```

### Custom Component Styling

Components support custom attributes:

```python
with doc:
    # Custom width and alignment
    doc.image(img, src="wide.png", width="100%", style="border: 1px solid black")

    # Custom table styling
    doc.table(df, class_name="custom-table")
```

## Component Backends

Different backends render components differently:

- **Markdown**: Maximum compatibility, works on GitHub
- **HTML**: Rich formatting, interactive elements
- **LaTeX**: Academic papers, publication-ready

Switch backends:

```python
from cmx.backends.html import HTML
from cmx.backends.latex import LaTeX

# Use HTML backend
doc = HTML(filename="output.html")

# Use LaTeX backend
doc = LaTeX(filename="output.tex")
```

## Best Practices

1. **Use meaningful filenames**: `figures/training_loss.png` not `fig1.png`
2. **Add captions**: Help readers understand visualizations
3. **Normalize images**: Use `normalize=True` for consistent display
4. **Keep tables readable**: Don't show too many rows/columns
5. **Organize outputs**: Use subdirectories (`figures/`, `videos/`, etc.)

## Troubleshooting

### Images not displaying

- Check that the `src` path is correct
- Ensure the directory exists (CMX doesn't create directories)
- For remote logging, verify logger configuration

### Tables not formatting correctly

- Ensure data is a pandas DataFrame
- Check for special characters that might break markdown
- Use `show_index=False` to hide the index column

### Videos not playing

- GIFs work everywhere, MP4 only in HTML backend
- Check file size (large videos might not display)
- Verify codec compatibility for MP4 files

## Learn More

- API Reference: https://cmx-python.readthedocs.io/en/latest/api/
- Examples: Check `examples/` directory in the repository
- Component source: `src/cmx/backends/components.py`
