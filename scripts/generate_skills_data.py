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

    # Check for scripts and references
    has_scripts = (path / "scripts").is_dir()
    has_references = (path / "references").is_dir() or (path / "reference").is_dir()
    has_assets = (path / "assets").is_dir()

    return {
        "id": full_name,
        "name": full_name,
        "description": desc,
        "license": license_info,
        "category": get_category(full_name, path.name),
        "has_scripts": has_scripts,
        "has_references": has_references,
        "has_assets": has_assets,
    }


def main():
    skills = collect_skills()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(skills, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Generated {OUTPUT} with {len(skills)} skills")


if __name__ == "__main__":
    main()
