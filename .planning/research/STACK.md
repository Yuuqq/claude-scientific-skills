# Stack Research

**Domain:** Quality auditing & remediation of Claude Code skill libraries (markdown-driven prompt-context bundles + Python helper scripts)
**Researched:** 2026-05-20
**Confidence:** MEDIUM (toolchain choices well-established; LLM-as-judge tooling emerging)

## Recommended Stack

### Core Technologies

| Technology | Version | Purpose | Why Recommended |
|------------|---------|---------|-----------------|
| Python 3.12+ | 3.12.x | Audit harness language; matches existing scripts/ language | Already the lingua franca of the repo (106 Python files); avoids introducing new language dependencies |
| ruff | 0.5+ | Static lint/format for Python scripts in scripts/ | Single binary, replaces flake8/pylint/black/isort; ~100x faster; default rules catch import issues, syntax errors, unused vars — exactly what static-only audit needs |
| pyright (or mypy --strict) | pyright 1.1.x / mypy 1.10+ | Static type checking for scripts/ | Catches API misuse without execution; pyright is faster, mypy has wider ecosystem |
| markdownlint-cli2 | 0.13+ | Markdown structural lint for SKILL.md / references/ | Catches broken headings, missing alt text, inconsistent list markers — supports custom rule config |
| Vale | 3.0+ | Prose quality + style checking | Open-source, configurable rule packs (write-good, alex, custom academic style); essential for "Academic Rigor" dimension |
| pyyaml | 6.0+ | Parse SKILL.md frontmatter | Standard library — no new dependency added |
| Pydantic | 2.x | Validate frontmatter against schema | Declarative schema → catches "Unknown" license, missing fields, format inconsistency |

