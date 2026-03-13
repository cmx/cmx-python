# Tables

**Questions**
- How do I display pandas DataFrames?
- How do I create tables from CSV data?
- How do I control the index column?

**Objectives**
- Display DataFrames as markdown tables
- Load and display CSV tables
- Control table formatting

## Basic DataFrame Table

Display a pandas DataFrame:

```python
from cmx import doc
import pandas as pd

doc.config(filename="output.md")

with doc:
    doc @ "## Model Comparison"

    data = pd.DataFrame({
        'Model': ['ResNet50', 'VGG16', 'MobileNet'],
        'Accuracy': [0.95, 0.87, 0.92],
        'Parameters': ['25.6M', '138M', '4.2M']
    })

    doc.table(data)

doc.flush()
```

## CSV Tables

Load and display CSV data:

```python
data = pd.read_csv("results.csv")

with doc:
    doc.table(data)
```

## Hiding the Index

Use `show_index=False` to hide row numbers:

```python
with doc:
    results = pd.DataFrame({
        'Experiment': ['baseline', 'optimized', 'final'],
        'Success Rate': ['45.2%', '67.8%', '89.1%']
    })

    doc.table(results, show_index=False)
```

## Markdown Table Syntax

You can also write tables in markdown:

```python
doc @ """
| Model      | Accuracy | Parameters |
| ---------- | -------- | ---------- |
| ResNet50   | 95%      | 25.6M      |
| VGG16      | 87%      | 138M       |
| MobileNet  | 92%      | 4.2M       |
"""
```

## Key Points

- Use `doc.table(dataframe)` to display DataFrames
- Works with CSV data loaded via pandas
- Use `show_index=False` to hide row numbers
- Can write tables manually in markdown

## Next Steps

- [Images](images.md) - Display images
- [YAML](yaml.md) - Display configuration
