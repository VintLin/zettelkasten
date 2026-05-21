#!/usr/bin/env python3
from __future__ import annotations

import argparse
from collections import Counter
import re
import sys
from pathlib import Path
from typing import Dict, Iterable, List, Set, Tuple

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from sync_argument_links import (  # noqa: E402
    ARG_DIR,
    LINK_LINE_RE,
    PERM_DIR,
    ROOT,
    build_global_next_index,
    build_global_next_source_index,
    collect_targets,
    extract_frontmatter_value,
    load_all_chains,
    parse_argument,
    read_text,
)

STRUCT_DIR = ROOT / "wiki" / "structure-notes"
REF_DIR = ROOT / "wiki" / "reference-notes"
WIKILINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]")
REFERENCE_NOTE_LINK_RE = re.compile(r"^\s*-\s+\[\[([^\]|]+)(?:\|([^\]]+))?\]\](.*)$")


def parse_note_link_targets(note_path: Path) -> Tuple[Set[str], Set[str]]:
    text = read_text(note_path)
    supports: Set[str] = set()
    nexts: Set[str] = set()
    for line in text.splitlines():
        m = LINK_LINE_RE.match(line)
        if not m:
            continue
        kind, target_id = m.group(1), m.group(2)
        if kind == "supports":
            supports.add(target_id)
        else:
            nexts.add(target_id)
    return supports, nexts


def parse_note_link_counts(note_path: Path) -> Tuple[Dict[str, int], Dict[str, int]]:
    text = read_text(note_path)
    support_counts: Dict[str, int] = {}
    next_counts: Dict[str, int] = {}
    for line in text.splitlines():
        m = LINK_LINE_RE.match(line)
        if not m:
            continue
        kind, target_id = m.group(1), m.group(2)
        if kind == "supports":
            support_counts[target_id] = support_counts.get(target_id, 0) + 1
        else:
            next_counts[target_id] = next_counts.get(target_id, 0) + 1
    return support_counts, next_counts


def extract_links_block_lines(note_path: Path) -> List[str]:
    text = read_text(note_path)
    lines = text.splitlines()
    start = -1
    end = len(lines)
    for i, line in enumerate(lines):
        if line.strip() == "## Links":
            start = i
            break
    if start == -1:
        return []
    for i in range(start + 1, len(lines)):
        if lines[i].startswith("## "):
            end = i
            break
    return lines[start + 1 : end]


def find_disallowed_link_lines(note_path: Path, all_argument_ids: Set[str]) -> List[str]:
    disallowed: List[str] = []
    for line in extract_links_block_lines(note_path):
        stripped = line.strip()
        if not stripped:
            continue
        m = LINK_LINE_RE.match(line)
        if not m:
            disallowed.append(stripped)
            continue
        kind, target_id = m.group(1), m.group(2)
        if kind == "supports" and target_id not in all_argument_ids:
            disallowed.append(stripped)
    return disallowed


def load_all_argument_ids() -> Set[str]:
    ids: Set[str] = set()
    for path in ARG_DIR.glob("*.md"):
        text = read_text(path)
        ids.add(extract_frontmatter_value(text, "id") or path.stem)
    return ids


def load_all_note_ids() -> Set[str]:
    ids: Set[str] = set()
    for path in (ROOT / "wiki").rglob("*.md"):
        ids.add(path.stem)
    return ids


def load_ids(directory: Path) -> Set[str]:
    ids: Set[str] = set()
    for path in directory.glob("*.md"):
        text = read_text(path)
        ids.add(extract_frontmatter_value(text, "id") or path.stem)
    return ids


def collect_structure_reachable_permanent_ids(
    argument_ids: Set[str],
    permanent_ids: Set[str],
) -> Set[str]:
    argument_to_permanent: Dict[str, Set[str]] = {}

    for path in sorted(ARG_DIR.glob("*.md")):
        text = read_text(path)
        arg_id = extract_frontmatter_value(text, "id") or path.stem
        linked_permanents: Set[str] = set()
        for target in iter_wikilink_targets(strip_frontmatter(text)):
            if target in permanent_ids:
                linked_permanents.add(target)
        argument_to_permanent[arg_id] = linked_permanents

    reachable: Set[str] = set()
    for path in sorted(STRUCT_DIR.glob("*.md")):
        text = read_text(path)
        for target in iter_wikilink_targets(strip_frontmatter(text)):
            if target not in argument_ids:
                continue
            reachable.update(argument_to_permanent.get(target, set()))

    return reachable


