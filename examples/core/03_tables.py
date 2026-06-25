"""
Tables Example

This example demonstrates how to create tables in CMX,
a common pattern for displaying experimental results.
"""

from cmx import doc
import pandas as pd

doc.config(__file__)

doc @ """
# Working with Tables

Tables are essential for displaying data and results.
"""

with doc:
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

with doc:
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

doc @ """
## Markdown Table Syntax

You can also create tables manually in markdown:

| Checkpoint | Success | Num Trials |
| ---------- | ------- | ---------- |
| v1         | 45.2%   | 100        |
| v2         | 67.8%   | 100        |
| v3         | 89.1%   | 100        |
"""

doc.flush()

print("\n✓ Tables example complete! Check 03_tables.md next to the script.")
