# CSS Python Patterns

> **Code-as-Truth**: These snippets are designed to be reproducible, robust, and rigorous. Copy, adapt, and run.

## 1. Setup & Configuration
Standard header for every script. Enforces reproducibility.

```python
import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# --- CONFIG LOADING ---
with open('config.json', 'r') as f:
    config = json.load(f)

# --- REPRODUCIBILITY ---
SEED = config['parameters']['random_seed']
np.random.seed(SEED)

# --- PATHS ---
RAW_DIR = Path(config['paths']['raw_data'])
PROC_DIR = Path(config['paths']['processed_data'])
FIG_DIR = Path(config['paths']['output_figures'])

# Ensure directories exist
FIG_DIR.mkdir(parents=True, exist_ok=True)
PROC_DIR.mkdir(parents=True, exist_ok=True)
```

## 2. Nature-Style Plotting
Global aesthetics for publication-quality figures.

```python
def set_nature_style():
    sns.set_style("ticks")
    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.sans-serif': ['Arial', 'Helvetica'],
        'font.size': 8,              # Base font size
        'axes.labelsize': 9,         # Axis labels
        'xtick.labelsize': 8,
        'ytick.labelsize': 8,
        'legend.fontsize': 8,
        'figure.titlesize': 10,
        'axes.spines.top': False,    # Remove chartjunk
        'axes.spines.right': False
    })

set_nature_style()

# Example Usage
fig, ax = plt.subplots(figsize=(3.5, 2.5)) # Single column width ~3.5 inch
sns.scatterplot(x='x', y='y', data=df, ax=ax, alpha=0.6, s=15, color='#377eb8')
plt.savefig(FIG_DIR / "fig1_nature_style.png", dpi=300, bbox_inches='tight')
```

## 3. Semantic Network Analysis (SNA)
Building a co-occurrence network from text.

```python
import networkx as nx
import community as community_louvain
from itertools import combinations
from collections import Counter

def build_semantic_network(tokens_list, window_size=5, top_n_edges=500):
    edges = Counter()
    
    # Sliding window co-occurrence
    for tokens in tokens_list:
        if len(tokens) < 2: continue
        for i in range(len(tokens) - window_size + 1):
            window = tokens[i : i + window_size]
            # Add all pairs in window (undirected)
            unique_tokens = sorted(list(set(window)))
            for pair in combinations(unique_tokens, 2):
                edges[pair] += 1
                
    # Filter for top edges
    most_common = edges.most_common(top_n_edges)
    
    # Build Graph
    G = nx.Graph()
    for (node1, node2), weight in most_common:
        G.add_edge(node1, node2, weight=weight)
        
    return G

# Metrics & Community
def analyze_network(G):
    # Louvain Community Detection
    partition = community_louvain.best_partition(G, weight='weight')
    
    # Centrality
    deg = nx.degree_centrality(G)
    bet = nx.betweenness_centrality(G, weight='weight')
    
    # Add to node attributes
    nx.set_node_attributes(G, partition, 'community')
    nx.set_node_attributes(G, deg, 'degree_centrality')
    nx.set_node_attributes(G, bet, 'betweenness_centrality')
    
    return G, partition
```

## 4. Panel Fixed Effects Regression
Econometrics using `linearmodels`.

```python
from linearmodels.panel import PanelOLS

def run_fixed_effects(df, y_col, x_cols, entity_col, time_col):
    """
    Runs a Two-Way Fixed Effects Model (Entity + Time).
    """
    # 1. Set Index for Panel
    panel_df = df.set_index([entity_col, time_col])
    
    # 2. Formula Construct
    # EntityEffects + TimeEffects adds the fixed effects
    formula = f"{y_col} ~ 1 + {' + '.join(x_cols)} + EntityEffects + TimeEffects"
    
    # 3. Fit Model
    mod = PanelOLS.from_formula(formula, data=panel_df)
    
    # 4. Cluster Standard Errors (Robust Inference)
    res = mod.fit(cov_type='clustered', cluster_entity=True)
    
    return res

# Usage:
# results = run_fixed_effects(data, 'polarization', ['algorithm_exposure', 'age'], 'user_id', 'date')
# print(results)
```

## 5. Semantic Decoupling (Embeddings)
Projecting words onto a bias axis.

