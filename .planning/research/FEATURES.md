# Feature Research

**Domain:** Quality auditing & remediation system for the 67 existing Claude scientific skills
**Researched:** 2026-05-20
**Confidence:** HIGH (constraints are clear; existing CONCERNS.md provides ground truth on real defects)

## Feature Landscape

### Table Stakes (Audit System Cannot Be Trusted Without These)

These features are non-negotiable. Missing any of them means the audit produces unreliable verdicts.

| Feature | Why Expected | Complexity | Notes / Rubric Dimension |
|---------|--------------|------------|---------------------------|
| **Rubric document (single source of truth)** | All 67 audits must use the SAME criteria. Without a versioned rubric, audits drift and cannot be compared | LOW | Cross-cutting — anchors everything |
| **Frontmatter schema validation** | CONCERNS.md flags 6 "Unknown" licenses, inconsistent capitalization, missing `compatibility` for skills needing API keys | LOW | Runnability + Discoverability |
| **marketplace.json ↔ disk consistency check** | CONCERNS critical: 142 registered, 67 on disk; 74 phantom registrations | LOW | Runnability (structural) |
| **Per-skill audit report (machine-readable + human-readable)** | Need both: machine for cross-cutting analysis ("how many skills fail X?"), human for triage decisions | MEDIUM | All 4 dimensions |
| **Severity classification (Critical / High / Medium / Low)** | Must drive fix-prioritization. Aligns with CONCERNS.md's existing language so contributors recognize it | LOW | All 4 dimensions |
| **Static lint pass on Python scripts** | ruff + pyright: catches deprecated APIs, broken imports, syntax errors. The bulk of "code can't run" issues are detectable statically | MEDIUM | Runnability |
| **Markdown structural lint** | Heading hierarchy, broken internal anchors, malformed code fences | LOW | Discoverability + Rigor |
| **Cross-skill reference validation** | CONCERNS observed dependency chains (`literature-review` → `scientific-schematics` MANDATORY) but no formal declaration. Audit must verify these references resolve | MEDIUM | Discoverability + Runnability |
| **External link integrity (lychee)** | Citation rot is the #1 quiet failure mode in scientific docs | MEDIUM | Academic Rigor |
| **Aggregated dashboard** | One file showing the audit state across all 67 skills — without this, the user cannot triage or watch progress | LOW | Cross-cutting |
| **Fix-tracking state per skill** | "Found", "Triaged", "Fixed", "Won't fix" — checkbox-style, in-repo, machine-parseable | LOW | Cross-cutting |

### Differentiators (Raise Audit Quality Significantly)

These are genuinely valuable but require more design / cost. Each must be justified against the user's "auto + spot-check" stance.

| Feature | Value Proposition | Complexity | Notes / Rubric Dimension |
|---------|-------------------|------------|---------------------------|
| **LLM-as-judge for description quality** | Mechanical lints can't tell "would Claude trigger this skill on the right user prompt?" — only an LLM can | MEDIUM | Discoverability — high leverage; description is what makes a skill discoverable |
| **Synthetic-task triggering test** | For each skill, generate 5-10 plausible user prompts that SHOULD trigger it and 5 that should NOT; verify Claude's selection | HIGH | Discoverability — converts triggering from subjective to measurable |
| **Toy-example detector (LLM + heuristic)** | Flag scripts using `np.random.rand(100)`, `make_classification(n_samples=20)`, etc. when no realistic alternative is shown | MEDIUM | Real-world Coverage |
| **Methodology checklist per scientific subdomain** | Bioinformatics skill must follow appropriate reporting (e.g., MIAPE, MIxS); clinical skills CONSORT/STROBE; ML benchmarks must specify dataset + metric + baseline | HIGH | Academic Rigor — domain-specific quality |
| **API-key requirement reconciliation** | CONCERNS lists 11+ skills needing keys, only 4 declare via `compatibility`. Audit detects undeclared keys via prose scan + script scan | MEDIUM | Runnability + Discoverability |
| **Cross-skill dependency graph** | Build implicit graph from "see X skill" / "uses Y" mentions; verify referenced skills exist and aren't deleted | MEDIUM | Runnability + Discoverability |
| **K-Dense / "Nano Banana Pro" boilerplate detector** | CONCERNS flagged this — proprietary references in 10+ skills create undeclared external dependencies. Audit flags consistently | LOW | Discoverability — clarity to user |
| **Promotional-content flagging** | "Suggest Using K-Dense Web For Complex Worflows" sections — should be consistent OR removed; currently inconsistently applied with a typo | LOW | Discoverability |
| **Versioning / freshness metadata** | Add `last-verified` date per database skill (28+ DB skills exposed to API drift) | MEDIUM | Academic Rigor — citation/API rot |

### Anti-Features (Explicitly NOT Building — Confirmed by PROJECT.md Out of Scope)

