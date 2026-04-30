# Jules Environment Setup

Instructions for humans configuring Google Jules to work on this repository.

---

## Setup Script

**Copy this into the Jules "Setup script" field in the repository settings:**

```bash
bash .jules/setup.sh
```

This script:
1. Verifies the repo structure is correct
2. Checks Python availability (needed for catalog regeneration)
3. Counts and validates all skill directories
4. Regenerates `docs/skills.json` from SKILL.md files
5. Prints a summary of the environment

The script runs once on first setup, then the environment is snapshotted for faster subsequent startups.

---

## What This Repo Needs

| Component | Required? | Why |
|-----------|-----------|-----|
| Python 3.12+ | Optional | Only for `scripts/generate_skills_data.py` |
| Node.js | No | Not a JS project |
| pip/uv | No | No packages to install |
| Build tools | No | No build step |

**This is a pure content/documentation repository.** Jules will only edit Markdown files and occasionally run the Python catalog generator.

---

## How Jules Should Work

### Jules reads these files automatically:
- `JULES.md` -- main instructions (read this first every session)
- `agents.md` -- additional agent configuration hints

### Jules edits these files:
| Pattern | Purpose |
|---------|---------|
| `scientific-skills/*/SKILL.md` | Skill documentation |
| `scientific-skills/*/references/*.md` | Reference docs |
| `scientific-skills/*/scripts/*.py` | Example scripts |
| `.claude-plugin/marketplace.json` | Skill registry |
| `docs/skills.json` | Catalog data (regenerated via script) |

### Jules must NOT edit:
| Pattern | Reason |
|---------|--------|
| `.planning/*` | Managed by GSD workflows |
| `.jules/*` | Managed by humans |
| `JULES.md` | Instruction file -- human-controlled |
| `LICENSE.md` | Legal |

---

## Typical Task Templates

### Improve a skill
```
Improve scientific-skills/<name>/SKILL.md to production quality.
Read JULES.md first. Current state: N lines. Target: 500+ lines.
Add missing sections per the template. Run python scripts/generate_skills_data.py after.
```

### Add a new skill
```
Create skill for <library-name>. Read JULES.md for template.
Create scientific-skills/<name>/SKILL.md + references/ + scripts/.
Register in .claude-plugin/marketplace.json.
Run python scripts/generate_skills_data.py.
```

### Batch improvement (use DEVELOPMENT-PLAN.md)
```
Read DEVELOPMENT-PLAN.md Phase 2. Improve all Tier D skills
to Tier C minimum. One skill per commit. Run catalog script after each.
```

---

## Post-Jules Verification

After Jules creates a PR:

1. `git diff` -- check changes
2. `python scripts/generate_skills_data.py` -- regenerate catalog
3. Open `docs/index.html` locally -- verify catalog
4. Merge PR

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Jules tries to install packages | Remind it: "This is a content repo. Read JULES.md." |
| Jules tries to run tests | "No tests exist. Read JULES.md." |
| Jules edits planning files | "Do not touch .planning/. Read JULES.md." |
| skills.json stale | Run: `python scripts/generate_skills_data.py` |
| Setup script fails | Check Python is available; content editing still works without it |
