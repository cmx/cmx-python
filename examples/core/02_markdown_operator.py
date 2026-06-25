"""
Markdown Operators Example

This example shows both the @ and | operator patterns for adding markdown.
The @ operator is prefix (doc @ "text") while | is postfix ("text" | doc).
"""

from cmx import doc

doc.config(__file__)

# Using prefix @ operator for multi-line content
doc @ """
# Markdown Operators: @ and |

CMX supports two syntax styles for adding markdown content.
"""

with doc:
    doc @ "## Prefix @ Operator"
    """
    The `@` operator comes before the content:
    ```python
    doc @ "Some markdown text"
    ```
    """ | doc  # Using postfix | for demonstration!

# Using postfix | operator
"""
## Postfix | Operator

The `|` operator comes after the content:
```python
"Some markdown text" | doc
```
""" | doc

with doc:
    doc @ "## Mixed Syntax"
    "You can mix both styles in the same code:" | doc

    values = [1, 2, 3, 4, 5]
    total = sum(values)
    doc.print(f"Total: {total}")

doc.flush()

print("\n✓ Markdown operator example complete! Check 02_markdown_operator.md next to the script.")
