# Architecture

**Analysis Date:** 2026-04-30

## Pattern Overview

**Overall:** Declarative Plugin Architecture (Content-as-Code)

**Key Characteristics:**
- No runtime or compiled software -- this is a pure documentation/content repository
- Skills are self-contained context units that Claude loads as prompt context
- A marketplace manifest (`marketplace.json`) declares available skills; Claude discovers and loads them on demand
- Each skill is an isolated knowledge bundle with a standardized directory structure
- Skills cross-reference each other via prose mentions in SKILL.md descriptions, not through an import/dependency system

## How Claude Loads Skills

The loading chain follows this path:

```
marketplace.json (manifest)
  |
  +--> skill path (e.g., ./scientific-skills/scikit-learn)
         |
         +--> SKILL.md (entry point, loaded first)
                |
                +--> references/*.md (sub-documents, loaded on demand by Claude)
                |
                +--> scripts/*.py (executable code, referenced in SKILL.md examples)
                |
                +--> assets/* (templates, images, LaTeX files)
```

1. Claude Code plugin system reads `.claude-plugin/marketplace.json`
2. When a user describes a scientific task, Claude matches it against skill `description` fields in the YAML frontmatter
3. Claude loads the matching `SKILL.md` file as context
4. `SKILL.md` references sub-documents in `references/` and scripts in `scripts/` -- Claude loads these as needed
5. Claude uses the loaded context to generate code, explanations, and workflows

There is no programmatic dispatch, no event bus, and no runtime execution framework. The architecture is purely **declarative**: markdown files define what Claude should know, and Claude's LLM capabilities handle the rest.

## Skill Composition Pattern

Every skill follows the same compositional structure:

**Layer 1 -- SKILL.md (Entry Point):**
- YAML frontmatter: `name`, `description`, `license`, `metadata.skill-author`, optionally `allowed-tools`
- Overview section: what the skill does
- Installation section: `uv pip install` commands
- "When to Use This Skill" section: triggers for Claude to activate this skill
- Quick Start section: runnable code examples
- References to `references/` sub-documents for deeper content

**Layer 2 -- references/ (Deep Documentation):**
- Multiple `.md` files covering specialized subtopics
- Example: `scikit-learn/references/` has `supervised_learning.md`, `unsupervised_learning.md`, `model_evaluation.md`, `preprocessing.md`, `pipelines_and_composition.md`, `quick_reference.md`
- Not all skills have references -- some have all content in SKILL.md

**Layer 3 -- scripts/ (Executable Examples):**
- Python scripts demonstrating real usage patterns
- Example: `scikit-learn/scripts/classification_pipeline.py`, `scikit-learn/scripts/clustering_analysis.py`
- Not all skills have scripts -- many are documentation-only

**Layer 4 -- assets/ (Static Resources):**
- LaTeX templates, formatting guides, images, project scaffolding scripts
- Example: `scientific-writing/assets/scientific_report_template.tex`, `scientific-writing/assets/scientific_report.sty`
- Present in 17 of 67 on-disk skill directories

## Layers

**Plugin Manifest:**
- Purpose: Registers all skills with Claude's plugin system; defines version, metadata, and skill paths
- Location: `.claude-plugin/marketplace.json`
- Contains: Plugin name, owner info, version string, array of skill directory paths
- Depends on: Nothing (standalone JSON)
- Used by: Claude Code plugin infrastructure

**Skill Content (scientific-skills/):**
- Purpose: All skill documentation, scripts, and assets
- Location: `scientific-skills/`
- Contains: 67 directories on disk (of 142 registered in marketplace)
- Depends on: Nothing (self-contained content)
- Used by: Claude Code when loading a skill as context

**Documentation (docs/):**
- Purpose: Repository-level documentation for humans (not loaded as skill context)
- Location: `docs/`
- Contains: `scientific-skills.md` (master skill catalog), `examples.md` (cross-skill workflow examples), `open-source-sponsors.md`, `k-dense-web.gif`
- Depends on: Nothing
- Used by: GitHub README readers, contributors

**Reference Skills (reference/):**
- Purpose: Skills under development or not yet promoted to the published skill set
- Location: `reference/`
- Contains: 3 skill directories (`scientist`, `academic-reviewer`, `dspy`)
- Depends on: Nothing
- Used by: Not referenced by marketplace.json -- development/staging area

**CI/CD:**
- Purpose: Automated release creation when marketplace.json version changes
- Location: `.github/workflows/release.yml`
- Contains: Single workflow that extracts version from marketplace.json, generates changelog, creates GitHub release with tag
- Depends on: `marketplace.json` (triggers on version change)
- Used by: GitHub Actions

