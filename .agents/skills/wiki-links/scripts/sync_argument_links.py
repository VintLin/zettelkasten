#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple


ROOT = Path(__file__).resolve().parents[4]
ARG_DIR = ROOT / "wiki" / "argument-notes"
PERM_DIR = ROOT / "wiki" / "permanent-notes"

LIST_ITEM_RE = re.compile(r"^\d+\.\s+\[\[([^\]|]+)(?:\|([^\]]+))?\]\]")
LINK_LINE_RE = re.compile(r"^\s*-\s+(supports|next)\s+\[\[([^\]|]+)(?:\|([^\]]+))?\]\](.*)$")
BRANCH_RE = re.compile(r"^\*\*分叉\b.*\*\*\s*$")
HEADING_RE = re.compile(r"^##\s+")


@dataclass
class ArgumentChain:
    path: Path
    arg_id: str
    arg_title: str
    cited_ids: Set[str] = field(default_factory=set)
    next_map: Dict[str, Set[str]] = field(default_factory=dict)
    next_sources: Dict[str, Set[str]] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_frontmatter_value(text: str, key: str) -> Optional[str]:
    m = re.search(rf"(?m)^{re.escape(key)}:\s*(.+?)\s*$", text)
    if not m:
        return None
    value = m.group(1).strip()
    return value.strip('"').strip("'")


def extract_h1_title(text: str) -> Optional[str]:
    m = re.search(r"(?m)^#\s+(.+?)\s*$", text)
    return m.group(1).strip() if m else None


def clean_title(title: str) -> str:
    return title.strip().rstrip("?？")


def parse_argument(path: Path) -> ArgumentChain:
    text = read_text(path)
    arg_id = extract_frontmatter_value(text, "id") or path.stem
    arg_title = clean_title(extract_frontmatter_value(text, "title") or extract_h1_title(text) or path.stem)
    chain = ArgumentChain(path=path, arg_id=arg_id, arg_title=arg_title)

    start = text.find("### 论据")
    if start == -1:
        chain.warnings.append("missing `### 论据` section")
        return chain
    body = text[start:].split("## Links", 1)[0]
    lines = body.splitlines()

    last_linear: Optional[str] = None
    branch_anchor: Optional[str] = None
    in_branch = False
    current_branch_last: Optional[str] = None

    for raw_line in lines[1:]:
        line = raw_line.strip()
        if not line:
            continue
        if line == "---":
            last_linear = None
            branch_anchor = None
            in_branch = False
            current_branch_last = None
            continue
        if line.startswith(">"):
            continue
        if BRANCH_RE.match(line):
            if last_linear is None and branch_anchor is None:
                chain.warnings.append("branch marker without anchor")
            branch_anchor = last_linear if last_linear is not None else branch_anchor
            in_branch = True
            current_branch_last = None
            continue
        if HEADING_RE.match(line):
            break

        m = LIST_ITEM_RE.match(line)
        if not m:
            continue

        note_id = m.group(1)
        chain.cited_ids.add(note_id)

        if in_branch:
            if branch_anchor is None:
                chain.warnings.append(f"branch item `{note_id}` has no anchor")
            elif current_branch_last is None:
                chain.next_map.setdefault(branch_anchor, set()).add(note_id)
                chain.next_sources.setdefault(branch_anchor, set()).add(arg_id)
            else:
                chain.next_map.setdefault(current_branch_last, set()).add(note_id)
                chain.next_sources.setdefault(current_branch_last, set()).add(arg_id)
            current_branch_last = note_id
            continue

        if last_linear is not None:
            chain.next_map.setdefault(last_linear, set()).add(note_id)
            chain.next_sources.setdefault(last_linear, set()).add(arg_id)
        last_linear = note_id

    if not chain.cited_ids:
        chain.warnings.append("no permanent-note citations found under `### 论据`")
    return chain


def load_all_chains() -> List[ArgumentChain]:
    return [parse_argument(path) for path in sorted(ARG_DIR.glob("*.md"))]


def build_global_next_index(chains: List[ArgumentChain]) -> Dict[str, Set[str]]:
    index: Dict[str, Set[str]] = {}
    for chain in chains:
        for note_id, next_ids in chain.next_map.items():
            index.setdefault(note_id, set()).update(next_ids)
    return index


def build_global_next_source_index(chains: List[ArgumentChain]) -> Dict[str, Set[str]]:
    index: Dict[str, Set[str]] = {}
    for chain in chains:
        for note_id, source_args in chain.next_sources.items():
            index.setdefault(note_id, set()).update(source_args)
    return index


def note_title(note_id: str) -> str:
    path = PERM_DIR / f"{note_id}.md"
    if not path.exists():
        return note_id
    text = read_text(path)
    return clean_title(extract_frontmatter_value(text, "title") or extract_h1_title(text) or note_id)


def find_links_section(lines: List[str]) -> Tuple[int, int]:
    start = -1
    for i, line in enumerate(lines):
        if line.strip() == "## Links":
            start = i
            break
    if start == -1:
        insert_at = len(lines)
        for i, line in enumerate(lines):
            if line.startswith("## References"):
                insert_at = i
                break
        lines[insert_at:insert_at] = ["## Links", ""]
        start = insert_at

    end = len(lines)
    for i in range(start + 1, len(lines)):
        if lines[i].startswith("## "):
            end = i
            break
    return start, end


