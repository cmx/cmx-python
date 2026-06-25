
# Markdown Operators: @ and |

CMX supports two syntax styles for adding markdown content.

````python
doc @ "## Prefix @ Operator"
"""
The `@` operator comes before the content:
```python
doc @ "Some markdown text"
```
""" | doc  # Using postfix | for demonstration!
````
## Prefix @ Operator

The `@` operator comes before the content:
```python
doc @ "Some markdown text"
```

## Postfix | Operator

The `|` operator comes after the content:
```python
"Some markdown text" | doc
```

```python
doc @ "## Mixed Syntax"
"You can mix both styles in the same code:" | doc

values = [1, 2, 3, 4, 5]
total = sum(values)
doc.print(f"Total: {total}")
```
## Mixed Syntax
You can mix both styles in the same code:

```
Total: 15
```
