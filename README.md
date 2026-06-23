# Technical Prose Cleanup Skill

A Codex skill for correctness-first cleanup of technical prose, especially LaTeX manuscripts, Markdown drafts, and academic text.

It guides the agent to work paragraph by paragraph, assign each sentence a role, audit phrase grammar and mathematical type discipline, remove formulaic LLM writing patterns, and preserve equations, theorem/proof structure, labels, citations, and technical claims.

## What is included

- `technical-prose-cleanup/SKILL.md`: skill instructions and trigger metadata.
- `technical-prose-cleanup/references/audit-protocol.md`: paragraph and sentence audit checklist.
- `technical-prose-cleanup/references/anti-patterns.md`: common technical prose failures to remove.
- `technical-prose-cleanup/scripts/paragraph_units.py`: helper for enumerating cleanup units and saving progress markers.
- `technical-prose-cleanup/agents/openai.yaml`: UI metadata for Codex skill lists.

## Install

From Codex, run the skill installer:

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-installer/scripts/install-skill-from-github.py" \
  --repo peterbromiltersen/technical-prose-cleanup-skill \
  --path technical-prose-cleanup
```

Then restart Codex so it discovers the new skill.

Manual fallback: copy the `technical-prose-cleanup/` directory into `${CODEX_HOME:-$HOME/.codex}/skills/`, then restart Codex.

## Use

Ask Codex something like:

```text
Use $technical-prose-cleanup to clean up main.tex paragraph by paragraph without changing the math.
```

The skill writes cleanup work to a sibling draft by default, such as `main.techclean.tex`, and records progress in `.technical-prose-cleanup-progress.json`.

## License

MIT.