def load_wikilink_targets() -> Tuple[Set[str], Set[str]]:
    bare_targets: Set[str] = set()
    path_targets: Set[str] = set()
    scan_dirs = [ROOT / "wiki", ROOT / "archive", ROOT / "raw", ROOT / "outputs"]

    for directory in scan_dirs:
        if not directory.exists():
            continue
        for path in directory.rglob("*"):
            if not path.is_file():
                continue
            rel_parts = path.relative_to(ROOT).parts
            if any(part.startswith(".") for part in rel_parts):
                continue
            rel = path.relative_to(ROOT).as_posix()
            bare_targets.add(path.name)
            path_targets.add(rel)
            if path.suffix == ".md":
                bare_targets.add(path.stem)
                rel = rel[:-3]
            path_targets.add(rel)
    return bare_targets, path_targets


def wikilink_target_exists(target: str, bare_targets: Set[str], path_targets: Set[str]) -> bool:
    note_target = target.split("#", 1)[0].strip()
    if not note_target:
        return False
    if "/" in note_target:
        normalized = note_target[:-3] if note_target.endswith(".md") else note_target
        return normalized in path_targets
    return note_target in bare_targets


def audit_broken_wikilinks(
    note_path: Path,
    bare_targets: Set[str],
    path_targets: Set[str],
) -> List[str]:
    issues: List[str] = []
    text = read_text(note_path)
    for lineno, line in enumerate(text.splitlines(), start=1):
        for m in WIKILINK_RE.finditer(line):
            target = m.group(1)
            if wikilink_target_exists(target, bare_targets, path_targets):
                continue
            issues.append(
                f"{note_path.relative_to(ROOT)}:{lineno} [broken_wikilink] -> [[{target}]]"
            )
    return issues


def strip_frontmatter(text: str) -> str:
    if not text.startswith("---\n"):
        return text
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        return text
    return parts[2]


def extract_section(text: str, heading: str) -> str:
    body = strip_frontmatter(text)
    lines = body.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.strip() == heading:
            start = i + 1
            break
    if start is None:
        return ""
    end = len(lines)
    for i in range(start, len(lines)):
        if lines[i].startswith("## "):
            end = i
            break
    return "\n".join(lines[start:end]).strip()


def iter_wikilink_targets(text: str) -> Iterable[str]:
    for m in WIKILINK_RE.finditer(text):
        yield m.group(1)


def audit_structure_note(
    note_path: Path,
    argument_ids: Set[str],
) -> List[str]:
    text = read_text(note_path)
    issues: List[str] = []
    if "## Summary" not in text:
        issues.append("[missing_summary]")
    if "## Note" not in text:
        issues.append("[missing_note]")
    if "Related entrances" in text:
        issues.append("[disallowed_related_entrances_heading]")

    body = strip_frontmatter(text)
    for target in sorted(set(iter_wikilink_targets(body))):
        if target.startswith("archive/") or target.startswith("outputs/") or target.startswith(".cache/"):
            issues.append(f"[disallowed_structure_link] -> {target}")
            continue
        if target not in argument_ids:
            issues.append(f"[disallowed_structure_link] -> {target}")
    return issues


def extract_argument_citations(arg_path: Path) -> Set[str]:
    chain = parse_argument(arg_path)
    return chain.cited_ids


