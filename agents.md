# Agent Configuration

## Repository Type

This is a **content/documentation repository**, not a software project. There is no runtime code, no build system, no test framework, no dependencies.

## Environment

- **Language:** Markdown (primary), Python (scripts only)
- **Build:** None
- **Tests:** None
- **Dependencies:** None to install
- **Python:** Available for `scripts/generate_skills_data.py` only

## Instructions

Read `JULES.md` at the start of every session. It contains all conventions, templates, and quality standards.

## After Making Changes

Run the catalog generator if any SKILL.md files were modified:

```bash
python scripts/generate_skills_data.py
```

## Do Not

- Install packages (there are none to install)
- Run tests (there are none)
- Modify `.planning/` directory
- Modify `JULES.md` or `.jules/` (human-managed)
- Add build configuration files
