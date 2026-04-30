
import os
import json
import sys
from pathlib import Path

def init_project(project_name):
    """
    Initializes a standardized Computational Social Science (CSS) project structure
    suitable for 'Nature'/'Science' rigor with GenAI capabilities.
    """
    base_path = Path(os.getcwd()) / project_name
    
    # 1. Directory Structure
    dirs = [
        "data/raw",          # Immutable raw data (GitIgnored)
        "data/processed",    # Cleaned intermediate parquet files
        "data/output",       # Final regression tables / figures
        "scripts/etl",       # Data cleaning scripts
        "scripts/analysis",  # Stats / Network / ML scripts
        "scripts/vis",       # Figure generation
        "prompts",           # System prompts versioned 
        "assets",            # Dictionaries, Stopwords, Configs
        "notebooks",         # Exploratory (Not production)
        "docs",              # Research Design & Logs
    ]
    
    for d in dirs:
        (base_path / d).mkdir(parents=True, exist_ok=True)
        # Add .gitkeep to empty dirs
        with open(base_path / d / ".gitkeep", "w") as f:
            pass

    # 2. Config Template (Gemini 3 Pro / Claude Opus 4.5)
    config = {
        "project_meta": {
            "name": project_name,
            "author": "qcm",
            "date": "2026-01-17",
            "target_journal": "Nature Human Behaviour / New Media & Society"
        },
        "paths": {
            "raw": "data/raw",
            "processed": "data/processed",
            "figures": "data/output"
        },
        "llm_config": {
            "primary_model": "claude-3-opus-20240229", 
            "secondary_model": "gemini-2.0-pro-001",
            "temperature": 0.0,
            "max_tokens": 4096,
            "api_key_env_var": "ANTHROPIC_API_KEY"
        },
        "plot_style": {
            "font": "Arial",
            "dpi": 300,
            "palette": "okabe_ito"
        },
        "random_seed": 42
    }
    
    with open(base_path / "assets/config.json", "w") as f:
        json.dump(config, f, indent=4)
        
    # 3. System Prompt Template
    prompt_template = """# System Role: Expert Computational Social Science Coder

You are an expert impartial coder for a study on [TOPIC].
Your goal is to classify the provided text into specific categories defined below.

## Coding Codebook
1. **Category A**: [Definition]
2. **Category B**: [Definition]
3. **NA**: If the text does not fit any category or is ambiguous, output "NA".

## Output Format
You MUST output strictly Valid JSON:
{
    "category": "Category A",
    "reasoning": "The text mentions...",
    "confidence": 0.95
}
"""
    with open(base_path / "prompts/system_v1.md", "w", encoding='utf-8') as f:
        f.write(prompt_template)

    # 4. Gitignore (Safety First)
    gitignore = """
# Data Safety
data/raw/*
!data/raw/.gitkeep
data/processed/*.parquet
data/processed/*.csv

# Secrets
.env
*.key
config_private.json

# Cache
__pycache__/
.ipynb_checkpoints/
"""
    with open(base_path / ".gitignore", "w") as f:
        f.write(gitignore)

    print(f"✅ CSS Project '{project_name}' initialized at {base_path}")
    print(f"👉 Next Step: Copy your 'RESEARCH_DESIGN_MASTER.md' to docs/")
    print(f"👉 Define your variables in 'assets/config.json'")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        init_project(sys.argv[1])
    else:
        init_project("css_project_template")
