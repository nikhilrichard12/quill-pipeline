The Kestrel Bible (v1.0, example)
Single source of truth for the content pipeline. Writers draft from this. The fact-checker rejects
anything not in it. Treat every fact here as the only authoritative version. If a claim is not in
this bible, it cannot go on a page.

Kestrel is a FICTIONAL product used to demonstrate the pipeline. Replace this file with your own
bible, keep the section numbering, and set PRODUCT in runner/config.json.

Provenance tiers: PRODUCT-VERIFIED > DOCS-VERIFIED > FOUNDER-STATED > TELEMETRY-VERIFIED >
NEEDS-VERIFICATION (do not publish). See prompts/GATING-POLICY.md.

1. How to use this bible
Cite by section. Every factual sentence must trace to a numbered section here.
Atomic facts only. Do not embellish a fact into something stronger than written.
Approved phrasing shows the REGISTER and the verified capability, not a word ceiling. Reframe the
wording freely in the Section 3 voice; never inflate the claim.
Composed claims: combining two VERIFIED capabilities is allowed and is fact-checked as the
conjunction of its parts. Never compose with an unverified tool.
Never invent features, integrations, mechanics, stats, prices, quotes, or customer names.

2. Source-of-truth table
Pricing: kestrel.example/pricing (DOCS-VERIFIED, 2026-09-01)
Integration mechanics: Section 9, from the product docs (DOCS-VERIFIED, 2026-09-01)
Security: Section 10, from the security page (DOCS-VERIFIED, 2026-09-01)
Everything else: NEEDS-VERIFICATION unless labeled.

3. Brand voice and tone
Core thesis (the spine of every page): most tools only know what you told them. Kestrel reads the
documents your team already shares in connected tools, so answers start from what actually happened.
Lead with a concrete failure scene (the thread, the doc, the meeting), then the thesis turn, then one
plain connect line. Never open with a feature.
Contractions are house style. Short declarative sentences. ASCII punctuation only; "--" stands in
for an em dash.
Top-level spoke H1: short, verb-led, two beats, a setup and a payoff. Example register (do not
copy): "Find the decision, cite the thread, close the loop."
Sub-spoke H1: instructional, SEO-literal, Title Case: "How to [X] with Kestrel's [Tool] Integration".
Capability lines: "Kestrel can [verb]..., so [the concrete moment it matters]." Vary the benefit.
Never a flat list where every line follows the same template.

4. Core product facts (atomic, quotable)
4.1 What it is. Kestrel is a team knowledge assistant that answers questions from the documents and
threads your team already has in connected tools. (DOCS-VERIFIED)
4.2 One-liner. "Kestrel answers from what your team already wrote."
4.3 How it works. Kestrel indexes the content of connected tools (Section 9) and answers questions
in chat with citations back to the source document or thread. (DOCS-VERIFIED)
4.4 Platforms. Web app and Slack app. (DOCS-VERIFIED) Desktop app: NEEDS-VERIFICATION, do not claim.
4.5 Controls. Workspace admins choose which tools connect and can exclude channels or folders.
Users can delete the index for a connected tool at any time. (DOCS-VERIFIED)
4.6 Company facts. Founded 2025. Team of 14. (FOUNDER-STATED, founder blog post 2026-06-02.) Funding
figures: NEEDS-VERIFICATION, do not publish.

5. Pricing (canonical block, DOCS-VERIFIED, kestrel.example/pricing, 2026-09-01)
Free: 1 connected tool, 50 questions per month.
Team: $12 per seat per month billed annually; unlimited questions, up to 5 connected tools.
Business: $28 per seat per month billed annually; everything in Team, unlimited connected tools,
SSO, audit log.
Enterprise: contact sales. Do not state a price.
Writer rule: no other prices, no discounts, no "starting at" figures beyond these.

6. Features
6.1 Ask. Chat with citations to the source document or thread. Answers include a link to every
source used. (DOCS-VERIFIED)
6.2 Digest. A scheduled summary of what changed across connected tools, delivered to Slack or
email, daily or weekly. (DOCS-VERIFIED) Custom schedules beyond daily/weekly: NEEDS-VERIFICATION.
6.3 Collections. Pin a set of documents so questions scope to them. (DOCS-VERIFIED)
6.4 Browser extension: NEEDS-VERIFICATION. Do not claim.

7. Positioning
7.1 Positioning statement. For teams whose answers are scattered across docs and chat, Kestrel is
the assistant that already read everything the team shared, so answers come with the source.
7.2 Signature differentiator. A general chatbot starts from a blank prompt. Kestrel starts from the
documents your team already wrote. State this on Kestrel's own terms; never as a defect of another
product.

9. Integrations (DOCS-VERIFIED unless noted)
9.1 Google Drive. Reads: Docs, Sheets, Slides, PDFs in connected folders. Writes: none. Approved
phrasing: "Kestrel reads the Google Docs your team shares and cites the exact doc in every answer."
9.2 Slack. Reads: messages in connected public channels. Writes: posts Digest summaries to a channel
you choose; answers questions when mentioned. Private channels: NEEDS-VERIFICATION, do not claim.
9.3 Notion. Reads: pages and databases in connected workspaces. Writes: none. Comments:
NEEDS-VERIFICATION.
9.4 Linear. Reads: issues, comments, project descriptions. Writes: none. (TELEMETRY-VERIFIED,
Tier 2 soft gate; note in the QA report, not inline.)
9.5 Other integrations (list only, mechanics NEEDS-VERIFICATION): GitHub, Jira, Confluence.
Do not describe what Kestrel does with these beyond "connects to".

10. Privacy and security (Tier 1, DOCS-VERIFIED, security page 2026-09-01)
10.1 Kestrel does not train models on customer data.
10.2 Data is encrypted in transit (TLS 1.2+) and at rest (AES-256).
10.3 Hosted on AWS in us-east-1. EU residency: NEEDS-VERIFICATION, do not claim.
10.4 SOC 2 Type II report available on request. Do not write "SOC 2 certified".
10.5 GDPR: NEEDS-VERIFICATION. Do not claim compliance or alignment.

12. Competitors
Named competitors get neutral, factual, dated treatment only. No pejoratives. See Section 15.

15. Hard Don'ts
- Banned words: seamless, effortless, streamline, game-changer, supercharge, unlock, revolutionize.
- No Unicode em or en dashes. "--" only.
- Never claim a desktop app, browser extension, private-channel reading, EU residency, GDPR status,
  or any item marked NEEDS-VERIFICATION.
- Never state a price outside Section 5.
- "SOC 2 Type II report available", never "SOC 2 certified".
- Never denigrate a competitor, an integration partner, or a category of tool.
- Never open a page with a feature. Open with the failure scene.
- Never invent a customer, quote, or statistic.

Appendix A. Open items (roadmap and unresolved)
- Desktop app (4.4)
- Browser extension (6.4)
- Slack private channels (9.2)
- Notion comments (9.3)
- EU data residency (10.3)
- GDPR status (10.5)