def sync_note_links(
    note_path: Path,
    chain: ArgumentChain,
    expected_nexts: Set[str],
    global_expected_nexts: Set[str],
    all_argument_ids: Set[str],
    prune_disallowed: bool = False,
) -> Tuple[bool, List[str]]:
    text = read_text(note_path)
    lines = text.splitlines()
    start, end = find_links_section(lines)
    block = lines[start + 1 : end]

    existing_supports: Dict[str, List[str]] = {}
    existing_nexts: Dict[str, List[str]] = {}
    preserved_other: List[str] = []

    for line in block:
        m = LINK_LINE_RE.match(line)
        if not m:
            if not prune_disallowed:
                preserved_other.append(line)
            continue
        kind, target_id = m.group(1), m.group(2)
        if kind == "supports":
            if prune_disallowed and target_id not in all_argument_ids:
                continue
            existing_supports.setdefault(target_id, []).append(line)
        else:
            existing_nexts.setdefault(target_id, []).append(line)

    note_id = note_path.stem
    affected_set = chain.cited_ids
    new_block: List[str] = []

    support_line = None
    if chain.arg_id in existing_supports and existing_supports[chain.arg_id]:
        support_line = existing_supports[chain.arg_id][0]
    else:
        support_line = f"- supports [[{chain.arg_id}|{chain.arg_title}]]"
    new_block.append(support_line)

    for next_id in sorted(expected_nexts):
        if next_id in existing_nexts and existing_nexts[next_id]:
            new_block.append(existing_nexts[next_id][0])
        else:
            new_block.append(f"- next [[{next_id}|{note_title(next_id)}]]")

    for target_id, link_lines in existing_supports.items():
        if target_id != chain.arg_id and link_lines:
            new_block.append(link_lines[0])

    for target_id, link_lines in existing_nexts.items():
        if not link_lines:
            continue
        if target_id in global_expected_nexts and target_id not in expected_nexts:
            new_block.append(link_lines[0])
            continue
        if target_id in affected_set:
            continue
        new_block.append(link_lines[0])

    if preserved_other:
        if new_block and preserved_other[0].strip():
            new_block.append("")
        new_block.extend(preserved_other)

    while new_block and new_block[-1] == "":
        new_block.pop()

    replacement = ["## Links"] + new_block
    if end < len(lines) and lines[end].strip():
        replacement.append("")

    old_section = lines[start:end]
    changed = old_section != replacement
    if changed:
        lines[start:end] = replacement
        new_text = "\n".join(lines) + ("\n" if text.endswith("\n") else "")
        note_path.write_text(new_text, encoding="utf-8")

    messages: List[str] = []
    if changed:
        messages.append(f"updated {note_path.relative_to(ROOT)}")
    return changed, messages


def collect_targets(raw_targets: List[str]) -> List[Path]:
    if not raw_targets:
        return sorted(ARG_DIR.glob("*.md"))
    result: List[Path] = []
    for raw in raw_targets:
        path = (ROOT / raw).resolve() if not raw.startswith("/") else Path(raw)
        if path.is_dir():
            result.extend(sorted(path.glob("*.md")))
        elif path.exists():
            result.append(path)
        else:
            matches = list(ROOT.glob(raw))
            result.extend(sorted(matches))
    seen = set()
    unique: List[Path] = []
    for path in result:
        if path in seen:
            continue
        seen.add(path)
        unique.append(path)
    return unique


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync supports/next links from argument notes into permanent notes.")
    parser.add_argument("targets", nargs="*", help="Argument-note files, directories, or globs. Default: wiki/argument-notes/*.md")
    parser.add_argument("--apply", action="store_true", help="Write changes to permanent notes. Default is dry-run.")
    parser.add_argument(
        "--prune-disallowed",
        action="store_true",
        help="Drop non `supports/next` lines in `## Links` and remove `supports` targets that are not argument notes.",
    )
    args = parser.parse_args()

    argument_paths = collect_targets(args.targets)
    if not argument_paths:
        print("No argument-note targets found.", file=sys.stderr)
        return 1

    all_chains = load_all_chains()
    all_argument_ids = {chain.arg_id for chain in all_chains}
    global_next_index = build_global_next_index(all_chains)

    changes = 0
    warnings = 0

    for arg_path in argument_paths:
        chain = parse_argument(arg_path)
        print(f"\nARG {arg_path.relative_to(ROOT)}")
        print(f"  id: {chain.arg_id}")
        print(f"  title: {chain.arg_title}")

        if chain.warnings:
            warnings += len(chain.warnings)
            for warning in chain.warnings:
                print(f"  warning: {warning}")

        for note_id in sorted(chain.cited_ids):
            note_path = PERM_DIR / f"{note_id}.md"
            if not note_path.exists():
                warnings += 1
                print(f"  warning: missing permanent note {note_id}")
                continue
            expected_nexts = chain.next_map.get(note_id, set())
            if args.apply:
                changed, messages = sync_note_links(
                    note_path,
                    chain,
                    expected_nexts,
                    global_next_index.get(note_id, set()),
                    all_argument_ids,
                    args.prune_disallowed,
                )
                if changed:
                    changes += 1
                for message in messages:
                    print(f"  {message}")
            else:
                print(
                    f"  would sync {note_id}: supports={chain.arg_id}, next={sorted(expected_nexts)}"
                )

    mode = "apply" if args.apply else "dry-run"
    print(f"\nDone ({mode}). changed={changes}, warnings={warnings}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
