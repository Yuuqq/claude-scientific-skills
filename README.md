# Claude Scientific Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE.md)
[![Skills](https://img.shields.io/badge/Skills-70-brightgreen.svg)](#available-skills)
[![GitHub Pages](https://img.shields.io/badge/GitHub-Pages-blue)](https://yuuqq.github.io/claude-scientific-skills/)

A collection of **70 ready-to-use scientific skills** for Claude Code. Transform Claude into your AI research assistant for biology, chemistry, medicine, physics, data analysis, and beyond.

**[Browse all skills on the interactive catalog](https://yuuqq.github.io/claude-scientific-skills/)**

---

## Origin

This repository is a **curated subset** of the original [claude-scientific-skills](https://github.com/K-Dense-AI/claude-scientific-skills) project by [K-Dense Inc.](https://k-dense.ai/). The original repository contained 140+ skills; this fork retains 70 skills that are actively maintained and validated. All skills are MIT-licensed (individual skills may have their own licenses as specified in their `SKILL.md`).

---

## Available Skills

### Scientific Communication (16 skills)
Literature review, peer review, scientific writing, hypothesis generation, citation management, research grants, scholar evaluation, scientific schematics, slides, posters, and more.

### Machine Learning (10 skills)
scikit-learn, PyTorch Lightning, Transformers, SHAP, Stable Baselines3, PufferLib, Torch Geometric, UMAP-learn, aeon, scikit-survival.

### Data Analysis (8 skills)
Polars, Dask, Vaex, NetworkX, GeoPandas, statsmodels, SymPy, Data Commons.

### Visualization (6 skills)
Matplotlib, Seaborn, Plotly, scientific visualization, AI image generation, scientific schematics.

### Research Tools (6 skills)
Computational social science, general data science, resource detection, market research, MATLAB, Perplexity search.

### Document Processing (5 skills)
DOCX, PDF, PPTX, XLSX generation, MarkItDown conversion.

### Quantum Computing (4 skills)
Qiskit (IBM), Cirq (Google), PennyLane (gradient-based), QuTiP (open quantum systems).

### Materials & Chemistry (4 skills)
Pymatgen, PyMC (Bayesian modeling), PyMOO (optimization), FluidSim.

### Physics & Math (3 skills)
Astropy, statsmodels, SymPy.

### Simulation & Engineering (3 skills)
SimPy, Modal (cloud compute), Denario.

### Databases (4 skills)
OpenAlex, PubMed, bioRxiv, USPTO.

---

## Getting Started

### Prerequisites

- **Claude Code** -- [Install guide](https://docs.claude.com/en/docs/claude-code/quickstart)
- **Python 3.9+** (3.12+ recommended)
- **uv** -- Python package manager ([install](https://docs.astral.sh/uv/))

### Install as Plugin

```bash
# In Claude Code:
/plugin marketplace add Yuuqq/claude-scientific-skills
/plugin install scientific-skills@claude-scientific-skills
```

### Or Use via MCP Server

For Cursor, ChatGPT, or any MCP-compatible client:

```
https://mcp.k-dense.ai/claude-scientific-skills/mcp
```

---

## Quick Examples

### Literature Review
```
Conduct a systematic literature review on CRISPR delivery mechanisms using PubMed and bioRxiv.
Include a PRISMA flow diagram using scientific-schematics.
```

### Data Analysis
```
Load my CSV dataset, run exploratory data analysis with statistical tests,
and create publication-quality visualizations with matplotlib and seaborn.
```

### Machine Learning
```
Train a classification model on my dataset using scikit-learn,
explain predictions with SHAP, and generate a comprehensive report.
```

---

## Project Structure

```
scientific-skills/
  <skill-name>/
    SKILL.md          # Main skill documentation (required)
    references/       # Detailed reference docs (optional)
    scripts/          # Example Python scripts (optional)
    assets/           # Images and diagrams (optional)
```

Each `SKILL.md` contains:
- Description of what the skill does and when to use it
- Core concepts and API reference
- Code examples and best practices
- Integration guides with other skills

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Follow the [Agent Skills Specification](https://agentskills.io/specification) for new skills
4. Ensure `SKILL.md` has valid frontmatter (`name`, `description`, `license`)
5. Test all code examples
6. Submit a pull request

---

## License

MIT License. Copyright (c) 2025 K-Dense Inc.

Individual skills may have their own licenses -- check the `license` field in each skill's `SKILL.md`.

**Original project:** [K-Dense-AI/claude-scientific-skills](https://github.com/K-Dense-AI/claude-scientific-skills) by [K-Dense Inc.](https://k-dense.ai/)
