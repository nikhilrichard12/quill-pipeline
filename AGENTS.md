# Quill: agent instructions

This repo is content GENERATION only. No CMS access, no publishing. The pipeline writes
`output/<slug>/*.md` on disk; loading and publishing happen elsewhere.

Run the stages IN ORDER for a slug that matches `briefs/<slug>.md`:

1. prompts/1-orchestrator.md -> output/<slug>/outline.md (skeleton + fact map + gated-claims list)
2. prompts/2-writer.md       -> output/<slug>/draft.md
3. prompts/3-reviewer.md     -> output/<slug>/review.md (verdict PASS/REVISE; apply required fixes)
4. prompts/4-factchecker.md  -> output/<slug>/factcheck.md (per-claim PASS/FLAG; resolve every FLAG)
5. prompts/5-grader.md       -> output/<slug>/grade.md (blind rubric grade; do not read review/factcheck)

The Bible (`bible/*.md`) is the only source of product facts. Every factual sentence must trace to
a numbered section. Anything the Bible lacks or marks NEEDS-VERIFICATION is `[GATED]` and is never
asserted as fact. See prompts/GATING-POLICY.md. `{{PRODUCT}}` in the prompts is the product name.

Any file-reading agent (Claude Code, Codex, Cursor, Aider) can run these by hand. `runner/run.py`
runs them unattended against any OpenAI-compatible chat API.
