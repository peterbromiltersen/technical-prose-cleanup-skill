---
name: technical-prose-cleanup
description: Apply a correctness-first sentence-by-sentence cleanup pass to technical prose, LaTeX manuscripts, Markdown drafts, or academic text. Use when the user asks to remove LLM writing patterns, especially odd negative statements where a simple positive statement would do, hidden denial-then-assertion frames, apply the tech-writing skill across a document, de-slop technical prose, improve exposition without personal voice transfer, or audit prose for phrase, sentence, paragraph, citation, and math-language failures while preserving equations, labels, citations, theorem/proof structure, notation, and technical claims.
---

# Technical Prose Cleanup

## Overview

Use this skill for document-level technical prose cleanup. It applies the `tech-writing` audits paragraph by paragraph and sentence by sentence, but does not imitate a personal voice. A pattern scan is not enough: each prose sentence must be assigned a role, audited for phrase and grammar failures, and either kept, rewritten, moved, or deleted.

Correctness dominates style. If a cleanup would change a theorem, proof dependency, definition, hypothesis, quantifier, citation claim, mathematical object type, or normative scope, keep the original wording or record the issue in notes.

## Resources

- Audit protocol: `references/audit-protocol.md`
- Anti-patterns: `references/anti-patterns.md`
- Paragraph extractor: `scripts/paragraph_units.py`

Load the audit protocol and anti-patterns before editing. Use the paragraph extractor to avoid skipping paragraphs, headings, displayed equations, theorem-like blocks, and quoted material.

## Default Workflow

1. Identify the source manuscript. If unspecified, prefer `main.tex`, then the largest local `.tex`, `.md`, or `.txt` draft.
2. Create or identify an output draft. By default, write a sibling file named `<stem>.techclean<suffix>`, such as `main.techclean.tex`. Do not overwrite the source unless explicitly asked.
3. Check for `.technical-prose-cleanup-progress.json` next to the source and resume from the recorded paragraph unless the user asks to restart.
4. Run:

```bash
python3 /path/to/skill/scripts/paragraph_units.py <source> --count 40
```

Use `--start <unit-number>` when resuming.

5. Work paragraph by paragraph. For each paragraph:
   - identify its job;
   - inventory every prose sentence in the paragraph;
   - for each sentence, identify its role in the paragraph;
   - audit nontrivial noun phrases, sentence grammar, pronouns, demonstratives, and relational words;
   - check mathematical type discipline;
   - remove filler and formulaic LLM patterns, including odd negative statements and denial-then-assertion pairs spread across adjacent sentences;
   - preserve citations, labels, notation, equations, theorem/proof blocks, and quoted text.
6. Apply only local edits that improve technical clarity or remove visible anti-patterns. Do not impose a personal tone. Keep a sentence, including a metaphorical sentence, when it has a clear technical role and does not obscure the claim.
7. Keep compact notes in `technical-prose-cleanup-notes.md`: current decisions, unresolved technical risks, and next continuation point.
8. Update progress when stopping:

```bash
python3 /path/to/skill/scripts/paragraph_units.py <source> --save-marker <next-unit> --note "Completed through unit <n>."
```

9. Run the natural validation. For LaTeX, prefer the project build command; otherwise run `pdflatex -interaction=nonstopmode -halt-on-error <draft>` and BibTeX/Biber if the manuscript uses a bibliography.

## Editing Policy

- Preserve formal content over style. Do not silently repair technical claims.
- Treat theorem/proof/proposition/definition environments, displayed equations, quotations, bibliography commands, labels, and citations as protected unless the user asks for mathematical revision.
- Prefer simple positive statements to odd negations. Rewrite "not A, it is B" patterns as direct B claims unless the exclusion of A blocks a live misreading or states a formal exclusion, and apply the same test to less explicit negative formulations. Treat "We accept the distinction, but our use of it is not to confine the paper to theorem statements. The unified theorem supplies the common mathematical object, and the later sections ask what argument forms that object makes available" as the anti-pattern and "We accept the distinction, and we will be interested in theorems as well as arguments. The unified theorem supplies the common mathematical object, and the later sections ask what argument forms that object makes available" as the corresponding pattern. Treat split forms as the same pattern: "We do not claim A. We claim B"; "The point is not A. The point is B"; "This is not about A. It is about B." When a limitation is necessary, state the affirmative claim first and then add the scoped limitation.
- Remove empty standalone emphasis sentences such as "That matters." and "This is important." If the point is real, name the operative distinction or consequence.
- Do not add drama, slogans, or pull-quote endings. Preserve good authorial metaphors when they sharpen the technical point; remove metaphors only when they replace the technical claim, overstate it, or read as generic filler.
- Keep hedges when they mark real scope, source uncertainty, modeling limits, or theorem assumptions. Remove hedges that merely soften an already precise claim.

## Maintenance

When this cleanup skill is updated, push the cleanup skill repository to GitHub.
