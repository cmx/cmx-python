# Next Steps After Restructuring

This document outlines the immediate next steps to complete the repository restructuring and prepare for release.

## Immediate Actions (Required Before Commit)

### 1. Review Changes
```bash
# Review all changes
git status
git diff

# Check the new directory structure
tree -L 2 src/ docs/ .claude-plugin/
```

### 2. Test Basic Functionality

```bash
# Install in development mode
make dev

# This will:
# - Build a wheel
# - Install it with pip
```

### 3. Verify Import Works

```bash
# Test basic import
python3 -c "from cmx import doc; print('✓ Import successful')"
```

### 4. Run Tests

```bash
# Run the test suite
make test

# If tests fail, review and fix issues
```

### 5. Build Documentation Locally

```bash
# Preview documentation with live reload
make preview

# This opens http://localhost:8888 in your browser
# Check that all pages render correctly
```

## Post-Commit Actions

### 1. Set Up ReadTheDocs

1. Go to https://readthedocs.org
2. Sign in with GitHub account
3. Import the cmx-python project
4. Verify `.readthedocs.yaml` is detected
5. Trigger a build
6. Check that documentation builds successfully

**Expected URL**: https://cmx-python.readthedocs.io

### 2. Update Repository Settings

On GitHub, update:
- Repository description: "REPL with Python Scripts via live documents"
- Topics/Tags: `python`, `documentation`, `markdown`, `jupyter`, `notebooks`
- Website: Link to ReadTheDocs once live

### 3. Create a Release

```bash
# Update VERSION if needed
echo "0.0.47" > VERSION

# Update docs/CHANGE_LOG.md with new version notes

# Create release
make release msg="Restructure repository following vuer-doc-boilerplate"
```

### 4. Publish to PyPI (Optional)

If you want to publish this restructured version:

```bash
# Make sure tests pass
make test

# Build and publish
make publish
```

**Note**: This requires PyPI credentials configured with `twine`.

## Optional Enhancements

### 1. Add CI/CD

Create `.github/workflows/test.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, '3.10', '3.11']

    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: |
        pip install -e ".[dev]"
    - name: Run tests
      run: make test
```

### 2. Add Documentation Build Check

Create `.github/workflows/docs.yml`:

```yaml
name: Documentation

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    - name: Install dependencies
      run: |
        pip install -r docs/requirements.txt
        pip install -e .
    - name: Build documentation
      run: make docs
```

### 3. Add More Examples

Create basic example files in `examples/`:

```bash
examples/
├── basic_usage.py
├── tables_example.py
├── images_example.py
├── figures_example.py
├── yaml_example.py
└── layout_example.py
```

Each should demonstrate a specific feature with clear documentation.

### 4. Improve API Documentation

Add docstrings to all public methods in `src/cmx/`:
- Use Google or NumPy docstring style
- Include parameter types and return types
- Add usage examples in docstrings

### 5. Add Logo/Brand Assets

Create logo files for documentation:
```bash
docs/_static/
├── cmx-logo-light.png
└── cmx-logo-dark.png
```

Update `docs/conf.py` if logos are added.

## Testing Checklist

Before considering the restructuring complete, verify:

- [ ] `make dev` installs successfully
- [ ] `from cmx import doc` works
- [ ] `make test` passes all tests
- [ ] `make preview` builds docs without errors
- [ ] All documentation pages render correctly
- [ ] Examples in docs can be copy-pasted and work
- [ ] `make wheel` builds a distribution
- [ ] Installing the wheel works: `pip install dist/*.whl`
- [ ] README.md renders correctly on GitHub
- [ ] Links in README.md work
- [ ] Claude plugin files are valid JSON
- [ ] `.gitignore` excludes build artifacts

## Maintenance Tasks

### Regular Updates

1. **Version bumps**: Update `VERSION` file
2. **Changelog**: Add entries to `docs/CHANGE_LOG.md`
3. **Dependencies**: Keep `pyproject.toml` dependencies up to date
4. **Documentation**: Update docs when adding features

### Before Each Release

1. Update version in `VERSION`
2. Update `docs/CHANGE_LOG.md`
3. Run full test suite
4. Build and test documentation
5. Update README if needed
6. Tag release with `make release`

## Troubleshooting

### Import Errors

If imports fail after restructuring:

```bash
# Clean old installations
pip uninstall cmx

# Reinstall
make dev
```

### Documentation Build Errors

If docs fail to build:

```bash
# Clean build directory
rm -rf docs/_build

# Install all doc dependencies
pip install -r docs/requirements.txt

# Try building again
make docs
```

### Test Failures

If tests fail:

```bash
# Run tests with verbose output
python -m pytest tests -v

# Run a specific test
python -m pytest tests/test_cmx.py -v
```

### Git Issues

If git shows unexpected changes:

```bash
# See what changed
git status
git diff

# Restore specific files if needed
git restore <file>
```

## Getting Help

If you encounter issues:

1. Check `RESTRUCTURE_SUMMARY.md` for what changed
2. Review `docs/development.md` for development guidelines
3. Check the original boilerplate: https://github.com/vuer-ai/vuer-doc-boilerplate
4. Open an issue on GitHub

## Success Metrics

The restructuring is successful when:

1. ✅ Package installs from `pip install cmx`
2. ✅ Documentation builds on ReadTheDocs
3. ✅ All tests pass
4. ✅ Examples run without errors
5. ✅ Claude skills work in Claude Code
6. ✅ PyPI page looks professional
7. ✅ Contributors can easily set up development environment

## Future Roadmap

Consider these longer-term improvements:

1. **Testing**: Increase test coverage to >80%
2. **Examples**: Add 10+ comprehensive examples
3. **Backends**: Add PDF output backend
4. **Integration**: Add VS Code extension
5. **Performance**: Optimize large document generation
6. **Features**: Add real-time collaboration support

---

**Last Updated**: 2026-03-12
**Status**: Ready for review and testing