## Data Flow

**Skill Discovery and Activation:**

1. User installs plugin via `/plugin install scientific-skills@claude-scientific-skills`
2. Claude Code reads `marketplace.json` and indexes all 142 skill paths
3. User describes a scientific task in natural language
4. Claude matches task description against `description` frontmatter fields in each SKILL.md
5. Claude loads the matched SKILL.md into context
6. Claude references `references/` sub-documents and `scripts/` as needed
7. Claude generates code, analysis, or documentation using the loaded context

**Skill Cross-Referencing:**

Skills reference each other in prose, not through an import system:
- `scientific-writing/SKILL.md` references `scientific-schematics` for diagram generation
- `peer-review/SKILL.md` references `scientific-schematics` for visual enhancement
- `pdf/SKILL.md` references `scientific-schematics` for document diagrams
- `hypothesis-generation/SKILL.md` references `scientific-brainstorming` and `hypogenic` as alternatives
- Many database skills reference package skills (e.g., ChEMBL references RDKit)

This cross-referencing is **implicit** -- Claude determines when to load a referenced skill based on the mention in context.

**State Management:**
- No persistent state between skill invocations
- Each skill load is independent
- `get-available-resources` skill creates a JSON file on disk as the only stateful artifact

## Key Abstractions

**Skill (Core Unit):**
- Purpose: A self-contained knowledge bundle for one scientific domain or tool
- Examples: `scientific-skills/scikit-learn/`, `scientific-skills/openalex-database/`, `scientific-skills/scientific-writing/`
- Pattern: Directory containing SKILL.md + optional references/ + optional scripts/ + optional assets/

**Skill Category (Logical Grouping):**
- Purpose: Groups skills by scientific domain (not enforced at filesystem level)
- Examples: Scientific Databases (`*-database`), Python Packages (library names), Integrations (`*-integration`), Analysis & Communication tools
- Pattern: Naming convention only -- no category directories or manifest grouping

**Document Sub-Skill (Nested Skill):**
- Purpose: Skills that share a parent directory for organizational grouping
- Examples: `document-skills/docx/`, `document-skills/pdf/`, `document-skills/pptx/`, `document-skills/xlsx/`
- Pattern: Parent directory (`document-skills/`) contains no SKILL.md; each subdirectory is independently registered in marketplace.json

**Cross-Skill Composition:**
- Purpose: Combining multiple skills for complex workflows
- Examples: Documented in `docs/examples.md` (23 real-world multi-skill workflow examples)
- Pattern: Skills mention each other by name in descriptions and documentation; Claude composes them at runtime

## Entry Points

**Plugin Manifest:**
- Location: `.claude-plugin/marketplace.json`
- Triggers: Claude Code plugin system on install/load
- Responsibilities: Declare plugin identity (name, owner, version), enumerate all skill paths, set `strict: false` mode

**Individual SKILL.md:**
- Location: `scientific-skills/{skill-name}/SKILL.md`
- Triggers: Claude matching user task to skill description
- Responsibilities: Provide frontmatter for discovery, overview for understanding, examples for code generation, references for deep context

**Release Workflow:**
- Location: `.github/workflows/release.yml`
- Triggers: Push to `main` that modifies `.claude-plugin/marketplace.json`, or manual `workflow_dispatch`
- Responsibilities: Extract version, check for existing tag, generate changelog, create GitHub release

## Error Handling

**Strategy:** No programmatic error handling -- this is a content repository. The only "runtime" is the CI workflow.

**CI Workflow Patterns:**
- Tag existence check prevents duplicate releases (`check_tag` step)
- Graceful handling when no previous tag exists (initial release)
- Version extraction uses `jq` with `marketplace.json` as source of truth

## Cross-Cutting Concerns

**Skill Discovery:** Claude matches user intent against `description` frontmatter fields. The `description` field is the primary discovery mechanism -- it must include both what the skill does AND when to use it.

**License Tracking:** Each skill declares its own license in frontmatter. Skills use a mix of MIT, BSD-3-Clause, Apache-2.0, Unknown, and Proprietary licenses.

**Authorship:** All published skills declare `metadata.skill-author: K-Dense Inc.` in frontmatter.

**Tool Restrictions:** 18 of 62 on-disk skills declare `allowed-tools` in frontmatter (e.g., `[Read, Write, Edit, Bash]`), restricting which Claude Code tools the skill can invoke.

---

*Architecture analysis: 2026-04-30*
