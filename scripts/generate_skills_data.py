#!/usr/bin/env python3
"""Extract skill metadata from SKILL.md files and generate docs/skills.json."""

import json
import os
import re
from pathlib import Path

SKILLS_DIR = Path("scientific-skills")
OUTPUT = Path("docs/skills.json")

# Category mapping based on skill name/description
CATEGORIES = {
    "Bioinformatics": [
        "biopython", "scanpy", "anndata", "scvi-tools", "pydeseq2", "pysam",
        "gget", "etetoolkit", "scikit-bio", "deeptools", "geniml", "cellxgene-census",
        "arboreto", "cobrapy", "biorxiv-database", "alphafold-database",
        "esm", "torchdrug", "adaptyv", "biomni", "bioservices", "diffdock",
        "rowan",
    ],
    "Cheminformatics": [
        "rdkit", "deepchem", "datamol", "molfeat", "medchem", "pytdc",
        "chembl-database", "pubchem-database", "zinc-database", "drugbank-database",
        "uspto-database",
    ],
    "Proteomics": [
        "pyopenms", "matchms", "flowio", "uniprot-database", "pdb-database",
        "brenda-database", "string-database",
    ],
    "Clinical & Medical": [
        "clinical-decision-support", "clinical-reports", "treatment-plans",
        "pyhealth", "pydicom", "pathml", "histolab", "neurokit2",
        "clinvar-database", "clinicaltrials-database", "clinpgx-database",
        "cosmic-database", "fda-database", "gene-database",
    ],
    "Machine Learning": [
        "scikit-learn", "pytorch-lightning", "transformers", "shap",
        "stable-baselines3", "pufferlib", "torch_geometric", "torch-geometric",
        "umap-learn", "aeon", "scikit-survival",
    ],
    "Quantum Computing": [
        "qiskit", "cirq", "pennylane", "qutip",
    ],
    "Materials & Chemistry": [
        "pymatgen", "pymc", "pymc-bayesian-modeling", "pymoo", "fluidsim",
    ],
    "Physics & Math": [
        "astropy", "sympy", "statsmodels",
    ],
    "Data Analysis": [
        "polars", "dask", "vaex", "networkx", "geopandas",
        "exploratory-data-analysis", "statistical-analysis",
        "datacommons-client",
    ],
    "Visualization": [
        "matplotlib", "seaborn", "plotly", "scientific-visualization",
        "generate-image", "scientific-schematics",
    ],
    "Simulation & Engineering": [
        "simpy", "modal", "denario", "gtars",
    ],
    "Scientific Communication": [
        "literature-review", "peer-review", "scientific-writing",
        "scientific-brainstorming", "scientific-critical-thinking",
        "hypothesis-generation", "hypogenic", "scholar-evaluation",
        "citation-management", "research-grants", "research-lookup",
        "scientific-slides", "latex-posters", "pptx-posters",
        "paper-2-web", "venue-templates",
    ],
    "Document Processing": [
        "markitdown", "document-skills", "docx", "pdf", "pptx", "xlsx",
    ],
    "Research Tools": [
        "get-available-resources", "perplexity-search", "matlab",
        "computational-social-science", "general-data-science",
        "market-research-reports",
    ],
    "Lab & Integration": [
        "benchling-integration", "dnanexus-integration",
        "labarchive-integration", "latchbio-integration",
        "omero-integration", "opentrons-integration",
        "protocolsio-integration", "pylabrobot",
        "lamindb", "iso-13485-certification",
    ],
    "Database & API": [
        "openalex-database", "pubmed-database", "geo-database",
        "gwas-database", "hmdb-database", "kegg-database",
        "metabolomics-workbench-database", "opentargets-database",
        "reactome-database", "ena-database", "ensembl-database",
    ],
}


