#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import List, Optional, Tuple

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from sync_argument_links import ARG_DIR, PERM_DIR, ROOT, read_text  # noqa: E402

REF_DIR = ROOT / "wiki" / "reference-notes"
STRUCT_DIR = ROOT / "wiki" / "structure-notes"

WIKILINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]")
URL_RE = re.compile(r"https?://\S+")
CODE_PATH_RE = re.compile(r"`([^`]+?\.(?:md|pdf|png|jpg|jpeg|webp))`")

FROM_PREFIXES = (
    "来源文件：",
    "原始材料：",
    "参考材料：",
    "补充来源：",
    "补充来源文件：",
    "分析输入：",
    "相关材料：",
)
REFERENCE_PREFIXES = (
    "对应文献笔记：",
    "对应参考笔记：",
    "参考文献：",
)
URL_PREFIXES = (
    "来源链接：",
    "原始参考链接：",
    "图表链接（远程，未落地本地资产）：",
    "补充线索：",
    "外部来源：",
    "参考链接：",
)
DROP_PREFIXES = (
    "无对应参考笔记：",
    "原始材料中的图片：",
    "参考图片：",
    "原始摘抄主题：",
)
PSEUDO_LINK_PREFIXES = ("- related_pattern ", "- related ")


def load_ids(directory: Path) -> set[str]:
    return {path.stem for path in directory.glob("*.md")}


def split_sections(lines: List[str]) -> Tuple[int, int]:
    start = -1
    end = len(lines)
    for i, line in enumerate(lines):
        if line.strip() == "## References":
            start = i
            break
    if start == -1:
        return -1, -1
    for i in range(start + 1, len(lines)):
        if lines[i].startswith("## "):
            end = i
            break
    return start, end


def basename_link(target: str, label: Optional[str]) -> Tuple[str, str]:
    cleaned = target.strip()
    if "/" in cleaned:
        cleaned = Path(cleaned).name
    if cleaned.endswith(".md"):
        cleaned = cleaned[:-3]
    link_label = (label or cleaned).strip()
    if link_label.endswith(".md"):
        link_label = link_label[:-3]
    return cleaned, link_label


def normalize_wikilink_line(line: str) -> Optional[str]:
    stripped = line.strip()
    for prefix in DROP_PREFIXES:
        if stripped.startswith(f"- {prefix}"):
            return ""
    numbered_from = re.match(r"^- (来源文件|补充来源文件)\s+\d+：", stripped)
    if numbered_from:
        m = WIKILINK_RE.search(stripped)
        if m:
            target, label = basename_link(m.group(1), m.group(2))
            return f"- from [[{target}|{label}]]"
        code = CODE_PATH_RE.search(stripped)
        if code:
            basename = Path(code.group(1)).stem
            return f"- from [[{basename}|{basename}]]"
    for prefix in FROM_PREFIXES:
        marker = f"- {prefix}"
        if stripped.startswith(marker):
            m = WIKILINK_RE.search(stripped)
            if m:
                target, label = basename_link(m.group(1), m.group(2))
                return f"- from [[{target}|{label}]]"
            code = CODE_PATH_RE.search(stripped)
            if code:
                basename = Path(code.group(1)).stem
                return f"- from [[{basename}|{basename}]]"
    for prefix in REFERENCE_PREFIXES:
        marker = f"- {prefix}"
        if stripped.startswith(marker):
            m = WIKILINK_RE.search(stripped)
            if m:
                target = m.group(1).strip()
                label = (m.group(2) or target).strip()
                return f"- references [[{target}|{label}]]"
    for prefix in URL_PREFIXES:
        marker = f"- {prefix}"
        if stripped.startswith(marker):
            m = URL_RE.search(stripped)
            if m:
                return f"- url: {m.group(0)}"
            return ""
    if stripped.startswith("- 外部参考：") or stripped.startswith("- 参考来源：") or stripped.startswith("- 提及来源："):
        m = URL_RE.search(stripped)
        if m:
            return f"- url: {m.group(0)}"
        return ""
    if stripped.startswith("- 参考来源见原始材料内附外部链接。"):
        return ""
    if stripped.startswith("- ") and WIKILINK_RE.fullmatch(stripped[2:]):
        m = WIKILINK_RE.fullmatch(stripped[2:])
        if m:
            target = m.group(1).strip()
            label = (m.group(2) or target).strip()
            return f"- references [[{target}|{label}]]"
    if stripped.startswith("- ") and "<http" in stripped:
        m = URL_RE.search(stripped)
        if m:
            return f"- url: {m.group(0)}"
    if stripped.startswith("- url: "):
        return stripped
    if stripped.startswith("- from [[") or stripped.startswith("- references [["):
        m = WIKILINK_RE.search(stripped)
        if not m:
            return stripped
        target, label = basename_link(m.group(1), m.group(2))
        if stripped.startswith("- from [["):
            return f"- from [[{target}|{label}]]"
        return f"- references [[{m.group(1).strip()}|{(m.group(2) or m.group(1)).strip()}]]"
    return None


