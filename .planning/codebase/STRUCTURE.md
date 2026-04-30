# Codebase Structure

**Analysis Date:** 2026-04-30

## Directory Layout

```
claude-scientific-skills/
├── .claude-plugin/
│   └── marketplace.json          # Plugin manifest: registers 142 skill paths
├── .github/
│   └── workflows/
│       └── release.yml           # CI: auto-release on marketplace.json version bump
├── docs/
│   ├── examples.md               # 23 real-world multi-skill workflow examples
│   ├── k-dense-web.gif           # Demo animation for README
│   ├── open-source-sponsors.md   # Open source acknowledgements
│   └── scientific-skills.md      # Master catalog of all skills with descriptions
├── reference/                    # Staging area: skills not yet published
│   ├── academic-reviewer/        #   SKILL.md only
│   ├── dspy/                     #   SKILL.md + references/
│   └── scientist/                #   SKILL.md + GUIDE.md + LICENSE.txt
├── scientific-skills/            # All published skills (67 directories on disk)
│   ├── aeon/                     #   Time series classification
│   ├── astropy/                  #   Astronomy computations
│   ├── biorxiv-database/         #   Preprint database access
│   ├── ...                       #   (64 more skill directories)
│   ├── document-skills/          #   Nested parent: contains sub-skills
│   │   ├── docx/                 #     Word document processing
│   │   ├── pdf/                  #     PDF manipulation
│   │   ├── pptx/                 #     PowerPoint processing
│   │   └── xlsx/                 #     Excel processing
│   └── ...
├── .gitignore                    # Ignores .claude/, temp/, .venv/, __pycache__/
├── LICENSE.md                    # MIT License, K-Dense Inc. 2025
└── README.md                     # Project overview, installation, skill catalog
```

## Directory Purposes

**`.claude-plugin/`:**
- Purpose: Plugin manifest that Claude Code reads to discover and load skills
- Contains: `marketplace.json` -- the single source of truth for plugin identity and skill registration
- Key file: `.claude-plugin/marketplace.json` (162 lines)
  - Declares plugin name (`scientific-skills`), owner (`K-Dense Inc.`), version (`2.17.0`)
  - Lists 142 skill paths as relative paths from repo root
  - Sets `strict: false` (allows partial skill loading)
  - Structure: `{ name, owner: { name, email }, metadata: { description, version }, plugins: [{ name, description, source, strict, skills: [] }] }`

**`.github/workflows/`:**
- Purpose: Automated release creation
- Contains: `release.yml` -- triggered on push to main when marketplace.json changes
- Key behavior: Extracts version from `metadata.version`, checks if git tag exists, generates changelog from commits, creates GitHub release via `softprops/action-gh-release@v1`

**`docs/`:**
- Purpose: Repository-level documentation for human readers (not loaded as skill context)
- Contains: 
  - `scientific-skills.md` (112KB) -- comprehensive catalog with descriptions for every skill category (databases, integrations, packages, analysis tools)
  - `examples.md` (116KB) -- 23 real-world workflow examples combining multiple skills across drug discovery, genomics, clinical research, materials science, etc.
  - `open-source-sponsors.md` (9.5KB) -- acknowledgements for open source projects referenced
  - `k-dense-web.gif` (23MB) -- demo animation

**`reference/`:**
- Purpose: Skills under development or staged for future publication
- Contains: 3 skill directories not registered in marketplace.json
- Key distinction from `scientific-skills/`: These are NOT discoverable by Claude's plugin system
- Structure: Same as published skills (SKILL.md + optional references/)

**`scientific-skills/`:**
- Purpose: All published skill content
- Contains: 67 directories on disk, but only 64 are registered in marketplace.json
- Key subdirectory: `document-skills/` is a parent directory containing 4 independently-registered sub-skills

## Skill Directory Anatomy

### Standard Skill (e.g., `scientific-skills/scikit-learn/`)

```
scikit-learn/
├── SKILL.md                     # Entry point (loaded by Claude)
├── references/                  # Deep documentation
│   ├── model_evaluation.md
│   ├── pipelines_and_composition.md
│   ├── preprocessing.md
│   ├── quick_reference.md
│   ├── supervised_learning.md
│   └── unsupervised_learning.md
└── scripts/                     # Executable Python examples
    ├── classification_pipeline.py
    └── clustering_analysis.py
```

