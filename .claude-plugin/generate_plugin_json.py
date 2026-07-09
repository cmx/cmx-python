#!/usr/bin/env python3
"""Generate plugin.json with version from VERSION file"""
import json
from pathlib import Path

# Read version from VERSION file
root = Path(__file__).parent.parent
with open(root / "VERSION") as f:
    version = f.read().strip()

# Plugin configuration. Skills are auto-discovered from skills/<name>/SKILL.md
# at the plugin root -- they are not declared here.
plugin = {
    "name": "cmx",
    "displayName": "CMX",
    "version": version,
    "description": "CMX - REPL with Python Scripts via live documents",
    "author": {"name": "Ge Yang"},
    "homepage": "https://cmx-python.readthedocs.io",
    "repository": "https://github.com/cmx/cmx-python",
    "license": "MIT",
    "keywords": ["documentation", "python", "markdown", "jupyter", "notebooks"],
}

# Write plugin.json
plugin_path = Path(__file__).parent / "plugin.json"
with open(plugin_path, "w") as f:
    json.dump(plugin, f, indent=2)
    f.write("\n")

print(f"Generated plugin.json with version {version}")