def normalize_note(path: Path, apply: bool) -> bool:
    text = read_text(path)
    lines = text.splitlines()
    start, end = split_sections(lines)
    if start == -1:
        return False

    old_block = lines[start + 1 : end]
    new_block: List[str] = []
    changed = False

    for line in old_block:
        stripped = line.strip()
        if not stripped:
            if new_block and new_block[-1] != "":
                new_block.append("")
            continue
        normalized = normalize_wikilink_line(line)
        if normalized is not None:
            if normalized:
                new_block.append(normalized)
            if normalized != stripped:
                changed = True
            continue
        new_block.append(stripped)

    while new_block and new_block[-1] == "":
        new_block.pop()

    replacement = ["## References"] + new_block
    if end < len(lines) and lines[end].strip():
        replacement.append("")

    if lines[start:end] != replacement:
        changed = True
        if apply:
            lines[start:end] = replacement
            new_text = "\n".join(lines) + ("\n" if text.endswith("\n") else "")
            path.write_text(new_text, encoding="utf-8")

    return changed


def split_section(lines: List[str], heading: str) -> Tuple[int, int]:
    start = -1
    end = len(lines)
    for i, line in enumerate(lines):
        if line.strip() == heading:
            start = i
            break
    if start == -1:
        return -1, -1
    for i in range(start + 1, len(lines)):
        if lines[i].startswith("## "):
            end = i
            break
    return start, end


def normalize_reference_link_line(
    line: str,
    permanent_ids: set[str],
    reference_ids: set[str],
    argument_ids: set[str],
    structure_ids: set[str],
) -> Tuple[Optional[str], List[str]]:
    stripped = line.strip()
    if not stripped:
        return "", []

    for prefix in PSEUDO_LINK_PREFIXES:
        if stripped.startswith(prefix):
            m = WIKILINK_RE.search(stripped)
            if not m:
                return "", []
            target = m.group(1).strip()
            label = (m.group(2) or target).strip()
            suffix = stripped.split("]]", 1)[1]
            if target in permanent_ids:
                return f"- [[{target}|{label}]]{suffix}", []
            if target in reference_ids:
                return "", [f"- references [[{target}|{label}]]"]
            if target in argument_ids or target in structure_ids:
                return "", []
            return stripped, []

    if stripped.startswith("- supports ") or stripped.startswith("- next "):
        return "", []

    if stripped.startswith("- [["):
        m = WIKILINK_RE.search(stripped)
        if not m:
            return stripped, []
        target = m.group(1).strip()
        if target in permanent_ids:
            return stripped, []
        if target in reference_ids:
            label = (m.group(2) or target).strip()
            return "", [f"- references [[{target}|{label}]]"]
        if target in argument_ids or target in structure_ids:
            return "", []
    return stripped, []


