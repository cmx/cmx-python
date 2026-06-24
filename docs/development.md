# Development Guide

This guide covers how to set up a development environment, contribute to CMX, and publish new releases.

## Setting Up Development Environment

### Clone the Repository

```bash
git clone https://github.com/cmx/cmx-python.git
cd cmx-python
```

### Install Development Dependencies

Install the package in development mode with all dependencies:

```bash
make dev
```

This will:
1. Build a wheel distribution
2. Install it with `pip install --ignore-installed`

Alternatively, you can install manually:

```bash
pip install -e ".[dev]"
```

## Development Workflow

### Running Tests

Run the test suite using pytest:

```bash
make test
```

Or run pytest directly:

```bash
python -m pytest tests --capture=no
```

### Code Quality

The project uses several tools for code quality:

#### Black (Code Formatting)

Format your code with Black (line length: 120):

```bash
black src/cmx tests examples
```

#### Pylint (Linting)

Check code quality with Pylint:

```bash
pylint src/cmx
```

#### Pyright (Type Checking)

The project includes Pyright configuration in `pyproject.toml`. Configure your IDE to use it for type checking.

### Building Documentation

#### Local Preview

Preview documentation locally with auto-reload:

```bash
make preview
```

This starts a server at `http://localhost:8888` that automatically rebuilds when you change documentation files.

#### Build HTML Documentation

Build the documentation without starting a server:

```bash
make docs
```

The built documentation will be in `docs/_build/html/`.

## Project Structure

```
cmx-python/
├── src/
│   └── cmx/              # Main package source code
│       ├── __init__.py
│       ├── backends/     # Output backends (Markdown, HTML, LaTeX)
│       ├── data.py       # Data utilities
│       ├── server/       # Server components
│       ├── utils.py      # Utility functions
│       └── with_hack.py  # Context manager utilities
├── docs/                 # Sphinx documentation
│   ├── conf.py          # Sphinx configuration
│   ├── index.md         # Documentation home page
│   ├── overview.md      # Quick start guide
│   ├── development.md   # This file
│   └── api/             # API documentation
├── examples/            # Example scripts
│   ├── old_demos/       # Legacy examples
│   └── three/           # 3D visualization examples
├── tests/               # Test suite
├── .claude-plugin/      # Claude Code skills
├── pyproject.toml       # Project configuration
├── Makefile            # Build automation
└── VERSION             # Version number
```

## Making Changes

### Adding New Features

1. Create a new branch for your feature:
   ```bash
   git checkout -b feature/my-new-feature
   ```

2. Implement your changes in `src/cmx/`

3. Add tests in `tests/`

4. Update documentation in `docs/`

5. Run tests to ensure everything works:
   ```bash
   make test
   ```

6. Format your code:
   ```bash
   black src/cmx tests
   ```

### Adding Examples

Add example scripts to the `examples/` directory:

```python
# examples/my_example.py
from cmx import doc

doc.config(filename="examples/my_example.md")

with doc:
    doc("# My Example")
    doc.print("Hello from my example!")
```

## Publishing

### Building a Release

1. Update the version in `VERSION` file:
   ```bash
   echo "0.0.47" > VERSION
   ```

2. Update the changelog in `docs/CHANGE_LOG.md`

3. Build the wheel:
   ```bash
   make wheel
   ```

### Publishing to PyPI

Publish the package to PyPI:

```bash
make publish
```

This will:
1. Convert README.md to reStructuredText
2. Run tests
3. Build the wheel
4. Upload to PyPI using twine

**Note**: You need PyPI credentials configured. Set them up with:
```bash
pip install twine
```

### Creating a Release Tag

Tag the release and push to GitHub:

```bash
make release msg="Release version 0.0.47"
```

This creates a git tag and pushes it to the remote repository.

## Contributing

### Pull Request Process

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests and documentation
5. Ensure all tests pass
6. Submit a pull request

### Code Style Guidelines

- Follow PEP 8 (enforced by Black with 120 character line length)
- Add docstrings to all public functions and classes
- Include type hints where appropriate
- Keep functions focused and simple
- Add comments for complex logic

### Commit Message Guidelines

Use clear, descriptive commit messages:

- **Good**: "Add support for video embedding in markdown backend"
- **Bad**: "Fixed stuff"

## Troubleshooting

### Import Errors After Installation

If you get import errors after installing in development mode, try:

```bash
pip uninstall cmx
make dev
```

### Documentation Build Errors

If documentation fails to build:

1. Check that all dependencies are installed:
   ```bash
   pip install -r docs/requirements.txt
   ```

2. Clean the build directory:
   ```bash
   rm -rf docs/_build
   ```

3. Try building again:
   ```bash
   make docs
   ```

### Test Failures

If tests fail:

1. Check that all dependencies are installed:
   ```bash
   pip install -e ".[dev]"
   ```

2. Run tests with verbose output:
   ```bash
   python -m pytest tests -v
   ```

## Getting Help

- **Issues**: Report bugs on [GitHub Issues](https://github.com/cmx/cmx-python/issues)
- **Discussions**: Ask questions in [GitHub Discussions](https://github.com/cmx/cmx-python/discussions)
- **Email**: Contact the maintainer at yangge1987@gmail.com
