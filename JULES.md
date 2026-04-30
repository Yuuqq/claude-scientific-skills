# Jules Instructions -- Claude Scientific Skills

You are working on **claude-scientific-skills**, a repository of 70 Claude Code skills for scientific research. Your role is to create, improve, and maintain these skills.

## What This Repository Is

- **Not a software project.** This is a content/documentation repository. There is no runtime code, no build system, no tests, no dependencies.
- Each skill is a self-contained knowledge bundle under `scientific-skills/<name>/` that Claude Code loads as context.
- The marketplace manifest at `.claude-plugin/marketplace.json` registers all skills.
- A GitHub Pages site at `docs/index.html` provides a browsable catalog.

## Repository Structure

```
.claude-plugin/marketplace.json   # Skill registry (source of truth for publishing)
scientific-skills/<name>/         # Skill directories
  SKILL.md                        # Main entry point (required)
  references/*.md                 # Detailed reference docs (optional)
  scripts/*.py                    # Example Python scripts (optional)
  assets/*                        # Images, diagrams (optional)
docs/
  index.html                      # GitHub Pages catalog
  skills.json                     # Generated skill metadata
scripts/
  generate_skills_data.py         # Regenerates skills.json from SKILL.md
.planning/                        # GSD project planning (do not modify unless asked)
```

## Skill Anatomy

Every skill MUST have a `SKILL.md` with this structure:

### Frontmatter (required)

```yaml
---
name: skill-name
description: One-line description of what the skill does and when to use it.
license: MIT license
metadata:
    skill-author: K-Dense Inc.
---
```

### Document Sections (required)

```markdown
# Skill Name

## Overview
2-3 paragraphs explaining what the skill/tool is.

## When to Use This Skill
Bullet list of specific scenarios. Also mention when NOT to use it
and which alternative skill to use instead.

## Core Concepts
Key concepts, API patterns, or domain knowledge needed.

## [Domain-Specific Sections]
As needed: Installation, Configuration, Data Formats, etc.

## Code Examples
Practical, runnable examples. Each example should:
- Have a clear title
- Show imports
- Include comments for non-obvious steps
- Be self-contained (assume user has the package installed)

## Best Practices
Do's and don'ts specific to this tool/domain.

## Common Pitfalls
Known issues, gotchas, workarounds.

## References
Links to official documentation, papers, tutorials.
```

## Quality Standards

### Minimum for a new skill:
- SKILL.md: 300+ lines with all required sections
- Description: specific, actionable (not "This skill does X")
- At least 3 code examples covering common use cases
- "When to Use" must name alternative skills for cases where this one is wrong

### Target for a mature skill:
- SKILL.md: 500+ lines
- references/: 3-5 reference documents
- scripts/: 1-3 runnable example scripts
- Cross-references to related skills in the collection

### Description style guide:
- BAD: "This skill should be used for machine learning tasks"
- GOOD: "Machine learning with scikit-learn. Use for classification, regression, clustering, preprocessing, and model evaluation. For deep learning use pytorch-lightning; for time series use aeon."

## When Making Changes

### Adding a new skill:
1. Create `scientific-skills/<name>/SKILL.md` following the template above
2. Add `references/` documents if the skill is complex
3. Add `scripts/` if the skill involves setup or multi-step workflows
4. Register in `.claude-plugin/marketplace.json` (add path to `skills` array)
5. Run `python scripts/generate_skills_data.py` to update the catalog
6. Keep descriptions under 300 characters when possible

### Improving an existing skill:
1. Read the current SKILL.md fully before editing
2. Preserve the frontmatter format exactly
3. Add missing sections rather than rewriting existing content
4. Test any code examples you add (verify API names, import paths)
5. Cross-reference to other skills where relevant

### Fixing issues:
- Outdated API references: verify against official docs before updating
- Missing examples: add practical, runnable examples
- Cross-reference gaps: mention related skills in "When to Use"

## What NOT To Do

- Do NOT add a build system, package.json, pyproject.toml, or similar
- Do NOT add automated tests (this is a content repo, not software)
- Do NOT add CI/CD workflows for content validation
- Do NOT change the directory structure
- Do NOT remove the `reference/` directory (contains external reference materials)
- Do NOT modify files outside `scientific-skills/` unless specifically asked
- Do NOT use emojis in SKILL.md files

## Current State Summary

| Metric | Value |
|--------|-------|
| Total skills | 70 |
| With references | 62/70 |
| With scripts | 34/70 |
| With assets | 17/70 |
| Categories | 15 |
| Shortest SKILL.md | 21 lines (offer-k-dense-web) |
| Longest SKILL.md | 1,155 lines (scientific-slides) |
| Median SKILL.md | ~400 lines |

## Regenerating the Catalog

After any skill changes, regenerate the data file:

```bash
python scripts/generate_skills_data.py
```

This updates `docs/skills.json` which powers the GitHub Pages catalog.

## Commit Conventions

Use conventional commits:
- `feat: add <skill-name> skill` -- new skill
- `docs: improve <skill-name>` -- documentation improvement
- `fix: correct <skill-name> API reference` -- factual fixes
- `chore: update skills.json` -- catalog regeneration

One logical change per commit. Do not bundle unrelated skill changes.