# Discipline tags (a skill can belong to several). Anything unmapped -> General.
DISCIPLINES = {
    # Scientific communication -> useful to every field
    "citation-management": ["General"],
    "hypogenic": ["General", "Data Science & AI"],
    "hypothesis-generation": ["General"],
    "latex-posters": ["General"],
    "literature-review": ["General"],
    "paper-2-web": ["General"],
    "peer-review": ["General"],
    "pptx-posters": ["General"],
    "research-grants": ["General"],
    "research-lookup": ["General"],
    "scholar-evaluation": ["General"],
    "scientific-brainstorming": ["General"],
    "scientific-critical-thinking": ["General"],
    "scientific-slides": ["General"],
    "scientific-writing": ["General"],
    "venue-templates": ["General"],
    # Machine learning
    "aeon": ["Data Science & AI", "Math & Statistics"],
    "pufferlib": ["Data Science & AI"],
    "pytorch-lightning": ["Data Science & AI"],
    "scikit-learn": ["Data Science & AI"],
    "scikit-survival": ["Biology & Medicine", "Math & Statistics", "Data Science & AI"],
    "shap": ["Data Science & AI"],
    "stable-baselines3": ["Data Science & AI"],
    "torch-geometric": ["Data Science & AI"],
    "transformers": ["Data Science & AI"],
    "umap-learn": ["Data Science & AI"],
    # Data analysis
    "dask": ["Data Science & AI"],
    "datacommons-client": ["Social Science & Economics"],
    "exploratory-data-analysis": ["Data Science & AI", "Math & Statistics"],
    "geopandas": ["Geospatial"],
    "networkx": ["Math & Statistics", "Social Science & Economics"],
    "polars": ["Data Science & AI"],
    "statistical-analysis": ["Math & Statistics"],
    "vaex": ["Data Science & AI"],
    # Research tools
    "computational-social-science": ["Social Science & Economics"],
    "general-data-science": ["Data Science & AI"],
    "get-available-resources": ["General"],
    "market-research-reports": ["Social Science & Economics"],
    "matlab": ["Engineering", "Math & Statistics"],
    "perplexity-search": ["General"],
    # Visualization
    "generate-image": ["General"],
    "matplotlib": ["General", "Data Science & AI"],
    "plotly": ["General", "Data Science & AI"],
    "scientific-schematics": ["General"],
    "scientific-visualization": ["General"],
    "seaborn": ["Data Science & AI", "Math & Statistics"],
    # Document processing
    "document-skills/docx": ["General"],
    "document-skills/pdf": ["General"],
    "document-skills/pptx": ["General"],
    "document-skills/xlsx": ["General"],
    "markitdown": ["General"],
    # Databases
    "openalex-database": ["General"],
    "pubmed-database": ["Biology & Medicine"],
    "biorxiv-database": ["Biology & Medicine"],
    "uspto-database": ["Engineering", "Social Science & Economics"],
    # Quantum computing
    "cirq": ["Quantum", "Physics & Astronomy"],
    "pennylane": ["Quantum", "Physics & Astronomy"],
    "qiskit": ["Quantum", "Physics & Astronomy"],
    "qutip": ["Quantum", "Physics & Astronomy"],
    # Materials, chemistry, physics, math
    "fluidsim": ["Physics & Astronomy", "Engineering"],
    "pymatgen": ["Chemistry & Materials"],
    "pymc": ["Math & Statistics", "Data Science & AI"],
    "pymoo": ["Engineering", "Math & Statistics"],
    "astropy": ["Physics & Astronomy"],
    "statsmodels": ["Math & Statistics", "Social Science & Economics"],
    "sympy": ["Math & Statistics", "Physics & Astronomy"],
    # Simulation & engineering
    "denario": ["General", "Data Science & AI"],
    "modal": ["Engineering", "Data Science & AI"],
    "simpy": ["Engineering"],
}


def get_disciplines(skill_id: str, dir_name: str) -> list:
    return DISCIPLINES.get(skill_id) or DISCIPLINES.get(dir_name) or ["General"]


def compute_maturity(lines: int, n_refs: int, n_scripts: int, has_assets: bool) -> int:
    """Auto-scored 1-5 from measurable signals only (no editorial opinion):
    documentation depth, reference docs, runnable scripts, bundled assets."""
    pts = 0
    if lines >= 500:
        pts += 3
    elif lines >= 300:
        pts += 2
    elif lines >= 120:
        pts += 1
    if n_refs >= 3:
        pts += 2
    elif n_refs >= 1:
        pts += 1
    if n_scripts >= 1:
        pts += 1
    if has_assets:
        pts += 1
    if pts <= 1:
        return 1
    if pts == 2:
        return 2
    if pts == 3:
        return 3
    if pts <= 5:
        return 4
    return 5


def get_category(skill_id: str, dir_name: str) -> str:
    # Try matching both the full ID and the directory name
    for cat, names in CATEGORIES.items():
        if skill_id in names or dir_name in names:
            return cat
    # Also try parent dir for sub-skills
    parent = skill_id.split("/")[0] if "/" in skill_id else None
    if parent:
        for cat, names in CATEGORIES.items():
            if parent in names:
                return cat
    return "Other"


def parse_frontmatter(text: str) -> dict:
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith(" ") and not line.startswith("\t"):
            key, val = line.split(":", 1)
            fm[key.strip()] = val.strip()
    return fm


def collect_skills():
    skills = []
    for d in sorted(SKILLS_DIR.iterdir()):
        if not d.is_dir():
            continue

        # Handle sub-skills (e.g., document-skills/docx)
        sub_dirs = [sd for sd in d.iterdir() if sd.is_dir() and (sd / "SKILL.md").exists()]
        if sub_dirs:
            for sd in sorted(sub_dirs):
                skills.append(_extract_skill(sd, parent=d.name))
        elif (d / "SKILL.md").exists():
            skills.append(_extract_skill(d))

    return skills


def _count_files(directory: Path) -> int:
    if not directory.is_dir():
        return 0
    return sum(1 for f in directory.rglob("*") if f.is_file())


def _extract_skill(path: Path, parent: str = None) -> dict:
    text = (path / "SKILL.md").read_text(encoding="utf-8")
    fm = parse_frontmatter(text)

    name = fm.get("name", path.name)
    full_name = f"{parent}/{name}" if parent else name

    # Clean description
    desc = fm.get("description", "")
    # Remove "This skill should be used" prefix patterns
    desc = re.sub(r"^This skill should be used\s+", "", desc, flags=re.IGNORECASE)

    # Extract license
    license_info = fm.get("license", "")

    lines = text.count("\n") + 1
    n_refs = _count_files(path / "references") + _count_files(path / "reference")
    n_scripts = _count_files(path / "scripts")
    has_assets = (path / "assets").is_dir()

    return {
        "id": full_name,
        "name": full_name,
        "description": desc,
        "license": license_info,
        "category": get_category(full_name, path.name),
        "disciplines": get_disciplines(full_name, path.name),
        "path": path.as_posix(),
        "lines": lines,
        "n_references": n_refs,
        "n_scripts": n_scripts,
        "maturity": compute_maturity(lines, n_refs, n_scripts, has_assets),
        "has_scripts": n_scripts > 0,
        "has_references": n_refs > 0,
        "has_assets": has_assets,
    }


def main():
    skills = collect_skills()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(skills, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Generated {OUTPUT} with {len(skills)} skills")


if __name__ == "__main__":
    main()