### Supporting Libraries / Tools

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| jsonschema | 4.x | Validate marketplace.json structure & per-skill schemas | Audit dimension: structural integrity |
| linkchecker (or lychee) | lychee 0.15+ | Check broken external links in SKILL.md and references/*.md | Cite-rot detection (Academic Rigor); lychee is Rust-based, fast, supports concurrency |
| Anthropic SDK | latest | LLM-as-judge for Discoverability dimension (description quality) | Programmatic critique of SKILL.md descriptions vs synthetic user prompts |
| Click or Typer | 8.x / 0.12+ | CLI for the audit harness | Each audit step exposed as a subcommand for selective re-run |
| Jinja2 | 3.x | Render audit reports from data | Single source of truth → markdown reports + dashboard |
| GitHub Actions | n/a | CI gate enforcing rubric compliance after fixes | Currently only release.yml exists; need a quality.yml workflow |

### Development Tools

| Tool | Purpose | Notes |
|------|---------|-------|
| `uv` (Astral) | Python package management for the audit harness itself | Already the project's documented choice; respect convention |
| pre-commit | Hook framework for running ruff / markdownlint / vale on staged changes | Prevents quality regressions after fixes ship |
| `cspell` (optional) | Spell check across markdown content | Helps Academic Rigor — catches "Worflows" type typos that exist today |

## Per-Tool Rationale Mapped to 4 Rubric Dimensions

| Rubric Dimension | Primary Tool | Secondary Tool | What It Catches |
|------------------|--------------|----------------|-----------------|
| **Academic Rigor** | Vale (custom academic style pack) | lychee (link rot), cspell | Imprecise language, dead citations, terminology errors, weasel words |
| **Real-world Coverage** | LLM-as-judge (Claude SDK) | Manual sampling of scripts/ | Detects toy examples (`np.random.rand(100)`), missing edge cases, lack of domain realism |
| **Discoverability** | LLM-as-judge against synthetic prompts | markdownlint (structural) | Tests if SKILL.md description triggers correctly given a user task; checks "When to Use" clarity |
| **Runnability (static)** | ruff + pyright | jsonschema (frontmatter) | Syntax errors, broken imports, type misuse, undeclared API key requirements |

## Installation

```bash
# Audit harness (single uv project at repo root)
uv init audit/ --no-readme
cd audit
uv add ruff pyright markdownlint-cli2 vale pyyaml pydantic jsonschema lychee anthropic click jinja2

# Or as a global toolset (pre-commit only)
uv tool install ruff
uv tool install pyright
npm install -g markdownlint-cli2  # markdownlint is npm-only currently
# Vale: brew install vale (macOS) / scoop install vale (Win) / cargo install for Linux
# lychee: cargo install lychee
```

## Alternatives Considered

| Recommended | Alternative | When to Use Alternative |
|-------------|-------------|-------------------------|
| ruff | flake8 + black + isort + bandit | If team is allergic to all-in-one tooling — but ruff is now the de facto choice in 2025 |
| pyright | mypy | If you need plugins (Django, SQLAlchemy stubs) — but our scripts are mostly stdlib + numpy/pandas |
| Vale | proselint | proselint is Python-only and has a narrower rule set; Vale supports custom academic style packs |
| LLM-as-judge (Claude) | LLM-as-judge (GPT-4 / Gemini) | If cross-LLM agreement matters; can run multiple in ensemble for higher confidence |
| markdownlint-cli2 | remark-lint | Both work; markdownlint-cli2 has simpler config, remark has richer plugin ecosystem |
| lychee | linkchecker | lychee is faster (Rust, concurrent); linkchecker has older Python ecosystem |

## What NOT to Use

| Avoid | Why | Use Instead |
|-------|-----|-------------|
| Running scripts/ in real environments | User explicitly chose "static check only" — execution adds dependency-management cost & flakiness | ruff + pyright catch the high-value issues without execution |
| pylint | 10× slower than ruff, weaker default rule set, deprecated in many 2025 toolchains | ruff |
| Pure regex audits in bash | Brittle, hard to maintain, can't validate semantics | Use AST-based tooling (ruff, pyright) where possible |
| GPT-3.5 for LLM-as-judge | Insufficient reasoning for "would this trigger correctly?" type judgments | Claude Sonnet/Opus or GPT-4-class models |
| Generic "good prose" linters with no academic profile | Will flag domain-correct technical phrasing as "passive voice" / "complex" | Vale with a custom academic style pack — domain-aware |
| Branch-based review-then-merge per-skill workflow | 67 skills × manual review = bottleneck; user chose Claude-auto + spot-check mode | Batch-fix per audit category, single PR per fix wave |

## Stack Patterns by Variant

**If the audit harness is one-shot (run once, throw away):**
- Skip pre-commit and CI integration — just produce reports
- Reduces tooling sprawl

**If the harness becomes ongoing infrastructure (recommended):**
- Wire ruff + markdownlint + vale into pre-commit + GitHub Actions
- Lock the rubric so future skill submissions can't regress

**If LLM-as-judge confidence is critical (high-stakes Discoverability checks):**
- Use ensemble (Claude + GPT-4) and require agreement
- Otherwise single-model judge is sufficient for triage

## Version Compatibility

| Package A | Compatible With | Notes |
|-----------|-----------------|-------|
| Python 3.12 | ruff 0.5+, pyright 1.1.x, pydantic 2.x | All current; ruff drops py37 support — fine for us |
| markdownlint-cli2 | Node.js 18+ | Add Node to dev requirements; document in audit/README |
| Vale 3.x | None of the project's existing deps | Standalone binary — zero risk |
| lychee 0.15+ | Rust toolchain not required (prebuilt binaries) | Use prebuilt on CI |

## Sources

- Anthropic Claude Code skill marketplace docs (2025) — frontmatter schema reference
- Astral ruff documentation (https://docs.astral.sh/ruff/) — current best-practice Python linting
- Vale documentation (https://vale.sh) — academic style pack examples
- Existing project's STACK.md, CONVENTIONS.md, CONCERNS.md — already-known issues + conventions
- agentskills.io specification — referenced by current STACK.md as the spec our skills follow

---
*Stack research for: Claude Scientific Skills Quality Audit*
*Researched: 2026-05-20*