| Feature | Why Requested | Why Problematic | Alternative |
|---------|---------------|-----------------|-------------|
| Actually run scripts in isolated venvs | Would catch runtime-only bugs | User explicitly chose static-only; execution introduces dependency-resolution cost, flaky network access, breaks on missing API keys | Trust ruff + pyright + lychee to catch the high-value subset |
| End-to-end "use this skill on a real research task" regression | Highest fidelity validation | Costs 67× the time of a static audit; not aligned with chosen verdict mechanism (structured checklist) | Defer to a future milestone if needed; sample 3-5 skills manually as confidence check |
| Adding new skills | Would expand coverage | Out of scope per user decision; mixing scope with quality work loses focus | Track ideas in a separate backlog file for future milestone |
| Multi-language SKILL.md (i18n) | Broader user base | Adds combinatorial audit cost; user explicitly excluded | English remains canonical |
| Tech-stack rewrites (replace Python lib choices) | Could "modernize" skills | This is "refactor", not "quality" — different goal; scope creep risk | Out of scope; only flag if the chosen lib is actually broken |
| Per-skill PR-style review with human approval | Highest quality | User explicitly chose auto + spot-check; 67-skill manual review is the bottleneck this whole project tries to avoid | Spot-check at gates: rubric approval, deletion decisions, before final merge |

## Feature Dependencies

```
Rubric (single source of truth)
    └──required by──> All 4 audit dimensions
                          └──required by──> Per-skill audit report
                                                └──required by──> Aggregated dashboard
                                                └──required by──> Fix-tracking state
                                                └──required by──> Re-verification

Frontmatter schema validation
    └──required by──> marketplace ↔ disk consistency check
    └──required by──> API-key reconciliation

Static lint (ruff + pyright)
    └──independent of──> all other dimensions

LLM-as-judge for description quality
    └──requires──> Synthetic-task triggering set (or it's just opinion-vs-opinion)

Cross-skill dependency graph
    └──enhances──> External link integrity (overlaps in detection)
```

### Dependency Notes

- **Rubric must come first.** Everything downstream calibrates to it. A vague rubric → unreliable audits.
- **marketplace ↔ disk consistency must be resolved early.** If 74 skills are phantom, audit results referencing those skills are noise. This is a "fix before audit" issue or "decide deletion plan first."
- **LLM-as-judge needs ground truth.** Without synthetic prompts (or human-labeled examples), LLM critiques become unfalsifiable opinion.
- **Static lint is parallelizable per-skill.** No shared state — ideal for batch processing.

## MVP Definition (for the Audit System Itself)

### Launch With (v1 — Phase 1-2 of roadmap)

Minimum viable audit system — produces trustworthy findings.

- [ ] Rubric document with 4-dimension scoring + severity scheme — without this, nothing else has meaning
- [ ] Audit harness (Python + ruff + pyright + markdownlint + lychee + Pydantic frontmatter validator)
- [ ] Per-skill audit report format (markdown + JSON)
- [ ] Aggregated dashboard
- [ ] Fix-tracking schema (per-skill issue file with checkbox state)

### Add After Validation (v1.x — within Phase 3-4 of roadmap)

- [ ] LLM-as-judge for SKILL.md description quality (Discoverability dimension)
- [ ] Toy-example detector (Real-world Coverage)
- [ ] Cross-skill dependency graph + validation
- [ ] Pre-commit hooks to prevent regressions during fix waves

### Future Consideration (post-milestone)

- [ ] Synthetic-task triggering test suite (HIGH cost — defer until rubric proves stable)
- [ ] Per-domain methodology checklists (CONSORT/STROBE) — higher complexity, only if Academic Rigor failures cluster around methodology gaps
- [ ] CI workflow gating future skill submissions
- [ ] Versioning per skill (`version` + `last-verified` frontmatter fields)

## Feature Prioritization Matrix

| Feature | User Value | Implementation Cost | Priority |
|---------|------------|---------------------|----------|
| Rubric document | HIGH | LOW | P1 |
| Frontmatter schema validation | HIGH | LOW | P1 |
| marketplace ↔ disk reconciliation | HIGH | LOW | P1 (resolve gating issue) |
| Static lint pass (ruff + pyright) | HIGH | LOW | P1 |
| Markdown structural lint | MEDIUM | LOW | P1 |
| Per-skill audit report + dashboard | HIGH | MEDIUM | P1 |
| Fix-tracking state | HIGH | LOW | P1 |
| External link integrity (lychee) | HIGH | LOW | P1 |
| LLM-as-judge for description | HIGH | MEDIUM | P2 |
| Toy-example detector | MEDIUM | MEDIUM | P2 |
| Cross-skill dependency validation | MEDIUM | MEDIUM | P2 |
| API-key reconciliation | MEDIUM | MEDIUM | P2 |
| Pre-commit / CI guards | MEDIUM | LOW | P2 (only if scope allows) |
| Synthetic triggering tests | HIGH | HIGH | P3 (defer) |
| Per-domain methodology checklists | HIGH | HIGH | P3 (defer) |

**Priority key:**
- P1: Must have for v1 audit; without it the audit is unreliable
- P2: Should have, raises quality significantly without massive cost
- P3: Nice to have, defer until P1/P2 proven

## Sources

- `.planning/codebase/CONCERNS.md` — already-documented quality issues; treated as ground truth for what audit must catch
- `.planning/codebase/CONVENTIONS.md` — current SKILL.md structure → informs structural-lint rules
- `.planning/codebase/STACK.md` — existing Python script ecosystem
- Anthropic Claude Code skill spec — what makes skills well-formed
- agentskills.io spec (referenced by project) — frontmatter requirements

---
*Feature research for: Claude Scientific Skills Quality Audit*
*Researched: 2026-05-20*
