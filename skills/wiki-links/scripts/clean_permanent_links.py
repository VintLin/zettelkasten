#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import List, Set, Tuple

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from sync_argument_links import ARG_DIR, LINK_LINE_RE, PERM_DIR, ROOT, collect_targets, read_text  # noqa: E402


def load_all_argument_ids() -> Set[str]:
    return {path.stem for path in ARG_DIR.glob("*.md")}


def find_links_section(lines: List[str]) -> Tuple[int, int]:
    start = -1
    for i, line in enumerate(lines):
        if line.strip() == "## Links":
            start = i
            break
    if start == -1:
        return -1, -1
    end = len(lines)
    for i in range(start + 1, len(lines)):
        if lines[i].startswith("## "):
            end = i
            break
    return start, end


def clean_note(note_path: Path, all_argument_ids: Set[str], apply: bool) -> bool:
    text = read_text(note_path)
    lines = text.splitlines()
    start, end = find_links_section(lines)
    if start == -1:
        return False

    cleaned_block: List[str] = []
    changed = False

    for line in lines[start + 1 : end]:
        stripped = line.strip()
        if not stripped:
            continue
        m = LINK_LINE_RE.match(line)
        if not m:
            changed = True
            continue
        kind, target_id = m.group(1), m.group(2)
        if kind == "supports" and target_id not in all_argument_ids:
            changed = True
            continue
        cleaned_block.append(stripped)

    replacement = ["## Links"] + cleaned_block
    if end < len(lines) and lines[end].strip():
        replacement.append("")

    if lines[start:end] != replacement:
        changed = True
        if apply:
            lines[start:end] = replacement
            new_text = "\n".join(lines) + ("\n" if text.endswith("\n") else "")
            note_path.write_text(new_text, encoding="utf-8")
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Clean permanent-note `## Links` blocks by keeping only valid `supports` to argument notes and `next` links."
    )
    parser.add_argument("targets", nargs="*", help="Permanent-note files, directories, or globs. Default: wiki/permanent-notes/*.md")
    parser.add_argument("--apply", action="store_true", help="Write changes. Default is dry-run.")
    args = parser.parse_args()

    targets = collect_targets(args.targets) if args.targets else sorted(PERM_DIR.glob("*.md"))
    note_paths = [path for path in targets if path.parent == PERM_DIR and path.suffix == ".md"]
    all_argument_ids = load_all_argument_ids()

    changed = 0
    for note_path in note_paths:
        if clean_note(note_path, all_argument_ids, args.apply):
            changed += 1
            prefix = "cleaned" if args.apply else "would clean"
            print(f"{prefix} {note_path.relative_to(ROOT)}")

    mode = "apply" if args.apply else "dry-run"
    print(f"\nDone ({mode}). changed={changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
