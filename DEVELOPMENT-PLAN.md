# Skill Development Plan

Iterative plan for developing all 70 skills to their final, production-quality form.

## Final Skill Form

A production-quality skill meets all of these criteria:

### Structure
```
scientific-skills/<name>/
  SKILL.md                    # 500+ lines, all sections present
  references/
    api_reference.md          # Complete API/function reference
    examples.md               # Extended examples with explanations
    best_practices.md         # Do's, don'ts, patterns
    [domain_specific].md      # Additional domain docs as needed
  scripts/
    basic_usage.py            # Minimal working example
    advanced_workflow.py      # Multi-step realistic workflow
  assets/
    [diagrams or images]      # Visual aids where helpful
```

### SKILL.md Sections (all required)

| Section | Target | Description |
|---------|--------|-------------|
| Frontmatter | -- | name, description, license, metadata |
| Overview | 2-3 paragraphs | What it is, who made it, why it matters |
| When to Use | 10-15 bullets | Specific scenarios + when NOT to use + alternatives |
| Core Concepts | Varies | Key abstractions, mental model, architecture |
| Installation | 5-10 lines | uv pip install + any system deps |
| Code Examples | 5-8 examples | Progressive complexity: basic -> intermediate -> advanced |
| Best Practices | 8-12 bullets | Domain-specific guidance |
| Common Pitfalls | 5-8 items | Known issues with workarounds |
| References | Links | Official docs, papers, tutorials |

### Description Quality

Every description must answer three questions in one sentence:
1. **What** does this tool do?
2. **When** should I use it?
3. **What else** should I consider instead?

---

## Phase 1: Gap Analysis & Triage

**Goal:** Categorize all 70 skills by current quality level.

### Quality Tiers

| Tier | Criteria | Action |
|------|----------|--------|
| A (Production) | 500+ lines, 3+ refs, 2+ scripts, all sections | Light polish only |
| B (Good) | 300-500 lines, 1+ refs, most sections | Add missing sections |
| C (Basic) | 150-300 lines, few sections | Significant rewrite |
| D (Skeleton) | <150 lines or missing key sections | Build from scratch |

### Current Distribution (estimated)

| Tier | Count | Skills |
|------|-------|--------|
| A | ~15 | scientific-slides, citation-management, research-grants, venue-templates, pymatgen, etc. |
| B | ~25 | scikit-learn, aeon, matplotlib, polars, qiskit, etc. |
| C | ~20 | transformers, pytorch-lightning, vaex, pennylane, etc. |
| D | ~10 | general-data-science, document-skills/*, etc. |

### Deliverable
- [ ] Audit every SKILL.md and assign tier
- [ ] Prioritize Tier D and C skills for immediate work

---

## Phase 2: Tier D Skills -- Build Foundations

**Goal:** Bring 10 skeleton skills to Tier C minimum.

### Target Skills
- general-data-science (91 lines)
- document-skills/docx, pdf, pptx, xlsx
- transformers (163 lines)
- pytorch-lightning (173 lines)
- vaex (181 lines)
- generate-image (184 lines)
- scientific-brainstorming (190 lines)
- denario (214 lines)

### Per-Skill Work
1. Write complete SKILL.md with all required sections
2. Create `references/api_reference.md`
3. Create `scripts/basic_usage.py`
4. Update description to match quality standard

### Acceptance Criteria
- [ ] All Tier D skills have 300+ line SKILL.md
- [ ] All have at least 1 reference document
- [ ] All have at least 1 example script
- [ ] Descriptions follow the three-question format

---

## Phase 3: Tier C Skills -- Fill Content Gaps

**Goal:** Bring 20 basic skills to Tier B.

### Target Skills (examples)
- geopandas, datacommons-client, plotly, qiskit, get-available-resources
- pennylane, pufferlib, stable-baselines3, torch_geometric
- sympy, astropy, simpy, modal

### Per-Skill Work
1. Add missing sections (Common Pitfalls, Best Practices, Installation)
2. Expand code examples to 4-6 per skill
3. Create `references/examples.md` and `references/best_practices.md`
4. Add cross-references to related skills

### Acceptance Criteria
- [ ] All Tier C skills have 400+ line SKILL.md
- [ ] All have 2+ reference documents
- [ ] All have "When to Use" with alternative skills named
- [ ] Code examples are verified against current API

---

## Phase 4: Tier B Skills -- Polish & Depth

**Goal:** Bring 25 good skills to Tier A.

### Target Skills (examples)
- scikit-learn, aeon, matplotlib, polars, seaborn
- networkx, dask, pymoo, pymc, fluidsim
- literature-review, peer-review, scientific-writing
- statsmodels, umap-learn, shap

### Per-Skill Work
1. Add advanced examples and workflows
2. Create domain-specific reference documents
3. Add `scripts/advanced_workflow.py`
4. Add `assets/` diagrams where helpful
5. Ensure cross-references are bidirectional

### Acceptance Criteria
- [ ] All Tier B skills have 500+ line SKILL.md
- [ ] All have 3+ reference documents
- [ ] All have 2+ example scripts
- [ ] Advanced use cases documented

---

## Phase 5: Tier A Skills -- Final Review

**Goal:** Final quality pass on all 70 skills.

### Checklist (per skill)
- [ ] Frontmatter: name, description, license, metadata all present and accurate
- [ ] Description: follows three-question format, under 300 chars
- [ ] Overview: clear, concise, authoritative
- [ ] When to Use: specific scenarios with alternatives named
- [ ] Code Examples: all import paths verified, all examples runnable
- [ ] Cross-references: bidirectional links to related skills
- [ ] References: links to official docs verified (no dead links)
- [ ] Scripts: run without errors in clean environment

### Global Checks
- [ ] `marketplace.json` lists all 70 skills with correct paths
- [ ] `docs/skills.json` regenerated and accurate
- [ ] No duplicate skill coverage (each topic in exactly one skill)
- [ ] GitHub Pages catalog works correctly

---

## Phase 6: Coverage Expansion

**Goal:** Identify and fill domain gaps.

### Potential New Skills (evaluate based on demand)

| Domain | Gap | Candidate |
|--------|-----|-----------|
| Bioinformatics | No single-cell RNA-seq | scanpy |
| Cheminformatics | No molecular viz | nglview |
| Deep Learning | No JAX/Flax | jax |
| NLP | No text processing | spacy |
| Imaging | No image processing | opencv, scikit-image |
| Geospatial | No GIS processing | rasterio |
| Time Series | No forecasting | prophet, neuralprophet |
| MLOps | No experiment tracking | mlflow, wandb |

### Per New Skill
1. Evaluate: is this genuinely useful for scientific research?
2. Create skill following the final form template
3. Register in marketplace.json
4. Update GitHub Pages catalog

---

## Iteration Cadence

| Cycle | Focus | Duration |
|-------|-------|----------|
| Sprint 1 | Phase 1 (audit) + Phase 2 (Tier D) | 1 week |
| Sprint 2 | Phase 3 (Tier C) | 2 weeks |
| Sprint 3 | Phase 4 (Tier B) | 2 weeks |
| Sprint 4 | Phase 5 (Tier A review) | 1 week |
| Sprint 5 | Phase 6 (new skills) | Ongoing |

After each sprint:
1. Regenerate `skills.json`: `python scripts/generate_skills_data.py`
2. Commit all changes
3. Push to trigger GitHub Pages rebuild
4. Review the catalog page for accuracy
