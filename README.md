# Quill

A five-stage, prompt-driven content pipeline that turns a one-paragraph brief into a fact-checked,
graded SEO/AEO landing page. Every factual sentence must trace to a numbered section of a single
"bible" file; anything else is gated out before it can ship.

In production this pipeline generated 400+ landing pages (integration "spoke" and single-capability
"sub-spoke" pages) for an AI productivity startup. A nightly worker ran it unattended and wrote
drafts into a Webflow CMS for human review. The product name, bible, and reference material from
that deployment are not in this repo; a fictional product ("Kestrel") stands in so the pipeline runs
end to end.

## Why it exists

Programmatic SEO at hundreds of pages has two failure modes: the model invents product capabilities,
and the pages read like templates. Quill treats those as separate problems with separate gates.
Hallucination is caught by a fact-checker that only checks claims against the bible. Voice is
caught by a reviewer that only checks register and never rules on facts. Keeping the two apart is
the main design decision; a single "review" prompt tends to pass invented claims that sound on-brand
and fail true claims that sound off-brand.

## Architecture

```
briefs/<slug>.md ----+
                     |
bible/*.md ----------+---> 1 orchestrator ---> outline.md   (skeleton + fact map + gated-claims list)
                                  |
                                  v
                            2 writer --------> draft.md
                                  |
                                  v
                            3 reviewer ------> review.md    PASS | REVISE --> rewrite
                                  |
                                  v
                            4 fact-checker --> factcheck.md PASS | FAIL   --> rewrite (max N)
                                  |
                                  v
                            5 grader (blind) -> grade.md    A..F; A/B promotes draft -> final.md
```

Each stage is a role prompt in `prompts/`. Each stage reads only what it needs and writes one
file to `output/<slug>/`. The runner wires them together; the prompts also work by hand in any
file-reading agent.

### Stage contracts

| Stage | Reads | Writes | Gate |
| --- | --- | --- | --- |
| 1 Orchestrator | brief, bible | `outline.md`: H1, section headers, the bible facts (by section number) under each, and a list of claims the page would need that the bible does not verify | none; the gated-claims list is the handoff |
| 2 Writer | outline, bible | `draft.md` | must not assert anything on the gated list |
| 3 Reviewer | draft, bible S3 + S15 | `review.md`: numbered fixes, each with the rule broken | PASS / REVISE on voice only |
| 4 Fact-checker | draft, bible | `factcheck.md`: one row per claim, PASS + section or FLAG + reason | PASS / FAIL on facts only |
| 5 Grader | draft, brief, bible | `grade.md`: six 0-10 scores, letter grade, hallucination audit | reads neither review nor factcheck |

## Design decisions

**Outline before prose.** The orchestrator maps every section to specific bible facts before a
word of copy exists. The writer never searches the bible; it fills a skeleton that already cites
its sources. Most hallucinations happen when a model writes and retrieves at the same time.

**One source of truth with provenance tiers.** The bible labels every fact: PRODUCT-VERIFIED,
DOCS-VERIFIED, FOUNDER-STATED (a founder's dated public answer, citable with attribution),
TELEMETRY-VERIFIED, or NEEDS-VERIFICATION. The writer may reframe wording freely but may never
exceed the tier of the underlying fact.

**Two-tier gating.** Privacy, security, compliance, pricing, and quotes are Tier 1: hard-gated,
never written unverified, hard FAIL at fact-check. Integration capabilities are Tier 2: writable
if telemetry-backed or product-plausible, logged as a NOTE rather than a FLAG. The tolerance
is explicit (~1-2% error on Tier 2) because the pipeline optimizes for volume, and the cost of a
wrong "reads your Linear issues" is nothing like the cost of a wrong "SOC 2 certified".
See `prompts/GATING-POLICY.md`.

**Composed claims.** "Read the transcript, then create the page" is allowed if and only if every
leg is independently verified. The fact-checker evaluates the conjunction, not the sentence.

**Register is not a fact.** The fact-checker is told, in so many words, not to flag a claim for
sounding stronger than the bible's phrasing. Only an unsupported capability or absolute fails.
Before this rule the fact-checker rejected most good writing.

**Blind grading.** The grader never sees the reviewer's or fact-checker's output and uses a
different model by default (`grader_model` in config). It produces its own hallucination audit,
which is the cheapest regression test for the fact-checker.

**Respectful comparison as a hard rule.** The writer may not describe a competitor or an
integration partner negatively, in any construction. Pages about a partner's integration were
the ones most likely to insult the partner.

## Run it

```
export OPENROUTER_API_KEY=...        # or whatever runner/config.json names
cp briefs/EXAMPLE-brief.md briefs/google-drive-cite-sources.md
python3 runner/run.py google-drive-cite-sources
```

Output lands in `output/google-drive-cite-sources/`. `--from 3` resumes at a stage; `--all`
runs every brief. The runner is stdlib-only and talks to any OpenAI-compatible chat endpoint;
set `base_url`, `model`, and `product` in `runner/config.json`.

To use your own product: replace `bible/EXAMPLE-bible.md` with your bible (keep the section
numbering the prompts reference: 3 voice, 4 core facts, 5 pricing, 9 integrations, 10 privacy,
15 hard don'ts), set `product` in the config, and write briefs.

## Layout

```
prompts/   1..5 stage prompts + GATING-POLICY.md   (the spec)
bible/     the single source of product facts     (EXAMPLE-bible.md: fictional product)
briefs/    one brief per page
output/    generated files per slug               (gitignored)
runner/    run.py + config.json
AGENTS.md  instructions for running the stages by hand in a coding agent (CLAUDE.md symlinks to it)
```

## What production taught me

- **Never overwrite what you did not write.** The nightly worker once cleared CMS fields that a
  human had hand-edited, because a sync step matched items by name. The fix was a set of
  idempotency rules: the worker only touches items it authored, skips any item edited since its
  last write, writes drafts only, and never flips a draft live. Those rules belong in the worker,
  not the prompts.
- **Two copies of the bible will drift.** The repo copy and the copy the worker read diverged
  within weeks. One canonical file, pulled at run time, or nothing.
- **Bible updates do not re-edit live pages.** When a fact changes, the change applies to future
  builds. Re-editing hundreds of live pages for every bible revision is how you get a spam
  classification.
- **Generic pages are the risk, not the volume.** A spam-update exposure audit put the risk on
  the pages whose anchor capability was weakest, not on the page count. Briefs with a vague
  anchor capability should be rejected at stage 1.
- **Keep the bible fresh from public sources.** A sibling bot scraped the founders' public Reddit
  and Discord answers weekly and opened PRs against the bible with each fact cited by permalink
  and date. That is where the FOUNDER-STATED tier came from.
- **Pin punctuation policy in the prompt.** Graders disagreed about whether `--` was an em dash
  violation until the policy named the ASCII stand-in explicitly.

## License

MIT
