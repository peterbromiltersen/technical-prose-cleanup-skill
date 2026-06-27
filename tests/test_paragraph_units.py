#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "technical-prose-cleanup" / "scripts" / "paragraph_units.py"
FIXTURE = ROOT / "tests" / "fixtures" / "sample.tex"

spec = importlib.util.spec_from_file_location("paragraph_units", SCRIPT)
paragraph_units = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = paragraph_units
spec.loader.exec_module(paragraph_units)


class ParagraphUnitsTest(unittest.TestCase):
    def test_paragraph_mode_shape_is_unchanged(self) -> None:
        units = paragraph_units.extract_units(FIXTURE)

        self.assertEqual(units[0].number, 1)
        self.assertEqual(units[0].kind, "paragraph")
        self.assertTrue(units[0].text.startswith(r"\title{A small fixture}"))
        self.assertTrue(any(unit.kind == "protected-block" for unit in units))

    def test_sentence_mode_splits_prose_and_protects_structure(self) -> None:
        units = paragraph_units.extract_units(FIXTURE)
        sentence_units = paragraph_units.sentence_units(units)
        sentence_texts = [unit.text for unit in sentence_units if unit.kind == "sentence"]
        protected_texts = [unit.text for unit in sentence_units if unit.kind in {"protected-block", "protected-paragraph"}]

        self.assertIn("First sentence with e.g. an abbreviation.", sentence_texts)
        self.assertIn(r"Second sentence cites \citep[p. 12]{Source}.", sentence_texts)
        self.assertIn("Third sentence has $x=1.2$ and continues.", sentence_texts)
        self.assertIn("Before theorem.", sentence_texts)
        self.assertIn("After display math.", sentence_texts)
        self.assertTrue(any(text.startswith(r"\title") for text in protected_texts))
        self.assertTrue(any(r"\author" in text for text in protected_texts))
        self.assertTrue(any(text.startswith(r"\begin{theorem}") for text in protected_texts))
        self.assertTrue(any(text.startswith(r"\[") for text in protected_texts))

    def test_ledger_contains_every_sentence_item(self) -> None:
        units = paragraph_units.sentence_units(paragraph_units.extract_units(FIXTURE))
        with tempfile.TemporaryDirectory() as tmpdir:
            ledger = Path(tmpdir) / "ledger.md"
            paragraph_units.write_ledger(ledger, FIXTURE, units, "sentence")
            contents = ledger.read_text(encoding="utf-8")

        self.assertIn("Granularity: `sentence`", contents)
        self.assertIn("First sentence with e.g. an abbreviation.", contents)
        self.assertIn("protected-block", contents)


if __name__ == "__main__":
    unittest.main()
