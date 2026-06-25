```python
doc @ "# CMX Operator Syntax Examples"
doc @ "This document demonstrates all available syntax variations for adding content to CMX documents."
```
# CMX Operator Syntax Examples
This document demonstrates all available syntax variations for adding content to CMX documents.
```python
doc @ "## 1. Prefix @ Operator (Single Line)"
doc @ "The `@` operator can be used as a prefix for single-line strings:"
doc.print('Syntax: doc @ "text"')
```
## 1. Prefix @ Operator (Single Line)
The `@` operator can be used as a prefix for single-line strings:

```
Syntax: doc @ "text"
```
```python
doc @ "## 2. Prefix @ Operator (Multi-Line)"
doc @ "The `@` operator also works with multi-line strings using triple quotes:"

doc @ """
```
## 2. Prefix @ Operator (Multi-Line)
The `@` operator also works with multi-line strings using triple quotes:

This is a multi-line text block using the prefix @ operator.
It can span multiple lines and preserves formatting.

- Bullet point 1
- Bullet point 2
- Bullet point 3
```python
"## 3. Postfix | (Pipe) Operator (Single Line)" | doc
"The pipe operator can be used postfix-style, similar to Unix pipes:" | doc
doc.print('Syntax: "text" | doc')
```
## 3. Postfix | (Pipe) Operator (Single Line)
The pipe operator can be used postfix-style, similar to Unix pipes:

```
Syntax: "text" | doc
```
```python
"## 4. Postfix | (Pipe) Operator (Multi-Line)" | doc
"The pipe operator also works with multi-line strings:" | doc

"""
```
## 4. Postfix | (Pipe) Operator (Multi-Line)
The pipe operator also works with multi-line strings:

This is a multi-line text block using the postfix pipe operator.
It reads like a Unix pipeline, which may be familiar to shell users.

Key advantages:
1. Familiar syntax for Unix/Linux users
2. Natural left-to-right reading flow
3. Potential for future chaining
```python
doc("## 5. Traditional doc() Call Syntax")
doc("The traditional function call syntax is still available and recommended for complex cases:")
doc("- Explicit and clear")
doc("- Supports additional parameters")
doc("- Works well with linters and IDEs")
```
## 5. Traditional doc() Call Syntax
The traditional function call syntax is still available and recommended for complex cases:
- Explicit and clear
- Supports additional parameters
- Works well with linters and IDEs
```python
doc @ "## 6. Comparison and Mixed Usage"

doc("You can mix and match these syntaxes as needed:")
doc.print()

# Using traditional call
doc('Using traditional call: doc("text")')

# Using prefix @
doc @ 'Using prefix @: doc @ "text"'

# Using postfix |
'Using postfix |: "text" | doc' | doc

doc.print()
doc("All three methods are functionally equivalent and produce the same output.")
```
## 6. Comparison and Mixed Usage
You can mix and match these syntaxes as needed:

```
```
Using traditional call: doc("text")
Using prefix @: doc @ "text"
Using postfix |: "text" | doc

```
```
All three methods are functionally equivalent and produce the same output.
```python
doc @ "## 7. Best Practices"

"""
```
## 7. Best Practices

### When to Use Each Syntax

**Prefix @ Operator (`doc @ "text"`)**
- Quick, concise text addition
- Good for simple markdown strings
- Clean and minimal syntax

**Postfix | Operator (`"text" | doc`)**
- Unix-style pipeline feel
- Good for data transformation chains (future)
- Familiar to shell users

**Traditional Call (`doc("text")`)**
- Complex cases with parameters
- When using IDE autocomplete
- Maximum clarity and explicitness

### General Guidelines

1. Choose the syntax that makes your code most readable
2. Be consistent within a single file
3. Use traditional calls when passing additional parameters
4. Use operators for simple text additions
```python
doc @ "## 8. Code Block Testing"
"This section tests that code blocks have proper spacing:" | doc

doc.print("Some output before code block")
```
## 8. Code Block Testing
This section tests that code blocks have proper spacing:

```
Some output before code block
```
```python
doc @ "## 9. Final Notes"
doc("This document demonstrates that all operator syntaxes work correctly.")
doc("The markdown output should be properly formatted with correct spacing between all elements.")
```
## 9. Final Notes
This document demonstrates that all operator syntaxes work correctly.
The markdown output should be properly formatted with correct spacing between all elements.