### Skill with Assets (e.g., `scientific-skills/scientific-writing/`)

```
scientific-writing/
├── SKILL.md
├── references/
│   ├── citation_styles.md
│   ├── figures_tables.md
│   ├── imrad_structure.md
│   ├── professional_report_formatting.md
│   ├── reporting_guidelines.md
│   └── writing_principles.md
└── assets/
    ├── REPORT_FORMATTING_GUIDE.md
    ├── scientific_report.sty
    └── scientific_report_template.tex
```

### Minimal Skill (e.g., `scientific-skills/astropy/`)

```
astropy/
└── SKILL.md                     # All content in single file, no references/scripts/assets
```

### Nested Document Sub-Skill (e.g., `scientific-skills/document-skills/pdf/`)

```
document-skills/
├── docx/
│   ├── SKILL.md
│   ├── docx-js.md               # Additional reference at skill root level
│   ├── LICENSE.txt
│   ├── ooxml/                   # Deep nested structure for schemas
│   │   ├── schemas/             # XML Schema definitions (XSD files)
│   │   └── scripts/             # Schema validation tools
│   └── scripts/                 # Document manipulation scripts
│       ├── document.py
│       ├── utilities.py
│       └── templates/           # XML templates
├── pdf/
│   ├── SKILL.md
│   ├── forms.md                 # Additional reference at skill root level
│   ├── reference.md             # Additional reference at skill root level
│   ├── LICENSE.txt
│   └── scripts/                 # 8 Python scripts for PDF operations
├── pptx/
│   ├── SKILL.md
│   ├── html2pptx.md             # Additional reference at skill root level
│   ├── LICENSE.txt
│   ├── ooxml/                   # Same schema structure as docx
│   └── scripts/                 # JS and Python scripts for PPTX operations
└── xlsx/
    ├── SKILL.md
    ├── LICENSE.txt
    └── recalc.py                # Single script at skill root (no scripts/ dir)
```

## SKILL.md Frontmatter Format

Every SKILL.md begins with YAML frontmatter. Required and optional fields:

```yaml
---
name: skill-name                    # REQUIRED - matches directory name
description: Long description...    # REQUIRED - used for skill discovery by Claude
allowed-tools: [Read, Write, Edit, Bash]  # OPTIONAL - restricts available tools
license: MIT license                # REQUIRED - license identifier or "Unknown"
metadata:
    skill-author: K-Dense Inc.      # REQUIRED for published skills
    persona: Data Science Architect # OPTIONAL - role Claude should adopt
---
```

**Frontmatter observations across 62 on-disk skills:**
- All 62 have `name`, `description`, `license`
- 18 of 62 declare `allowed-tools` (mostly analysis/writing tools: `[Read, Write, Edit, Bash]`)
- All published skills have `metadata.skill-author: K-Dense Inc.`
- 1 skill has `metadata.persona` field (`general-data-science`)
- 1 reference skill has `version` field (`reference/scientist/SKILL.md`)

## File Naming Conventions

**Skill Directories:**
- Lowercase with hyphens: `scikit-learn`, `openalex-database`, `scientific-writing`
- Domain suffixes for categories: `*-database`, `*-integration`
- Compound names for tools: `torch_geometric` (underscore, matching PyPI name)

**SKILL.md:**
- Always uppercase `SKILL.md` -- the single entry point per skill

**Reference Files:**
- Lowercase with underscores: `model_evaluation.md`, `supervised_learning.md`
- Some use hyphens: `professional_report_formatting.md`

**Script Files:**
- Lowercase with underscores: `classification_pipeline.py`, `detect_resources.py`
- Match Python module conventions

**Asset Files:**
- Mixed conventions: `scientific_report.sty`, `REPORT_FORMATTING_GUIDE.md`, `project_init_ds.py`

## Key File Locations

**Entry Points:**
- `.claude-plugin/marketplace.json`: Plugin manifest -- Claude reads this to discover skills
- `scientific-skills/{name}/SKILL.md`: Per-skill entry point -- Claude loads this for context

**Configuration:**
- `.claude-plugin/marketplace.json`: Only configuration file; defines version, owner, skill list
- `.gitignore`: Excludes `.claude/`, `temp/`, `.venv/`, `__pycache__/`, `pyproject.toml`, `uv.lock`, `main.py`

