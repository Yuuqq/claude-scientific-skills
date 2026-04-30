# Technology Stack

**Analysis Date:** 2026-04-30

## Languages

**Primary:**
- Markdown - SKILL.md files, reference documentation, templates (all 140+ skills)
- YAML - SKILL.md frontmatter metadata (skill name, description, license, compatibility)

**Secondary:**
- Python 3.9+ (3.12+ recommended) - Helper scripts in 36 skills (`.py` files under `scripts/` directories)
- LaTeX - Template files in 15 skills (`.tex` files under `assets/` directories for posters, slides, papers, grants)
- JSON - Plugin manifest (`.claude-plugin/marketplace.json`), OOXML validation schemas in document-skills
- XML/HTML - OOXML document templates within `document-skills/docx/`, `document-skills/pptx/`

## Runtime

**Environment:**
- No runtime engine required for the repository itself (content-only project)
- Python 3.9+ required by end-users when executing skill scripts
- uv (Astral) - Python package manager recommended for dependency installation (`uv pip install`)
- System support: macOS, Linux, Windows with WSL2

**Package Manager:**
- uv (Astral) - Recommended Python package manager for skill dependencies
- `pyproject.toml` and `uv.lock` are gitignored (not part of the repository distribution)
- No Node.js, no npm, no package.json at the project level

**Lockfile:**
- Missing (gitignored by design - each skill manages dependencies independently)

## Frameworks & Platforms

**Distribution Platform:**
- Claude Code Plugin Marketplace - Primary distribution via `marketplace.json` manifest
- MCP (Model Context Protocol) Server - Alternative distribution for non-Claude clients
  - Hosted: `https://mcp.k-dense.ai/claude-scientific-skills/mcp`
  - Self-hosted: Separate repo at `github.com/K-Dense-AI/claude-skills-mcp`
- Cursor IDE - One-click MCP installation
- ChatGPT, Google ADK, OpenAI Agent SDK - Via MCP protocol

**Spec Compliance:**
- Agent Skills Specification (agentskills.io) - All skills follow this spec for frontmatter, naming, directory structure

**Build/CI:**
- GitHub Actions (`softprops/action-gh-release@v1`) - Automated release creation
- Trigger: Pushes to `main` that modify `.claude-plugin/marketplace.json`
- No build step, no compilation, no bundling

## Key Dependencies (Referenced by Skills)

**Python Scientific Stack (referenced across skills):**
- NumPy - Numerical computing foundation (used by nearly all scientific skills)
- pandas - Tabular data manipulation (used by most data analysis skills)
- SciPy - Scientific computing algorithms (optimization, interpolation, signal processing)
- scikit-learn - Classical ML framework (referenced by ML and analysis skills)
- Matplotlib / Seaborn - Visualization (referenced by visualization and reporting skills)

**Bioinformatics Stack:**
- Scanpy + AnnData - Single-cell RNA-seq analysis ecosystem
- BioPython - Sequence analysis and database access
- BioServices - Unified access to 40+ biological web services
- pysam - Genomic file I/O (SAM/BAM/VCF/FASTA)
- scvi-tools - Probabilistic deep learning for single-cell omics
- PyDESeq2 - Differential gene expression for bulk RNA-seq
- gget - Unified genomic database querying

**Cheminformatics Stack:**
- RDKit - Core cheminformatics toolkit (molecular I/O, descriptors, fingerprints, SMARTS)
- DeepChem - Deep learning for molecular ML (TensorFlow/PyTorch backends)
- DiffDock - Diffusion-based molecular docking
- Datamol / Molfeat / MedChem - Molecular manipulation, featurization, drug-likeness assessment
- PyTDC - Therapeutics Data Commons benchmarks for drug discovery

**ML/AI Stack:**
- PyTorch Lightning - Deep learning training framework (40+ tasks automated)
- Hugging Face Transformers - NLP and multimodal models (1M+ pre-trained models)
- Stable Baselines3 - Reinforcement learning (PPO, SAC, DQN, TD3, DDPG, A2C)
- PufferLib - High-performance RL (1M-4M steps/sec vectorization)
- Torch Geometric - Graph neural networks for molecular/geometric data
- SHAP - Model interpretability via Shapley values
- aeon - Time series ML (classification, regression, clustering, forecasting, anomaly detection)
- UMAP-learn - Dimensionality reduction

**Bayesian & Statistical:**
- PyMC - Bayesian statistical modeling and probabilistic programming
- statsmodels - Classical statistical modeling and econometrics
- scikit-survival - Survival analysis with censored data
- PyMOO - Multi-objective optimization (NSGA-II, NSGA-III, MOEA/D)

**Quantum Computing:**
- Qiskit - IBM quantum framework (13M+ downloads, 100+ quantum gates)
- PennyLane - Cross-platform quantum ML (PyTorch/JAX/NumPy integration)
- Cirq - Google quantum framework
- QuTiP - Quantum mechanics simulation (open/closed quantum systems)

**Data Processing:**
- Dask - Parallel computing for larger-than-memory datasets
- Polars - High-performance DataFrames (Rust-backed, 5-30x faster than pandas)
- Vaex - Out-of-core lazy DataFrames (billion rows/sec)
- Zarr - Chunked compressed N-dimensional array storage

**Document Processing:**
- python-docx / python-pptx - Office document generation (OOXML)
- ReportLab - Programmatic PDF generation
- openpyxl - Excel file handling
- MarkItDown - Multi-format to Markdown conversion (20+ formats)

