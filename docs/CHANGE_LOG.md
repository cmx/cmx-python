# Changelog

All notable changes to CMX will be documented in this file.

## [0.0.49] - 2026-06-25

### Added

- Lifecycle hooks for storage/integration: `on_mount`, `on_save`, `on_flush`, `on_close`, `on_error`, plus `on_block`, `on_hide`, `on_skip`. Override by subclassing `CommonMark` or binding a function on the instance (`doc.on_save = ...`). See the Hooks guide.
- `doc.config(__file__)` script-relative output; `figdir` template (default `{fname}`) with bare-name → figdir asset resolution.
- Overridable `end=` on text blocks (default `"\n"`).
- Pure-Python GitHub-table renderer (`md_table`); `tabulate` is no longer a runtime dependency.
- Golden-file test harness; suite expanded to 108 tests.

### Changed

- Block-aware Markdown rendering: a blank line is inserted before block elements, and code fences escalate their backtick count around nested fences.
- Dependency-free core with optional extras (`tables`/`images`/`figures`/`yaml`/`all`). Requires Python ≥ 3.11.
- Documentation revamped across all pages.

### Removed

- `SimpleLogger` — its I/O moved into the default lifecycle hooks (storage now flows through `on_save`/`on_flush`).

## [0.0.48] - 2026-06-25

### Added

- `doc.table(file=...)` and `doc.yaml(file=...)` load data straight from disk — csv/tsv/json/parquet/excel and list-of-records yaml (#18).
- Matplotlib figure documentation and example; `doc.savefig` matplotlib kwargs (`dpi`, `bbox_inches`, ...) are routed to matplotlib only and kept out of the `<img>` markup (#17).

## [0.0.46]

### Current Features

- REPL-style documentation generation from Python scripts
- Multiple output backends: Markdown, HTML, LaTeX
- Rich components: tables, images, videos, figures, YAML
- Context management with `with doc:` blocks
- Built-in file logger for saving images, videos, and text
- Layout components (rows, containers)
- Code block auto-capture
- Skip/hide functionality for development

### Components Available

- **Print**: Console-style text output
- **Text**: Markdown text blocks
- **Table**: DataFrame and CSV table rendering
- **Image**: Image embedding with auto-save
- **Video**: Video/GIF embedding
- **Figure**: Images with titles and captions
- **YAML**: Structured data display
- **Row**: Horizontal layout container

## Future Improvements

### Planned Features

- Scope inspection component
- Travel-back-in-time debugger with stack frame saving
- Enhanced plugin system under `cmx-<>` prefix
- Additional backend support

### In Development

- Video component enhancements
- Improved table formatting options
- Enhanced logging features

## Version History

### Done

- [x] Simple text output
- [x] Layout row component
- [x] Saving matplotlib figures
- [x] Video component with GIF support
- [x] Image component with normalization
- [x] Table component with pandas integration
- [x] YAML component

### Upcoming

- [ ] Scope inspection component
- [ ] Enhanced debugging features
- [ ] Plugin architecture improvements

---

For more details on any release, see the [GitHub releases page](https://github.com/cmx/cmx-python/releases).
