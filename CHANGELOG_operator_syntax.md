# CMX Operator Syntax Update - Changelog

**Date:** 2026-03-12

## Summary

This update fixes critical markdown formatting issues and implements new string processing syntax features for CMX.

## Changes Made

### 1. Fixed Markdown Output Formatting

**Issue:** Generated markdown had formatting problems where text would run directly into code blocks without proper newlines (e.g., `examples/core/01_basic_usage.md` line 6-7).

**Root Cause:** The `Span` component's `_md` property was not ensuring text ended with a newline, causing consecutive components to run together.

**Fix:**
- Modified `/Users/ge/fortyfive/cmx-python/src/cmx/backends/components.py`:
  - Updated `Span._md` property to ensure text ends with a newline for proper markdown formatting
  - Simplified `Article._md` property to concatenate component markdown output directly

**Files Modified:**
- `src/cmx/backends/components.py` (lines 119-123, 422-425)

### 2. Implemented Postfix Pipe Syntax

**Feature:** Added support for `"""...""" | doc` syntax using Python's `__ror__` operator.

**Implementation:**
- Added `__ror__` method to `CommonMark` class for postfix pipe syntax
- Added `__or__` method (reserved for future use)
- Enhanced docstrings for all operator methods

**Files Modified:**
- `src/cmx/backends/markdown.py` (lines 172-188)

**Syntax Now Supported:**
```python
# Prefix @ operator
doc @ "text"
doc @ """multiline text"""

# Postfix pipe operator (NEW)
"text" | doc
"""multiline text""" | doc

# Traditional call syntax (still works)
doc("text")
```

### 3. Created Comprehensive Documentation

**New File:** `docs/operator_overloading.md`

This documentation provides:
- Complete overview of Python operator overloading for string processing
- Detailed explanation of implemented operators (`__matmul__`, `__ror__`, `__or__`)
- Discussion of other potentially useful operators (with pros/cons)
- Best practices and recommendations
- Code examples for each syntax variation

### 4. Created Test Suite

**New File:** `tests/test_operator_syntax.py`

Comprehensive unit tests covering:
- Prefix @ operator with single-line strings
- Prefix @ operator with multi-line strings
- Postfix | operator with single-line strings
- Postfix | operator with multi-line strings
- Mixed syntax usage in one document
- Markdown formatting validation

All tests pass successfully.

### 5. Created Example File

**New File:** `examples/core/09_operator_syntax.py`

Demonstrates all syntax variations with real-world examples:
- Shows all four operator combinations
- Compares traditional call vs operator syntax
- Provides best practice guidelines
- Tests proper markdown spacing

### 6. Re-ran All Examples

All existing examples were re-run to verify proper markdown output:
- ✓ `examples/core/01_basic_usage.py`
- ✓ `examples/core/02_markdown_operator.py`
- ✓ `examples/core/03_tables.py`
- ✓ `examples/core/05_yaml_output.py`
- ✓ `examples/core/06_hiding_code.py`
- ✓ `examples/core/08_comprehensive.py`
- ✓ `examples/core/09_operator_syntax.py` (NEW)

All examples now produce properly formatted markdown with correct spacing between text and code blocks.

## Technical Details

### Operator Overloading Methods

#### `__matmul__` (@ operator)
```python
def __matmul__(self, string_or_array):
    """Support prefix @ syntax: doc @ "text" or doc @ '''text'''"""
    if isinstance(string_or_array, tuple):
        string, *rest = string_or_array
        return self(string, *rest)
    return self(string_or_array)
```

#### `__ror__` (reverse | operator)
```python
def __ror__(self, string_or_array):
    """Support postfix pipe syntax: "text" | doc or '''text''' | doc"""
    if isinstance(string_or_array, tuple):
        string, *rest = string_or_array
        return self(string, *rest)
    return self(string_or_array)
```

### Markdown Formatting Fix

#### Before:
```python
@property
def _md(self):
    return self.text
```

#### After:
```python
@property
def _md(self):
    # Ensure text ends with newline for proper markdown formatting
    text = self.text
    if text and not text.endswith('\n'):
        text = text + '\n'
    return text
```

## Breaking Changes

None. All existing code continues to work as before.

## Migration Guide

No migration needed. The new syntax is optional and all existing syntax remains supported.

## Files Added

1. `docs/operator_overloading.md` - Comprehensive documentation
2. `tests/test_operator_syntax.py` - Test suite
3. `examples/core/09_operator_syntax.py` - Example demonstrating all syntax variations
4. `CHANGELOG_operator_syntax.md` - This file

## Files Modified

1. `src/cmx/backends/components.py` - Fixed markdown formatting
2. `src/cmx/backends/markdown.py` - Added postfix pipe operator support

## Verification

- All unit tests pass (6/6)
- All examples run successfully and produce valid markdown
- No regressions in existing functionality
- Markdown formatting issues resolved

## Future Enhancements

Potential additions documented in `docs/operator_overloading.md`:
- Left-side pipe operator (`__or__`) for chaining processors
- Stream-like insertion using `<<` operator
- Path-like navigation using `/` operator

## References

- [Python Data Model - Special Method Names](https://docs.python.org/3/reference/datamodel.html#special-method-names)
- [PEP 465 - A dedicated infix operator for matrix multiplication](https://www.python.org/dev/peps/pep-0465/)
