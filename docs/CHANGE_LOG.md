# Changelog

All notable changes to CMX will be documented in this file.

## [0.0.46] - Current

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
