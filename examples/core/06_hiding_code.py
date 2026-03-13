"""
Hiding Code Example

This example demonstrates how to use doc.hide to run code
without showing it in the documentation.
"""

from cmx import doc

doc.config(filename="examples/core/06_hiding_code.md")

doc @ """
# Hiding Code Blocks

Sometimes you need to run setup code without showing it in the output.
"""

# This code runs but won't appear in the documentation
with doc.hide:
    # Load data, set up environment, etc.
    import numpy as np

    # Prepare some data
    data = np.random.randn(1000)
    mean = data.mean()
    std = data.std()

    doc @ "## Data Statistics (hidden setup)"

doc @ """
## Results

The analysis results are shown below, but the setup code is hidden.
"""

with doc:
    doc @ f"### Summary Statistics"
    doc.print(f"Mean: {mean:.4f}")
    doc.print(f"Std:  {std:.4f}")

doc @ """
## Use Cases for `doc.hide`

1. **Data loading**: Don't show file I/O code
2. **Environment setup**: Hide initialization details
3. **Expensive computations**: Show results but not the computation
4. **Helper functions**: Define utilities without cluttering docs
"""

with doc.hide:
    # This won't show up
    def helper_function():
        return "This is hidden"

    hidden_result = helper_function()

with doc:
    doc @ "## Using Hidden Results"
    doc.print("We can still use results from hidden code blocks!")

doc.flush()

print("\n✓ Hiding code example complete! Check examples/core/06_hiding_code.md")
