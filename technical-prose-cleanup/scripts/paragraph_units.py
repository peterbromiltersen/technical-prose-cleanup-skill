#!/usr/bin/env python3
"""Extract paragraph-scale cleanup units and save progress markers."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


MARKER_NAME = ".technical-prose-cleanup-progress.json"

PROTECTED_ENVIRONMENTS = {
    "align",
    "align*",
    "alignat",
    "alignat*",
    "assumption",
    "claim",
    "conjecture",
    "corollary",
    "definition",
    "equation",
    "equation*",
    "example",
    "fact",
    "gather",
    "gather*",
    "lemma",
    "multline",
    "multline*",
    "notation",
    "observation",
    "proof",
    "proposition",
    "quote",
    "quotation",
    "remark",
    "theorem",
}


@dataclass
class Unit:
    number: int
    line: int
    kind: str
    text: str


def strip_tex_comment(line: str) -> str:
    escaped = False
    for index, char in enumerate(line):
        if char == "\\" and not escaped:
            escaped = True
            continue
        if char == "%" and not escaped:
            return line[:index]
        escaped = False
    return line


def add_unit(units: list[Unit], line: int, kind: str, text: str) -> None:
    cleaned = text.strip()
    if cleaned:
        units.append(Unit(len(units) + 1, line, kind, cleaned))


def begin_environment(line: str) -> str | None:
    match = re.match(r"\\begin\{([^}]+)\}", line)
    if match and match.group(1) in PROTECTED_ENVIRONMENTS:
        return match.group(1)
    return None


def end_environment(line: str, env: str) -> bool:
    return bool(re.match(rf"\\end\{{{re.escape(env)}\}}", line))


def heading_kind(line: str) -> str | None:
    match = re.match(r"\\(part|chapter|section|subsection|subsubsection|paragraph)\*?\{", line)
    return match.group(1) if match else None


def extract_tex_units(path: Path) -> list[Unit]:
    lines = path.read_text(encoding="utf-8").splitlines()
    units: list[Unit] = []
    paragraph: list[str] = []
    paragraph_line = 1
    in_document = not any(r"\begin{document}" in line for line in lines)
    in_abstract_command = False
    in_block: tuple[str, int, list[str]] | None = None

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            add_unit(units, paragraph_line, "paragraph", "\n".join(paragraph))
            paragraph = []

    for line_number, raw_line in enumerate(lines, start=1):
        line = strip_tex_comment(raw_line).strip()

        if line == r"\begin{document}":
            in_document = True
            continue
        if not in_document:
            continue
        if line in {r"\maketitle", r"\end{document}"}:
            flush_paragraph()
            continue

        if in_block is not None:
            env, start_line, block = in_block
            block.append(raw_line)
            if end_environment(line, env):
                add_unit(units, start_line, "protected-block", "\n".join(block))
                in_block = None
            continue

        if line == r"\abstract{":
            flush_paragraph()
            paragraph_line = line_number + 1
            in_abstract_command = True
            continue
        if in_abstract_command and line == "}":
            flush_paragraph()
            paragraph_line = line_number + 1
            in_abstract_command = False
            continue

        env = begin_environment(line)
        if env:
            flush_paragraph()
            block = [raw_line]
            if end_environment(line, env):
                add_unit(units, line_number, "protected-block", "\n".join(block))
            else:
                in_block = (env, line_number, block)
            continue

        kind = heading_kind(line)
        if kind:
            flush_paragraph()
            add_unit(units, line_number, kind, raw_line)
            continue

        if re.match(r"\\(?:label|bibliographystyle|bibliography|nocite)\b", line):
            flush_paragraph()
            add_unit(units, line_number, "command", raw_line)
            continue

        if not line:
            flush_paragraph()
            paragraph_line = line_number + 1
            continue

        if not paragraph:
            paragraph_line = line_number
        paragraph.append(raw_line)

    flush_paragraph()
    if in_block is not None:
        _env, start_line, block = in_block
        add_unit(units, start_line, "protected-block", "\n".join(block))
    return units


def extract_plain_units(path: Path) -> list[Unit]:
    units: list[Unit] = []
    paragraph: list[str] = []
    paragraph_line = 1
    in_fence = False
    fence: list[str] = []
    fence_line = 1

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            add_unit(units, paragraph_line, "paragraph", "\n".join(paragraph))
            paragraph = []

    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.strip()
        if in_fence:
            fence.append(raw_line)
            if line.startswith("```") or line.startswith("~~~"):
                add_unit(units, fence_line, "protected-block", "\n".join(fence))
                in_fence = False
            continue
        if line.startswith("```") or line.startswith("~~~"):
            flush_paragraph()
            fence = [raw_line]
            fence_line = line_number
            in_fence = True
            continue
        if re.match(r"#{1,6}\s+\S", line):
            flush_paragraph()
            add_unit(units, line_number, "heading", raw_line)
            continue
        if not line:
            flush_paragraph()
            paragraph_line = line_number + 1
            continue
        if not paragraph:
            paragraph_line = line_number
        paragraph.append(raw_line)

    flush_paragraph()
    if in_fence:
        add_unit(units, fence_line, "protected-block", "\n".join(fence))
    return units


def extract_units(path: Path) -> list[Unit]:
    if path.suffix.lower() == ".tex":
        return extract_tex_units(path)
    return extract_plain_units(path)


def marker_path(manuscript: Path) -> Path:
    return manuscript.parent / MARKER_NAME


def save_marker(manuscript: Path, units: list[Unit], next_unit: int, note: str) -> None:
    target = next((unit for unit in units if unit.number == next_unit), None)
    payload = {
        "manuscript": str(manuscript),
        "next_unit": next_unit,
        "next_line": target.line if target else None,
        "saved_at": datetime.now(timezone.utc).isoformat(),
        "note": note,
    }
    marker_path(manuscript).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("manuscript", type=Path)
    parser.add_argument("--start", type=int, default=1)
    parser.add_argument("--count", type=int, default=20)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--save-marker", type=int)
    parser.add_argument("--note", default="")
    args = parser.parse_args()

    manuscript = args.manuscript.resolve()
    units = extract_units(manuscript)

    if args.save_marker is not None:
        save_marker(manuscript, units, args.save_marker, args.note)
        print(f"Saved {marker_path(manuscript)} at unit {args.save_marker}")
        return

    selected = units[args.start - 1 : args.start - 1 + args.count]
    if args.json:
        print(json.dumps([unit.__dict__ for unit in selected], indent=2, ensure_ascii=False))
        return

    for unit in selected:
        print(f"[{unit.number}] line {unit.line} {unit.kind}")
        print(unit.text)
        print()


if __name__ == "__main__":
    main()