**Core Content:**
- `scientific-skills/*/SKILL.md`: 62 skill entry points on disk
- `scientific-skills/*/references/*.md`: Deep reference documentation
- `docs/scientific-skills.md`: Master catalog (112KB) with descriptions of all skills
- `docs/examples.md`: Cross-skill workflow examples (116KB)

**CI/CD:**
- `.github/workflows/release.yml`: Single workflow for automated releases

## Where to Add New Code

**New Skill:**
1. Create directory: `scientific-skills/{skill-name}/`
2. Create `SKILL.md` with required frontmatter (`name`, `description`, `license`, `metadata.skill-author`)
3. Add `references/` directory with subtopic `.md` files if content exceeds ~200 lines
4. Add `scripts/` directory with Python example scripts if skill involves executable code
5. Add `assets/` directory if skill needs templates or static resources
6. Register path in `.claude-plugin/marketplace.json` under `plugins[0].skills` array

**New Nested Sub-Skill (like document-skills):**
1. Create subdirectory under parent: `scientific-skills/{parent}/{sub-skill}/`
2. Follow same SKILL.md pattern
3. Register with full path in marketplace.json: `./scientific-skills/{parent}/{sub-skill}`

**New Reference Skill (not yet published):**
1. Create directory: `reference/{skill-name}/`
2. Create SKILL.md
3. Do NOT add to marketplace.json until ready for publication
4. When ready, move to `scientific-skills/` and register in marketplace.json

**New Documentation:**
- Repository-level docs go in `docs/`
- Update `docs/scientific-skills.md` master catalog when adding new skills
- Update `README.md` skill count badges when adding new skills

## Special Directories

**`document-skills/` (Nested Skill Parent):**
- Purpose: Organizational parent for document format sub-skills
- Contains: 4 subdirectories (`docx/`, `pdf/`, `pptx/`, `xlsx/`), each a fully independent skill
- Unique: Has no SKILL.md of its own; not registered in marketplace.json
- Each sub-skill has its own LICENSE.txt (Proprietary, unlike MIT repo license)
- `docx/` and `pptx/` contain deep OOXML schema trees (`ooxml/schemas/`) with XSD files

**`reference/` (Staging Area):**
- Purpose: Skills under development before promotion to published set
- Contains: 3 skill directories (`scientist/`, `academic-reviewer/`, `dspy/`)
- Generated: No (manually created)
- Committed: Yes (tracked in git)
- Not registered in marketplace.json

**`docs/` (Human Documentation):**
- Purpose: Repository-level documentation for GitHub visitors and contributors
- Generated: No
- Committed: Yes

## Marketplace vs On-Disk Gap

The marketplace.json registers 142 skill paths. Only 67 directories exist on disk. This gap exists because:

**75 skills are registered but missing from disk (deleted in working tree):**
- 39 scientific package skills (e.g., `rdkit`, `scanpy`, `biopython`, `deepchem`)
- 22 database skills (e.g., `chembl-database`, `uniprot-database`, `pubchem-database`)
- 8 integration skills (e.g., `benchling-integration`, `opentrons-integration`)
- 6 other skills (e.g., `clinical-decision-support`, `iso-13485-certification`)

These files show `D` (deleted) status in git -- they exist in the repository history but are deleted in the current working tree.

**3 directories exist on disk but are NOT in marketplace.json:**
- `scientific-skills/computational-social-science/` -- not registered
- `scientific-skills/general-data-science/` -- not registered (has `allowed-tools` and `persona` metadata, appears to be a newer/development skill)
- `scientific-skills/document-skills/` -- parent directory not registered; its 4 sub-skills are individually registered

**`document-skills/` sub-skills count as 4 entries in marketplace.json but share 1 parent directory.**

## Statistics

| Metric | Count |
|--------|-------|
| Skills in marketplace.json | 142 |
| Directories on disk in scientific-skills/ | 67 |
| SKILL.md files on disk | 70 (62 in scientific-skills + 4 in document-skills + 3 in reference + 1 academic-reviewer) |
| Skills with references/ | 30 |
| Skills with scripts/ | 30 |
| Skills with assets/ | 17 |
| Skills with allowed-tools | 18 |
| Document sub-skills (nested) | 4 |
| Reference/staging skills | 3 |
| Skills missing from disk | 75 |
| On-disk directories not in marketplace | 3 |

---

*Structure analysis: 2026-04-30*
