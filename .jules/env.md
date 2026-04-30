# Jules Environment Setup

Instructions for humans configuring Google Jules to work on this repository.

## What Jules Will Do

Jules will create, edit, and improve skill documentation files (`SKILL.md`, references, scripts). It does NOT need Python, build tools, or test frameworks -- this is a pure content repository.

## Repository Access

1. Fork or own the repository: `Yuuqq/claude-scientific-skills`
2. Ensure Jules has write access to the repository via GitHub integration

## Environment Requirements

### Runtime
- **Language:** None required (Markdown content only)
- **Python:** 3.12+ (only for `scripts/generate_skills_data.py` to regenerate catalog)
- **Build system:** None

### Tools Jules Should Have Access To
- File read/write (for SKILL.md, references, scripts)
- Shell (for running `python scripts/generate_skills_data.py`)
- Git (for commits)

### No Special Dependencies
This repo has no `requirements.txt`, `package.json`, or build config. Jules should NOT attempt to install any packages or run any build commands.

## Jules Configuration

### Repository Settings

```
Repository: Yuuqq/claude-scientific-skills
Branch: main
Working directory: /
```

### Instructions File

The main instructions are in `JULES.md` at the repository root. Jules should read this file at the start of every session.

### Key Files Jules Will Edit

| File Pattern | Purpose |
|-------------|---------|
| `scientific-skills/*/SKILL.md` | Main skill documentation |
| `scientific-skills/*/references/*.md` | Reference documents |
| `scientific-skills/*/scripts/*.py` | Example Python scripts |
| `.claude-plugin/marketplace.json` | Skill registry (add new skills) |
| `docs/skills.json` | Catalog data (regenerated) |

### Files Jules Should NOT Edit

| File | Reason |
|------|--------|
| `docs/index.html` | GitHub Pages site (edit separately if needed) |
| `.planning/*` | GSD project planning artifacts |
| `README.md` | Top-level docs (edit separately if needed) |
| `LICENSE.md` | Legal -- do not modify |

## Typical Jules Tasks

### Task: Improve a skill
```
Read scientific-skills/<name>/SKILL.md and improve it to production quality.
Follow the skill template in JULES.md. Add missing sections, expand examples,
create reference documents. Target 500+ lines.
```

### Task: Add a new skill
```
Create a new skill for <library-name>. Follow the skill template in JULES.md.
Create SKILL.md, references/, scripts/. Register in marketplace.json.
Run python scripts/generate_skills_data.py to update the catalog.
```

### Task: Fix factual errors
```
The API reference in scientific-skills/<name>/references/api_reference.md
contains outdated information. Verify against official docs and update.
```

### Task: Regenerate catalog
```
Run python scripts/generate_skills_data.py to regenerate docs/skills.json.
Commit the updated file.
```

## Post-Jules Verification

After Jules completes a task:

1. **Check the diff:** `git diff` -- verify changes look correct
2. **Regenerate catalog:** `python scripts/generate_skills_data.py`
3. **Preview locally:** Open `docs/index.html` in a browser
4. **Commit and push:** `git add -A && git commit && git push`

## Environment Variables

None required. No API keys, tokens, or secrets are needed for skill development.

If a skill references external APIs that need keys (e.g., Perplexity search needs OpenRouter), document this in the skill's SKILL.md but do NOT store actual keys in the repository.

## Troubleshooting

**Jules tries to install Python packages:**
Tell it this is a content repository. No packages to install. Read JULES.md.

**Jules tries to run tests:**
There are no tests. This is documentation. Read JULES.md.

**Jules modifies planning files:**
Stop it. Planning files are managed by GSD workflows, not Jules.

**skills.json is out of date:**
Run: `python scripts/generate_skills_data.py`