**External API Clients (via scripts):**
- LiteLLM - Unified LLM API proxy (used by perplexity-search and research-lookup)
- requests - HTTP client (used by database query scripts)
- OpenRouter API - Gateway for Perplexity and image generation models

## Skill Directory Structure

**Standard Skill Layout:**
```
scientific-skills/{skill-name}/
  SKILL.md              # Required. Frontmatter + documentation
  references/           # Optional. Deep-dive reference docs (.md files)
  scripts/              # Optional. Python helper scripts (.py files)
  assets/               # Optional. Templates, color schemes, report templates
```

**SKILL.md Frontmatter Schema:**
```yaml
---
name: {skill-name}                    # Required. Lowercase kebab-case matching directory
description: {one-line description}    # Required. Skill purpose and when to use
license: {license identifier}          # Required. MIT, Apache-2.0, BSD-3-Clause, Unknown
compatibility: {requirements}          # Optional. API keys or special setup needed
allowed-tools: [Read, Write, Edit, Bash]  # Optional. Tool permissions
metadata:
    skill-author: K-Dense Inc.         # Required
---
```

**Document Skills Sub-structure:**
```
scientific-skills/document-skills/
  docx/               # Word document creation
    SKILL.md
    scripts/          # document.py, utilities.py
    ooxml/            # Pack/unpack/validate tools
  pdf/                # PDF processing
    SKILL.md
    scripts/          # 7 Python scripts for form/image operations
  pptx/               # PowerPoint creation
    SKILL.md
    ooxml/            # Pack/unpack/validate tools
  xlsx/               # Excel operations
    SKILL.md
```

**Computation Social Science Sub-structure:**
```
scientific-skills/computational-social-science/
  SKILL.md
  methods/            # Additional sub-directory for method documentation
  references/
  scripts/
  assets/
```

## Configuration

**Plugin Manifest:**
- `.claude-plugin/marketplace.json` - Defines plugin name, owner, version (2.17.0), and skill paths
- Version-driven releases: Changing version in marketplace.json triggers GitHub Actions release
- 140 skill paths registered across a single plugin named `scientific-skills`
- Skills are prefixed with `./scientific-skills/` in the manifest

**Environment Variables (skill-specific, user-configured):**
- `OPENROUTER_API_KEY` - Required by perplexity-search, generate-image, research-lookup, scientific-schematics skills
- Various API keys per database skill (many databases are open/no-auth)

**Build/CI Configuration:**
- `.github/workflows/release.yml` - Single workflow file
- No `.eslintrc`, `tsconfig.json`, `webpack.config`, or similar build tooling
- No Docker configuration

## Platform Requirements

**Development (contributing to the repo):**
- Git
- Text editor or IDE
- No build tools required
- Python 3.9+ for testing scripts locally

**Production (using skills):**
- Claude Code (recommended), Cursor IDE, or any MCP-compatible client
- Python 3.9+ (3.12+ recommended)
- uv package manager for installing Python dependencies
- Internet access for database skills (API-dependent)
- Optional: GPU for ML/AI skills (NVIDIA CUDA, AMD ROCm, Apple Silicon Metal)
- Optional: LaTeX distribution (TeX Live, MiKTeX) for poster/paper/template skills

## Asset Types

**Documentation:**
- `SKILL.md` - 71 files across 67 top-level directories (document-skills has 4 sub-skills)
- `references/` - 62 skills have reference documentation directories
- `.md` files in references/ - Deep-dive API references, best practices, workflow guides

**Code:**
- `scripts/` - 36 skills have Python script directories
- 106 total Python files across all skills
- `assets/` - 17 skills have asset directories (LaTeX templates, report templates, color schemes)

**Templates:**
- 15 LaTeX (`.tex`) template files across poster, slides, writing, grants, and venue-template skills
- OOXML templates in `document-skills/docx/`, `document-skills/pptx/`
- PDF form templates in `document-skills/pdf/`

## Skill Categories by Stack Domain

**Bioinformatics & Genomics (16+ skills):**
- Tools: BioPython, pysam, Scanpy, AnnData, scvi-tools, Arboreto, PyDESeq2, gget, geniml, gtars, deepTools, FlowIO, BioServices, Cellxgene Census, ETE Toolkit, scikit-bio, Zarr

**Cheminformatics & Drug Discovery (11+ skills):**
- Tools: RDKit, Datamol, Molfeat, MedChem, DeepChem, TorchDrug, DiffDock, Rowan, PyTDC

**Clinical Research (12+ skills):**
- Tools: PyHealth, NeuroKit2, pysam (for VCF parsing)

**ML & AI (15+ skills):**
- Tools: PyTorch Lightning, Transformers, Stable Baselines3, PufferLib, scikit-learn, scikit-survival, SHAP, aeon, PyMC, PyMOO, Torch Geometric, UMAP-learn, statsmodels

**Materials Science & Physics (7 skills):**
- Tools: Pymatgen, COBRApy, Astropy, Cirq, PennyLane, Qiskit, QuTiP

**Data Analysis & Visualization (14+ skills):**
- Tools: Matplotlib, Seaborn, Plotly, NetworkX, GeoPandas, SymPy, Polars, Dask, Vaex, ReportLab, Data Commons

**Laboratory Automation (3 skills):**
- Tools: PyLabRobot, Protocols.io, Benchling, LabArchives, Opentrons

---

*Stack analysis: 2026-04-30*
