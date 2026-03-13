
# Working with Tables

Tables are essential for displaying data and results.
```python
"## Simple DataFrame" | doc  # Using postfix pipe syntax

# Create a pandas DataFrame
data = pd.DataFrame(
    {
        "Model": ["ResNet50", "VGG16", "MobileNet"],
        "Accuracy": [0.95, 0.87, 0.92],
        "Parameters": ["25.6M", "138M", "4.2M"],
    }
)

doc.table(data)
```
## Simple DataFrame
| Model     |   Accuracy | Parameters   |
|-----------|------------|--------------|
| ResNet50  |       0.95 | 25.6M        |
| VGG16     |       0.87 | 138M         |
| MobileNet |       0.92 | 4.2M         |
```python
doc @ "## Experiment Results"
"Here's a typical use case - showing experiment metrics:" | doc  # Mix both syntaxes

results = pd.DataFrame(
    {
        "Experiment": ["baseline", "optimized", "final"],
        "Success Rate": ["45.2%", "67.8%", "89.1%"],
        "Trials": [100, 100, 100],
    }
)

doc.table(results, show_index=False)
```
## Experiment Results
Here's a typical use case - showing experiment metrics:
| Experiment   | Success Rate   |   Trials |
|--------------|----------------|----------|
| baseline     | 45.2%          |      100 |
| optimized    | 67.8%          |      100 |
| final        | 89.1%          |      100 |

## Markdown Table Syntax

You can also create tables manually in markdown:

| Checkpoint | Success | Num Trials |
| ---------- | ------- | ---------- |
| v1         | 45.2%   | 100        |
| v2         | 67.8%   | 100        |
| v3         | 89.1%   | 100        |