def audit_argument_note(
    arg_path: Path,
    structure_ids: Set[str],
    permanent_ids: Set[str],
) -> List[str]:
    text = read_text(arg_path)
    issues: List[str] = []
    if "## Summary" not in text:
        issues.append("[missing_summary]")
    if "## Note" not in text:
        issues.append("[missing_note]")
    if "### 论点 / 问题" not in text:
        issues.append("[missing_question_section]")
    if "### 论据" not in text:
        issues.append("[missing_evidence_section]")

    summary = extract_section(text, "## Summary")
    if not summary:
        issues.append("[empty_summary]")
    elif len(summary) < 30:
        issues.append("[summary_too_short]")

    body_before_links = strip_frontmatter(text).split("## Links", 1)[0]
    cited_ids = extract_argument_citations(arg_path)
    for target in sorted(set(iter_wikilink_targets(body_before_links))):
        if target not in cited_ids and target in structure_ids:
            issues.append(f"[argument_body_links_structure] -> {target}")
        elif target not in cited_ids and target not in permanent_ids:
            issues.append(f"[argument_body_non_permanent_link] -> {target}")

    link_lines = extract_links_block_lines(arg_path)
    for line in link_lines:
        stripped = line.strip()
        if not stripped:
            continue
        m = LINK_LINE_RE.match(line)
        if not m:
            issues.append(f"[disallowed_argument_link_line] {stripped}")
            continue
        kind, target_id = m.group(1), m.group(2)
        if kind != "supports":
            issues.append(f"[disallowed_argument_link_kind] {stripped}")
            continue
        if target_id not in structure_ids:
            issues.append(f"[argument_supports_non_structure] -> {target_id}")
    return issues


def audit_permanent_note(
    note_path: Path,
    argument_ids: Set[str],
    permanent_ids: Set[str],
) -> List[str]:
    text = read_text(note_path)
    issues: List[str] = []
    if "## Summary" not in text:
        issues.append("[missing_summary]")
    if "## Note" not in text:
        issues.append("[missing_note]")

    supports, nexts = parse_note_link_targets(note_path)
    if not supports:
        issues.append("[orphan_permanent_no_support]")
    for target in sorted(supports):
        if target not in argument_ids:
            issues.append(f"[permanent_supports_non_argument] -> {target}")
    for target in sorted(nexts):
        if target not in permanent_ids:
            issues.append(f"[permanent_next_non_permanent] -> {target}")

    references = extract_section(text, "## References")
    if not references:
        issues.append("[missing_references]")
        return issues

    allowed_prefixes = ("- from [[", "- references [[", "- url: ")
    for raw_line in references.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if not line.startswith("- "):
            issues.append(f"[bad_reference_line] {line}")
            continue
        if not line.startswith(allowed_prefixes):
            issues.append(f"[bad_reference_line] {line}")
            continue
        if line.startswith("- from [["):
            m = WIKILINK_RE.search(line)
            if not m:
                issues.append(f"[bad_from_format] {line}")
                continue
            target = m.group(1)
            if "/" in target:
                issues.append(f"[from_uses_path_not_filename] {line}")
    return issues


