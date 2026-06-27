#!/usr/bin/env python3
"""Extract paragraph- or sentence-scale cleanup units and save progress markers."""

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


@dataclass
class SentenceUnit:
    number: int
    line: int
    kind: str
    text: str
    parent_unit: int
    parent_kind: str
    sentence_index: int | None
    context: str


STRUCTURAL_PARAGRAPH_COMMANDS = {
    "address",
    "author",
    "date",
    "email",
    "institute",
    "keywords",
    "subjclass",
    "thanks",
    "title",
}

ABBREVIATIONS = {
    "cf.",
    "dr.",
    "e.g.",
    "ed.",
    "eds.",
    "etc.",
    "fig.",
    "i.e.",
    "mr.",
    "mrs.",
    "ms.",
    "no.",
    "p.",
    "pp.",
    "prof.",
    "sec.",
    "st.",
    "vs.",
}

SENTENCE_CLOSERS = "\"'`)]}"


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


def begin_display_math(line: str) -> str | None:
    if line.startswith(r"\["):
        return "bracket-display"
    if line.startswith("$$"):
        return "dollar-display"
    return None


def end_protected_block(line: str, marker: str) -> bool:
    if marker.startswith("env:"):
        return end_environment(line, marker[4:])
    if marker == "bracket-display":
        return r"\]" in line
    if marker == "dollar-display":
        return line.endswith("$$")
    return False


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
            marker, start_line, block = in_block
            block.append(raw_line)
            if end_protected_block(line, marker):
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
            marker = f"env:{env}"
            if end_protected_block(line, marker):
                add_unit(units, line_number, "protected-block", "\n".join(block))
            else:
                in_block = (marker, line_number, block)
            continue

        display_math = begin_display_math(line)
        if display_math:
            flush_paragraph()
            block = [raw_line]
            if line != r"\[" and line != "$$" and end_protected_block(line, display_math):
                add_unit(units, line_number, "protected-block", "\n".join(block))
            else:
                in_block = (display_math, line_number, block)
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


def is_structural_paragraph(text: str) -> bool:
    stripped = text.strip()
    match = re.match(r"\\([A-Za-z]+)\*?(?:\[[^\]]*\])?\{", stripped)
    return bool(match and match.group(1) in STRUCTURAL_PARAGRAPH_COMMANDS)


def is_escaped(text: str, index: int) -> bool:
    slash_count = 0
    cursor = index - 1
    while cursor >= 0 and text[cursor] == "\\":
        slash_count += 1
        cursor -= 1
    return slash_count % 2 == 1


def preceding_token(text: str, index: int) -> str:
    cursor = index
    while cursor >= 0 and (text[cursor].isalpha() or text[cursor] == "."):
        cursor -= 1
    return text[cursor + 1 : index + 1].lower()


def should_split_at(text: str, index: int, brace_depth: int, bracket_depth: int, in_math: bool) -> bool:
    char = text[index]
    if char not in ".?!" or in_math or brace_depth or bracket_depth:
        return False
    if char == ".":
        if index > 0 and index + 1 < len(text) and text[index - 1].isdigit() and text[index + 1].isdigit():
            return False
        if preceding_token(text, index) in ABBREVIATIONS:
            return False
    cursor = index + 1
    while cursor < len(text) and text[cursor] in SENTENCE_CLOSERS:
        cursor += 1
    if cursor >= len(text):
        return True
    if text[cursor].isspace():
        return True
    return False


def split_sentences(text: str) -> list[str]:
    sentences: list[str] = []
    start = 0
    brace_depth = 0
    bracket_depth = 0
    in_math = False
    index = 0

    while index < len(text):
        char = text[index]
        if char == "$" and not is_escaped(text, index):
            in_math = not in_math
        elif not in_math:
            if char == "{" and not is_escaped(text, index):
                brace_depth += 1
            elif char == "}" and not is_escaped(text, index):
                brace_depth = max(0, brace_depth - 1)
            elif char == "[" and not is_escaped(text, index):
                bracket_depth += 1
            elif char == "]" and not is_escaped(text, index):
                bracket_depth = max(0, bracket_depth - 1)

        if should_split_at(text, index, brace_depth, bracket_depth, in_math):
            end = index + 1
            while end < len(text) and text[end] in SENTENCE_CLOSERS:
                end += 1
            sentence = text[start:end].strip()
            if sentence:
                sentences.append(sentence)
            start = end
            while start < len(text) and text[start].isspace():
                start += 1
            index = start
            continue
        index += 1

    trailing = text[start:].strip()
    if trailing:
        sentences.append(trailing)
    return sentences


