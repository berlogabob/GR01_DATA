#!/usr/bin/env python3
from pathlib import Path

BLOCK = "\n**Assignee**: @me\n**Priority**:\n**Status**: Todo\n\n"
folder = Path(__file__).parent

for md_file in sorted(folder.glob("*.md")):
    if md_file.name == "script.py":
        continue

    content = md_file.read_text(encoding="utf-8")
    if BLOCK.strip() not in content:
        md_file.write_text(content + BLOCK, encoding="utf-8")
