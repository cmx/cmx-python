#!/usr/bin/env python3
"""Generate plugin.json with version from VERSION file"""
import json
from pathlib import Path

# Read version from VERSION file
root = Path(__file__).parent.parent
with open(root / "VERSION") as f:
    version = f.read().strip()

# Plugin configuration
plugin = {
    "name": "cmx",
    "version": version,
    "description": "CMX - REPL with Python Scripts via live documents",
    "author": "Ge Yang",
    "skills": [
        {
            "name": "cmx-basics",
            "description": "Basic usage patterns and quick start guide for CMX",
            "file": "cmx-basics.md"
        },
        {
            "name": "cmx-components",
            "description": "Guide to using CMX components (tables, images, videos, etc.)",
            "file": "cmx-components.md"
        }
    ]
}

# Write plugin.json
plugin_path = Path(__file__).parent / "plugin.json"
with open(plugin_path, "w") as f:
    json.dump(plugin, f, indent=2)
    f.write("\n")

print(f"Generated plugin.json with version {version}")
