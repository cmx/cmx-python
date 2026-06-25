"""
Basic Usage Example

This example demonstrates the fundamental features of CMX:
- Using the `with doc:` context manager
- Adding markdown text with @ and | operators
- Printing output with doc.print()
"""

from cmx import doc

# Configure output file (anchored to this script's directory)
doc.config(__file__)

# Add a title using the @ operator (prefix syntax)
doc @ "# Basic CMX Usage"
doc @ "This demonstrates the core features of CMX."

# Show some code and its output
with doc:
    doc @ "## Simple Loop"
    "Let's print numbers from 0 to 9:" | doc  # Postfix pipe syntax

    for i in range(10):
        doc.print(i, end=" ")

# You can add multiple sections
with doc:
    doc @ "## Calculations"
    "CMX captures both code and output:" | doc

    result = sum(range(100))
    doc.print(f"Sum of 0-99: {result}")

    # More complex calculation
    squares = [i**2 for i in range(10)]
    doc.print(f"First 10 squares: {squares}")

# Don't forget to flush at the end
doc.flush()

print("\n✓ Basic usage example complete! Check 01_basic_usage.md next to the script.")