def audit_reference_note(
    note_path: Path,
    permanent_ids: Set[str],
) -> List[str]:
    text = read_text(note_path)
    issues: List[str] = []
    if "## Summary" not in text:
        issues.append("[missing_summary]")
    if "## Note" not in text:
        issues.append("[missing_note]")

    for raw_line in extract_links_block_lines(note_path):
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("- supports ") or line.startswith("- next "):
            issues.append(f"[reference_uses_structural_link_kind] {line}")
            continue
        if line.startswith("- related_pattern ") or line.startswith("- related "):
            issues.append(f"[reference_uses_pseudo_link] {line}")
            continue
        m = REFERENCE_NOTE_LINK_RE.match(raw_line)
        if not m:
            issues.append(f"[bad_reference_note_link_line] {line}")
            continue
        target = m.group(1).strip()
        if target not in permanent_ids:
            issues.append(f"[reference_link_non_permanent] -> {target}")

    references = extract_section(text, "## References")
    if not references:
        issues.append("[missing_references]")
        return issues

    allowed_prefixes = ("- from [[", "- references [[", "- url: ")
    for raw_line in references.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if not line.startswith("- "):
            issues.append(f"[bad_reference_line] {line}")
            continue
        if not line.startswith(allowed_prefixes):
            issues.append(f"[bad_reference_line] {line}")
            continue
        if line.startswith("- from [["):
            m = WIKILINK_RE.search(line)
            if not m:
                issues.append(f"[bad_from_format] {line}")
                continue
            target = m.group(1)
            if "/" in target:
                issues.append(f"[from_uses_path_not_filename] {line}")
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit permanent-note supports/next links against argument notes.")
    parser.add_argument("targets", nargs="*", help="Argument-note files, directories, or globs. Default: wiki/argument-notes/*.md")
    args = parser.parse_args()

    argument_paths = collect_targets(args.targets)
    if not argument_paths:
        print("No argument-note targets found.", file=sys.stderr)
        return 1

    all_argument_ids = load_all_argument_ids()
    all_structure_ids = load_ids(STRUCT_DIR)
    all_reference_ids = load_ids(REF_DIR)
    all_permanent_ids = load_ids(PERM_DIR)
    all_note_ids = load_all_note_ids()
    structure_reachable_permanent_ids = collect_structure_reachable_permanent_ids(
        all_argument_ids,
        all_permanent_ids,
    )
    wikilink_bare_targets, wikilink_path_targets = load_wikilink_targets()
    all_chains = load_all_chains()
    global_next_index = build_global_next_index(all_chains)
    global_next_source_index = build_global_next_source_index(all_chains)
    issue_count = 0
    checked_notes = 0
    issue_types: Counter[str] = Counter()

    def count_issue(issue: str) -> None:
        m = re.search(r"\[([^\]]+)\]", issue)
        if m:
            issue_types[m.group(1)] += 1

    for arg_path in argument_paths:
        chain = parse_argument(arg_path)
        local_issues: List[str] = []

        for warning in chain.warnings:
            issue = f"[argument_warning] {warning}"
            local_issues.append(issue)
            count_issue(issue)

        for note_id in sorted(chain.cited_ids):
            note_path = PERM_DIR / f"{note_id}.md"
            if not note_path.exists():
                local_issues.append(f"[missing_note] {note_id}")
                count_issue(local_issues[-1])
                continue

            checked_notes += 1
            supports, nexts = parse_note_link_targets(note_path)
            support_counts, next_counts = parse_note_link_counts(note_path)
            expected_nexts = chain.next_map.get(note_id, set())
            relevant_actual_nexts = {target for target in nexts if target in chain.cited_ids}

            if chain.arg_id not in supports:
                issue = f"[missing_support] {note_id} -> [[{chain.arg_id}|{chain.arg_title}]]"
                local_issues.append(issue)
                count_issue(issue)

            missing_nexts = sorted(expected_nexts - relevant_actual_nexts)
            if missing_nexts:
                issue = f"[missing_next] {note_id} -> {missing_nexts}"
                local_issues.append(issue)
                count_issue(issue)

            globally_valid_nexts = global_next_index.get(note_id, set())
            unexpected_nexts = sorted(
                target for target in relevant_actual_nexts - expected_nexts if target not in globally_valid_nexts
            )
            if unexpected_nexts:
                issue = f"[unexpected_next] {note_id} -> {unexpected_nexts}"
                local_issues.append(issue)
                count_issue(issue)

            duplicate_supports = sorted(target for target, count in support_counts.items() if count > 1)
            if duplicate_supports:
                issue = f"[duplicate_support] {note_id} -> {duplicate_supports}"
                local_issues.append(issue)
                count_issue(issue)

            duplicate_nexts = sorted(target for target, count in next_counts.items() if count > 1)
            if duplicate_nexts:
                issue = f"[duplicate_next] {note_id} -> {duplicate_nexts}"
                local_issues.append(issue)
                count_issue(issue)

            disallowed_lines = find_disallowed_link_lines(note_path, all_argument_ids)
            if disallowed_lines:
                issue = f"[disallowed_link_line] {note_id} -> {disallowed_lines}"
                local_issues.append(issue)
                count_issue(issue)

        if local_issues:
            issue_count += len(local_issues)
            print(f"\nARG {arg_path.relative_to(ARG_DIR.parent.parent.parent)}")
            for issue in local_issues:
                print(f"  {issue}")

    stale_support_issues: List[str] = []
    for note_path in sorted(PERM_DIR.glob("*.md")):
        supports, _ = parse_note_link_targets(note_path)
        stale = sorted(
            target
            for target in supports
            if target.startswith("2026") and target not in all_argument_ids and target not in all_note_ids
        )
        if stale:
            stale_support_issues.append(
                f"{note_path.relative_to(PERM_DIR.parent.parent)} -> stale supports {stale}"
            )

    if stale_support_issues:
        issue_count += len(stale_support_issues)
        print("\nGLOBAL")
        for issue in stale_support_issues:
            print(f"  [stale_support] {issue}")
            issue_types["stale_support"] += 1

    suspicious_multi_next_issues: List[str] = []
    for note_id, next_ids in sorted(global_next_index.items()):
        if len(next_ids) <= 1:
            continue
        source_args = sorted(global_next_source_index.get(note_id, set()))
        if len(source_args) <= 1:
            continue
        suspicious_multi_next_issues.append(
            f"{note_id} -> next {sorted(next_ids)} across arguments {source_args}"
        )

    if suspicious_multi_next_issues:
        print("\nGLOBAL")
        for issue in suspicious_multi_next_issues:
            print(f"  [suspicious_multi_next] {issue}")
            issue_types["suspicious_multi_next"] += 1

    structure_issues: List[str] = []
    for path in sorted(STRUCT_DIR.glob("*.md")):
        issues = audit_structure_note(path, all_argument_ids)
        for issue in issues:
            structure_issues.append(f"{path.relative_to(ROOT)} {issue}")

    if structure_issues:
        issue_count += len(structure_issues)
        print("\nSTRUCTURE")
        for issue in structure_issues:
            print(f"  {issue}")
            count_issue(issue)

    argument_logic_issues: List[str] = []
    for path in sorted(ARG_DIR.glob("*.md")):
        issues = audit_argument_note(path, all_structure_ids, all_permanent_ids)
        for issue in issues:
            argument_logic_issues.append(f"{path.relative_to(ROOT)} {issue}")

    if argument_logic_issues:
        issue_count += len(argument_logic_issues)
        print("\nARGUMENT")
        for issue in argument_logic_issues:
            print(f"  {issue}")
            count_issue(issue)

    permanent_logic_issues: List[str] = []
    for path in sorted(PERM_DIR.glob("*.md")):
        issues = audit_permanent_note(path, all_argument_ids, all_permanent_ids)
        if path.stem not in structure_reachable_permanent_ids:
            issues.append("[permanent_unreachable_from_structure]")
        for issue in issues:
            permanent_logic_issues.append(f"{path.relative_to(ROOT)} {issue}")

    if permanent_logic_issues:
        issue_count += len(permanent_logic_issues)
        print("\nPERMANENT")
        for issue in permanent_logic_issues:
            print(f"  {issue}")
            count_issue(issue)

    reference_logic_issues: List[str] = []
    for path in sorted(REF_DIR.glob("*.md")):
        issues = audit_reference_note(path, all_permanent_ids)
        for issue in issues:
            reference_logic_issues.append(f"{path.relative_to(ROOT)} {issue}")

    if reference_logic_issues:
        issue_count += len(reference_logic_issues)
        print("\nREFERENCE")
        for issue in reference_logic_issues:
            print(f"  {issue}")
            count_issue(issue)

    broken_wikilink_issues: List[str] = []
    for path in sorted((ROOT / "wiki").rglob("*.md")):
        broken_wikilink_issues.extend(
            audit_broken_wikilinks(path, wikilink_bare_targets, wikilink_path_targets)
        )

    if broken_wikilink_issues:
        issue_count += len(broken_wikilink_issues)
        print("\nWIKILINK")
        for issue in broken_wikilink_issues:
            print(f"  {issue}")
            count_issue(issue)

    if issue_types:
        print("\nSUMMARY")
        for issue_type, count in issue_types.most_common():
            print(f"  {issue_type}: {count}")

    print(f"\nDone. checked_notes={checked_notes}, issues={issue_count}")
    return 0 if issue_count == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