def sentence_units(units: list[Unit]) -> list[SentenceUnit]:
    items: list[SentenceUnit] = []

    def add_item(unit: Unit, kind: str, text: str, sentence_index: int | None = None) -> None:
        items.append(
            SentenceUnit(
                number=len(items) + 1,
                line=unit.line,
                kind=kind,
                text=text,
                parent_unit=unit.number,
                parent_kind=unit.kind,
                sentence_index=sentence_index,
                context=unit.text,
            )
        )

    for unit in units:
        if unit.kind != "paragraph":
            add_item(unit, unit.kind, unit.text)
            continue
        if is_structural_paragraph(unit.text):
            add_item(unit, "protected-paragraph", unit.text)
            continue
        sentences = split_sentences(unit.text)
        if not sentences:
            add_item(unit, "empty-paragraph", unit.text)
            continue
        for index, sentence in enumerate(sentences, start=1):
            add_item(unit, "sentence", sentence, index)
    return items


def marker_path(manuscript: Path) -> Path:
    return manuscript.parent / MARKER_NAME


def save_marker(manuscript: Path, units: list[Unit] | list[SentenceUnit], next_unit: int, note: str, granularity: str) -> None:
    target = next((unit for unit in units if unit.number == next_unit), None)
    payload = {
        "manuscript": str(manuscript),
        "granularity": granularity,
        "next_unit": next_unit,
        "next_line": target.line if target else None,
        "saved_at": datetime.now(timezone.utc).isoformat(),
        "note": note,
    }
    marker_path(manuscript).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def markdown_cell(text: object) -> str:
    if text is None:
        return ""
    return str(text).replace("|", r"\|").replace("\n", "<br>")


def write_ledger(path: Path, manuscript: Path, units: list[Unit] | list[SentenceUnit], granularity: str) -> None:
    if path.exists():
        raise SystemExit(f"Refusing to overwrite existing ledger: {path}")
    lines = [
        f"# Technical Prose Cleanup Ledger: {manuscript.name}",
        "",
        f"Granularity: `{granularity}`",
        "",
        "| Item | Line | Kind | Parent | Sentence | Action | Notes | Text |",
        "| --- | ---: | --- | ---: | ---: | --- | --- | --- |",
    ]
    for unit in units:
        parent = getattr(unit, "parent_unit", unit.number)
        sentence_index = getattr(unit, "sentence_index", "")
        lines.append(
            "| "
            + " | ".join(
                [
                    markdown_cell(unit.number),
                    markdown_cell(unit.line),
                    markdown_cell(unit.kind),
                    markdown_cell(parent),
                    markdown_cell(sentence_index),
                    "",
                    "",
                    markdown_cell(unit.text),
                ]
            )
            + " |"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("manuscript", type=Path)
    parser.add_argument("--granularity", choices=["paragraph", "sentence"], default="paragraph")
    parser.add_argument("--start", type=int, default=1)
    parser.add_argument("--count", type=int, default=20)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--init-ledger", type=Path)
    parser.add_argument("--save-marker", type=int)
    parser.add_argument("--note", default="")
    args = parser.parse_args()

    manuscript = args.manuscript.resolve()
    paragraph_units = extract_units(manuscript)
    units = paragraph_units if args.granularity == "paragraph" else sentence_units(paragraph_units)

    if args.init_ledger is not None:
        write_ledger(args.init_ledger, manuscript, units, args.granularity)
        return

    if args.save_marker is not None:
        save_marker(manuscript, units, args.save_marker, args.note, args.granularity)
        print(f"Saved {marker_path(manuscript)} at unit {args.save_marker}")
        return

    selected = units[args.start - 1 : args.start - 1 + args.count]
    if args.json:
        print(json.dumps([unit.__dict__ for unit in selected], indent=2, ensure_ascii=False))
        return

    if args.granularity == "paragraph":
        for unit in selected:
            print(f"[{unit.number}] line {unit.line} {unit.kind}")
            print(unit.text)
            print()
        return

    for unit in selected:
        sentence_index = "" if unit.sentence_index is None else f".{unit.sentence_index}"
        print(f"[{unit.number}] line {unit.line} {unit.kind} parent {unit.parent_unit}{sentence_index}")
        print(unit.text)
        print()


if __name__ == "__main__":
    main()