def normalize_reference_note(path: Path, apply: bool) -> bool:
    text = read_text(path)
    lines = text.splitlines()
    refs_start, refs_end = split_section(lines, "## References")
    links_start, links_end = split_section(lines, "## Links")

    permanent_ids = load_ids(PERM_DIR)
    reference_ids = load_ids(REF_DIR)
    argument_ids = load_ids(ARG_DIR)
    structure_ids = load_ids(STRUCT_DIR)

    changed = False
    migrated_reference_links: List[str] = []
    migrated_permanent_links: List[str] = []

    if links_start != -1:
        old_links = lines[links_start + 1 : links_end]
        new_links: List[str] = []
        for line in old_links:
            normalized, migrated_refs = normalize_reference_link_line(
                line,
                permanent_ids,
                reference_ids,
                argument_ids,
                structure_ids,
            )
            migrated_reference_links.extend(migrated_refs)
            if normalized == "":
                continue
            new_links.append(normalized)
            if normalized != line.strip():
                changed = True
        replacement = ["## Links"] + new_links
        if links_end < len(lines) and lines[links_end].strip():
            replacement.append("")
        if lines[links_start:links_end] != replacement:
            changed = True
            if apply:
                lines[links_start:links_end] = replacement
                delta = len(replacement) - (links_end - links_start)
                refs_start += delta if refs_start > links_start else 0
                refs_end += delta if refs_end > links_start else 0

    if refs_start != -1:
        old_refs = lines[refs_start + 1 : refs_end]
        new_refs: List[str] = []
        for line in old_refs:
            stripped = line.strip()
            if not stripped:
                if new_refs and new_refs[-1] != "":
                    new_refs.append("")
                continue
            normalized = normalize_wikilink_line(line)
            if normalized is not None:
                if normalized:
                    new_refs.append(normalized)
                if normalized != stripped:
                    changed = True
                continue
            if stripped.startswith("- 对应永久笔记："):
                m = WIKILINK_RE.search(stripped)
                if m:
                    target = m.group(1).strip()
                    label = (m.group(2) or target).strip()
                    if target in permanent_ids:
                        migrated_permanent_links.append(f"- [[{target}|{label}]]")
                        changed = True
                        continue
            if stripped.startswith("- 对应参考笔记："):
                m = WIKILINK_RE.search(stripped)
                if m:
                    target = m.group(1).strip()
                    label = (m.group(2) or target).strip()
                    new_refs.append(f"- references [[{target}|{label}]]")
                    changed = True
                    continue
            new_refs.append(stripped)

        while new_refs and new_refs[-1] == "":
            new_refs.pop()

        existing_ref_lines = set(new_refs)
        for migrated in migrated_reference_links:
            if migrated not in existing_ref_lines:
                new_refs.append(migrated)
                existing_ref_lines.add(migrated)
                changed = True

        replacement = ["## References"] + new_refs
        if refs_end < len(lines) and lines[refs_end].strip():
            replacement.append("")

        if lines[refs_start:refs_end] != replacement:
            changed = True
            if apply:
                lines[refs_start:refs_end] = replacement

    if changed and apply:
        if migrated_permanent_links:
            links_start, links_end = split_section(lines, "## Links")
            if links_start == -1:
                insert_at = len(lines)
                refs_start, _ = split_section(lines, "## References")
                if refs_start != -1:
                    insert_at = refs_start
                lines[insert_at:insert_at] = ["## Links", ""]
                links_start, links_end = split_section(lines, "## Links")
            existing_links = lines[links_start + 1 : links_end]
            seen = {line.strip() for line in existing_links if line.strip()}
            additions = [line for line in migrated_permanent_links if line not in seen]
            if additions:
                new_block = ["## Links"] + [line.strip() for line in existing_links if line.strip()] + additions
                if links_end < len(lines) and lines[links_end].strip():
                    new_block.append("")
                lines[links_start:links_end] = new_block
        new_text = "\n".join(lines) + ("\n" if text.endswith("\n") else "")
        path.write_text(new_text, encoding="utf-8")

    return changed


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Normalize permanent-note and reference-note structural residue into canonical `Links` / `References` forms."
    )
    parser.add_argument("--apply", action="store_true", help="Write changes. Default is dry-run.")
    args = parser.parse_args()

    changed = 0
    for path in sorted(PERM_DIR.glob("*.md")):
        if normalize_note(path, apply=args.apply):
            changed += 1
            prefix = "normalized" if args.apply else "would normalize"
            print(f"{prefix} {path.relative_to(ROOT)}")
    for path in sorted(REF_DIR.glob("*.md")):
        if normalize_reference_note(path, apply=args.apply):
            changed += 1
            prefix = "normalized" if args.apply else "would normalize"
            print(f"{prefix} {path.relative_to(ROOT)}")

    mode = "apply" if args.apply else "dry-run"
    print(f"\nDone ({mode}). changed={changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