```python
from scipy.spatial.distance import cosine

def measure_projection(target_vec, axis_start_vec, axis_end_vec):
    """
    Scales target_vec onto the axis defined by (axis_end - axis_start).
    Returns -1 to 1 (roughly).
    """
    axis = axis_end_vec - axis_start_vec
    
    # Cosine similarity projection
    # sim(a, b) = dot(a, b) / (norm(a) * norm(b))
    return 1 - cosine(target_vec, axis)

## 6. Robust LLM Annotation Pattern
# Use this for converting text to categorical variables with stability checks.

import time
import pandas as pd
# from openai import OpenAI (or use local Ollama client)

def functional_llm_coder(text_batch, system_prompt, model="gpt-4-turbo", distinct_n=3):
    """
    Annotates a batch of text. Runs 'distinct_n' times to check stability (stochasticity).
    Returns the consensus label and a stability score (0.0 - 1.0).
    """
    results = []
    
    # Mock LLM Call structure
    # for _ in range(distinct_n):
    #     response = client.chat.completions.create(...)
    #     results.append(response.content)
    
    # Logic:
    # 1. Force strict JSON output (e.g., {"label": "Populist", "confidence": 0.9})
    # 2. Compare results across runs.
    # 3. If stability < 1.0, flag for human review.
    
    pass

## 8. DSPy Annotation Pipeline (The Gold Standard)
# Replaces manual prompt engineering with compiled, optimized modules.

import dspy
from pydantic import BaseModel, Field

# 1. Define Output Schema
class AnnotationOutput(BaseModel):
    label: str = Field(description="Category: 'Populist' or 'Mainstream'")
    confidence: float = Field(description="Confidence score between 0.0 and 1.0")
    reasoning: str = Field(description="Brief justification for the coding")

# 2. Define Signature
class TextClassifier(dspy.Signature):
    """Classify political text into defined stances."""
    text = dspy.InputField(desc="The social media post or article fragment")
    classification = dspy.OutputField(desc="Structured categorization", type=AnnotationOutput)

# 3. Create Module
def run_classification_pipeline(train_examples, unlabeled_data):
    # Configure LM
    lm = dspy.Claude(model="claude-3-5-sonnet-latest")
    dspy.settings.configure(lm=lm)
    
    # Compile Optimizer (MIPRO or BootstrapFewShot)
    # This "learns" the best prompt from your labeled examples
    optimizer = dspy.teleprompt.BootstrapFewShotWithRandomSearch(metric=custom_metric)
    
    # The 'program' is the compiled annotator
    program = dspy.TypedPredictor(TextClassifier)
    optimized_program = optimizer.compile(program, trainset=train_examples)
    
    return optimized_program(text=unlabeled_data[0])

## 7. Text-as-Confounder Causal Inference (Double Machine Learning Concept)
# Estimating Effect of T on Y, controlling for high-dim Text (Z)

from sklearn.linear_model import LassoCV
from sklearn.ensemble import RandomForestRegressor
import numpy as np

def causal_effect_with_text_controls(df, treatment_col, outcome_col, text_embedding_cols):
    """
    Implements a basic Double Machine Learning (DML) approach using Partialing Out.
    1. Regress Y ~ TextEmbeddings -> Get Residuals (Y_res)
    2. Regress T ~ TextEmbeddings -> Get Residuals (T_res)
    3. Regress Y_res ~ T_res -> Coefficient is the causal effect of T on Y.
    """
    
    # 1. Model Outcome ~ Text
    y = df[outcome_col]
    X_text = df[text_embedding_cols]
    model_y = RandomForestRegressor(n_estimators=100)
    model_y.fit(X_text, y)
    y_res = y - model_y.predict(X_text)
    
    # 2. Model Treatment ~ Text
    t = df[treatment_col]
    model_t = RandomForestRegressor(n_estimators=100)
    model_t.fit(X_text, t)
    t_res = t - model_t.predict(X_text)
    
    # 3. Final Causal Estimate (Frisch-Waugh-Lovell Theorem)
    # Using a simple OLS on residuals
    import statsmodels.api as sm
    model_final = sm.OLS(y_res, sm.add_constant(t_res))
    results = model_final.fit()
    
    return results.summary()
```
