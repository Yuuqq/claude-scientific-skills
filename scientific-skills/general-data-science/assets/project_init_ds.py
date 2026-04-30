
import os
import sys
import yaml
from pathlib import Path

def init_ds_project(project_name):
    """
    Initializes a standardized Data Science project structure.
    """
    base = Path(os.getcwd()) / project_name
    
    # 1. Directory Tree
    dirs = [
        "data/raw",          # Immutable
        "data/processed",    # Clean Parquet
        "data/interim",      # Checkpoints
        "data/external",     # Third-party data
        "notebooks/eda",     # Exploratory
        "notebooks/modeling",# Modeling prototypes
        "src/data",          # ETL Scripts
        "src/features",      # Feature Engineering
        "src/models",        # Training Scripts
        "src/visualization", # Plotting scripts
        "reports/figures",   # Final plots
        "config"             # Yaml/Json configs
    ]
    
    for d in dirs:
        (base / d).mkdir(parents=True, exist_ok=True)
        # Add .gitkeep to ensure git tracks empty dirs
        with open(base / d / ".gitkeep", "w") as f:
            pass

    # 2. Config File (YAML)
    config = {
        "project": {
            "name": project_name,
            "version": "0.1.0",
            "description": "Data Science Project"
        },
        "data": {
            "raw": "data/raw",
            "processed": "data/processed",
            "interim": "data/interim"
        },
        "parameters": {
            "random_seed": 42,
            "test_size": 0.2
        }
    }
    
    with open(base / "config/main.yaml", "w") as f:
        yaml.dump(config, f, default_flow_style=False)
        
    # 3. Gitignore
    gitignore = """
# Data
data/*
!data/**/*.gitkeep

# Environment
.env
__pycache__/
*.pyc

# IDE
.vscode/
.idea/

# Notebooks
.ipynb_checkpoints/
"""
    with open(base / ".gitignore", "w") as f:
        f.write(gitignore)

    print(f"✅ General Data Science Project '{project_name}' initialized.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="Project Name")
    args = parser.parse_args()
    init_ds_project(args.name)
