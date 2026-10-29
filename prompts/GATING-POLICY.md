# Gating Policy

Rationale: the pipeline optimizes for SEO/AEO volume, so a small error rate on integration
capabilities (~1-2%) is acceptable. Claims that carry legal, privacy, or trust risk are not.
Hence two tiers.

---

## TIER 1 -- HARD GATE
Never relaxed. Verification required before the claim is written or published.

Includes:
- Privacy claims (what the product collects, sees, stores, or does not)
- Security and encryption claims (ciphers, key management, audits, certifications)
- Data storage and residency details
- Legal and compliance claims (SOC 2, GDPR, CCPA, HIPAA)
- Pricing claims (plan names, prices, what each plan includes)
- Customer quotes (approved list only)

Writer rule: if a Tier 1 claim is not verified in the Bible, do NOT write it. Insert
[GATED: TIER 1 -- requires verification before publish] and note it in the QA report.

Fact-checker rule: a Tier 1 claim not traceable to a verified Bible section is a hard FAIL.
It blocks the page.

---

## TIER 2 -- SOFT GATE
Integration capabilities only: what the product reads, writes, finds, or does through a
connected integration.

May be written if the capability is:
(a) telemetry-backed (appears in usage data or is marked SHOWCASE in the Bible), OR
(b) product-plausible (consistent with how the integration is described in the Bible and
    does not exceed the approved phrasing ceiling)

Never fabricate a capability with no telemetry or product basis.

Writer rule: write the capability as a clean declarative sentence, no inline [GATED] block.
In the QA report, note each capability not yet app-verified:
"CAPABILITY NOTE: [capability] -- telemetry-backed / product-plausible, not yet app-verified."

Fact-checker rule: do NOT hard-fail a Tier 2 claim. Log it as a NOTE in the factcheck table.
The page verdict may still be PASS.

---

## PROVENANCE TIERS (how the Bible labels its own facts)

PRODUCT-VERIFIED   first-hand, app-tested
DOCS-VERIFIED      confirmed on the product's published documentation or changelog
FOUNDER-STATED     a founder's dated public statement, cited with a permalink; quotable with
                   attribution; contractual or legal claims still need explicit confirmation
TELEMETRY-VERIFIED usage data; Tier 2 soft gate
NEEDS-VERIFICATION do not publish

Where a changelog entry and a FOUNDER-STATED line conflict, the changelog governs.

---

## PUNCTUATION POLICY
The Bible bans Unicode em and en dashes in output. The ASCII double hyphen "--" is the
approved stand-in. Reviewers and graders must not flag "--".
