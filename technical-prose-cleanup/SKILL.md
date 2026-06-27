---
name: technical-prose-cleanup
description: Apply a correctness-first sentence-by-sentence cleanup pass to technical prose, LaTeX manuscripts, Markdown drafts, or academic text. Use when the user asks to remove LLM writing patterns, especially odd negative statements where a simple positive statement would do, hidden denial-then-assertion frames, apply the tech-writing skill across a document, de-slop technical prose, improve exposition without personal voice transfer, or audit prose for phrase, sentence, paragraph, citation, and math-language failures while preserving equations, labels, citations, theorem/proof structure, notation, and technical claims.
---

# Technical Prose Cleanup

## Overview

Use this skill for document-level technical prose cleanup. It applies the `tech-writing` audits sentence by sentence and phrase by phrase, but does not imitate a personal voice. A pattern scan is not enough: each prose sentence must be assigned a role, audited for phrase and grammar failures, and either kept, rewritten, moved, or deleted.

A cleanup pass is incomplete unless every prose sentence in the requested scope has its own audit record. Do not summarize a paragraph as checked, do not report that "the rest looks fine," and do not skip sentences because they contain no obvious anti-pattern. Triage scans for low-hanging fruit are allowed only when the user explicitly asks for triage rather than cleanup.

Correctness dominates style. If a cleanup would change a theorem, proof dependency, definition, hypothesis, quantifier, citation claim, mathematical object type, or normative scope, keep the original wording or record the issue in notes.

## Resources

- Audit protocol: `references/audit-protocol.md`
- Anti-patterns: `references/anti-patterns.md`
- Sentence and paragraph extractor: `scripts/paragraph_units.py`

Load the audit protocol and anti-patterns before editing. Use the extractor in sentence mode for cleanup work so that headings, displayed equations, theorem-like blocks, quoted material, and every prose sentence appear in the work queue. Use paragraph mode only for orientation, not as the main cleanup workflow.

## Default Workflow

1. Identify the source manuscript. If unspecified, prefer `main.tex`, then the largest local `.tex`, `.md`, or `.txt` draft.
2. Create or identify an output draft. By default, write a sibling file named `<stem>.techclean<suffix>`, such as `main.techclean.tex`. Do not overwrite the source unless explicitly asked.
3. Check for `.technical-prose-cleanup-progress.json` next to the source and resume from the recorded sentence-level unit unless the user asks to restart.
4. Initialize a ledger for any multi-paragraph cleanup pass:

```bash
python3 /path/to/skill/scripts/paragraph_units.py <source> --granularity sentence --init-ledger technical-prose-cleanup-ledger.md
```

The ledger is a discipline device, not optional bookkeeping. Each sentence or protected unit must end with one action: kept, revised, deleted, moved, protected, or flagged.

5. Pull exactly the next sentence-level unit:

```bash
python3 /path/to/skill/scripts/paragraph_units.py <source> --granularity sentence --start <unit-number> --count 1
```

Use `--start <unit-number>` when resuming. Increase `--count` only for inspection; do not treat a multi-sentence batch as audited unless each item receives a separate ledger entry.

6. For each sentence unit:
   - identify the parent paragraph's job;
   - identify the sentence's role in that paragraph;
   - audit nontrivial noun phrases, sentence grammar, pronouns, demonstratives, definite descriptions, named labels, and relational words;
   - check mathematical type discipline;
   - scan adjacent sentences when needed for denial-then-assertion frames, odd negations, metronomic rhythm, or hidden scope shifts;
   - apply one action in the ledger: kept, revised, deleted, moved, or flagged;
   - record replacement text when revised, or the concrete reason when kept or flagged.
7. Mark headings, commands, displayed equations, theorem/proof blocks, quotations, bibliography commands, labels, and other protected units as protected in the ledger unless the user has explicitly asked to revise them.
8. Apply only local edits that improve technical clarity or remove visible anti-patterns. Do not impose a personal tone. Keep a sentence, including a metaphorical sentence, when it has a clear technical role and does not obscure the claim.
9. Keep compact notes in `technical-prose-cleanup-notes.md`: current decisions, unresolved technical risks, and next continuation point.
10. Update progress when stopping:

```bash
python3 /path/to/skill/scripts/paragraph_units.py <source> --granularity sentence --save-marker <next-unit> --note "Completed through sentence unit <n>."
```

11. Run the natural validation. For LaTeX, prefer the project build command; otherwise run `pdflatex -interaction=nonstopmode -halt-on-error <draft>` and BibTeX/Biber if the manuscript uses a bibliography.

## Editing Policy

- Preserve formal content over style. Do not silently repair technical claims.
- A sentence is not audited merely because the paragraph containing it was read. Give each sentence an explicit action in the ledger.
- Treat theorem/proof/proposition/definition environments, displayed equations, quotations, bibliography commands, labels, and citations as protected unless the user asks for mathematical revision.
- Check reader-available reference. Do not let a sentence presuppose a theorem, construction, distinction, or label before the reader has encountered it. Replace first-use definites such as "the transfer theorem" with an indefinite introduction such as "a theorem proved below," or introduce the name before relying on "the". When a sentence introduces a new technical term, make the naming act syntactically visible: identify the object already in view, then name it ("Such an addition is a \emph{first-inquiry decoration}: ..."). Do not start with the new term as grammatical subject unless the surrounding text has already prepared it; "A first-inquiry decoration supplies ..." can read as an assertion about an established kind rather than as a first introduction.
- Use typographic emphasis sparingly to mark an important term at first introduction, but keep the definition local: it should tell the reader what object is being named and why it belongs in the paragraph, not pull the section away from its topic.
- Prefer simple positive statements to odd negations. Rewrite "not A, it is B" patterns as direct B claims unless the exclusion of A blocks a live misreading or states a formal exclusion, and apply the same test to less explicit negative formulations. Treat "We accept the distinction, but our use of it is not to confine the paper to theorem statements. The unified theorem supplies the common mathematical object, and the later sections ask what argument forms that object makes available" as the anti-pattern and "We accept the distinction, and we will be interested in theorems as well as arguments. The unified theorem supplies the common mathematical object, and the later sections ask what argument forms that object makes available" as the corresponding pattern. Treat split forms as the same pattern: "We do not claim A. We claim B"; "The point is not A. The point is B"; "This is not about A. It is about B." When a limitation is necessary, state the affirmative claim first and then add the scoped limitation.
- Remove empty standalone emphasis sentences such as "That matters." and "This is important." If the point is real, name the operative distinction or consequence.
- Do not add drama, slogans, or pull-quote endings. Preserve good authorial metaphors when they sharpen the technical point; remove metaphors only when they replace the technical claim, overstate it, or read as generic filler.
- Keep hedges when they mark real scope, source uncertainty, modeling limits, or theorem assumptions. Remove hedges that merely soften an already precise claim.

## Maintenance

The installed skill directory is not a git checkout. The source folder is `/home/bromille/technical-prose-cleanup-skill`; when this cleanup skill is updated, update that folder and push it to GitHub.
