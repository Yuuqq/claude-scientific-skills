# Contributing

Thanks for helping researchers get trustworthy AI skills. This repository holds itself to a simple bar: **every skill must be something a researcher can rely on in real work**. Contributions are validated automatically in CI; this guide tells you how to pass on the first try.

## Repository Layout

```
scientific-skills/<skill-name>/
  SKILL.md          # Main entry point (required)
  references/       # Detailed reference docs (optional)
  scripts/          # Runnable example scripts (optional)
  assets/           # Images, diagrams (optional)
.claude-plugin/marketplace.json   # Skill registry
docs/skills.json                  # Generated catalog (do not edit by hand)
scripts/validate_skills.py        # The CI quality gate
```

## Adding a New Skill

1. Create `scientific-skills/<skill-name>/SKILL.md` with this frontmatter:

```yaml
---
name: skill-name            # must match the directory name exactly
description: What it does and when to use it. Name alternatives for cases it does not cover.
license: MIT license        # or the license of the upstream tool docs
metadata:
    skill-author: Your Name
---
```

2. Follow the standard section order: Overview, When to Use This Skill, Core Concepts, Code Examples, Best Practices, Common Pitfalls, References.
3. Register the skill: add `"./scientific-skills/<skill-name>"` to `.claude-plugin/marketplace.json`.
4. Regenerate the catalog:

```bash
python scripts/generate_skills_data.py
```

5. Validate before pushing:

```bash
pip install pyyaml
python scripts/validate_skills.py
```

## Quality Bar

- **Descriptions decide discoverability.** The agent picks skills by description. Write what the skill does, when to use it, and what to use instead. Bad: "This skill should be used for machine learning tasks." Good: "Machine learning with scikit-learn. Use for classification, regression, clustering, model evaluation. For deep learning use pytorch-lightning; for time series use aeon."
- **Code examples must be real.** Verify import paths and API names against the current release of the library. No pseudo-APIs, no invented functions.
- **Name the failure modes.** A Common Pitfalls section that saves a researcher an afternoon is worth more than three extra examples.
- **300+ lines for a new skill**, all required sections present. Mature skills target 500+ lines with 3-5 reference docs.
- **No vendor promotion.** Skills must not steer users toward commercial platforms. CI rejects this automatically.

## What CI Checks

Every push and pull request runs `scripts/validate_skills.py`:

- SKILL.md exists and frontmatter parses with `name`, `description`, `license`
- Frontmatter name matches the directory name
- Relative links resolve to real files
- Python scripts pass a syntax check and error-level ruff rules
- Every skill on disk is registered in `marketplace.json` and vice versa
- `docs/skills.json` is in sync with the skills on disk
- No vendor-promotion content

A weekly scheduled job also checks all external links for rot.

## Fixing an Existing Skill

Factual fixes (wrong API names, outdated function signatures, dead links) are the most valuable contributions. Verify against official documentation, link the source in the PR description, and keep one logical fix per PR.

## Commit Style

Conventional commits, one logical change per commit:

- `feat: add <skill-name> skill`
- `docs: improve <skill-name>`
- `fix: correct <skill-name> API reference`
- `chore: update skills.json`
