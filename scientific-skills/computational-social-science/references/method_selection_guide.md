# Method Selection Guide for Computational Social Science

## Decision Tree

Use this flow to determine the most appropriate method for your research question.

```mermaid
graph TD
    A[Start: Define Research Question] --> B{Does it involve Text/Language?}
    
    B -->|Yes| C{What is the Unit of Analysis?}
    B -->|No| D{Does it involve Causal Inference on Tables?}
    
    C -->|Relationships between Words| E[Semantic Network Analysis (SNA)]
    C -->|Relationships between Actors| F[Social Network Analysis]
    C -->|Content/Theme/Stance| G[Natural Language Processing (NLP)]
    
    D -->|Yes: Observational Data| H[Econometrics / Causal Inference]
    D -->|Yes: Experimental Data| I[AB Testing / Experiments]
    D -->|No: Description| J[Descriptive Statistics]
    D -->|No: Space/Time| K[Geospatial / Temporal]

    E --> E1[Co-occurrence Networks]
    E --> E2[Structural Hole Analysis]
    
    G --> G1[Topic Modeling (LDA/BERTopic)]
    G --> G2[Sentiment/Emotion Analysis]
    G --> G3[Bias/Stance Embeddings]
    G --> G4[Semantic Decoupling Index]
    
    H --> H1[Panel Fixed Effects]
    H --> H2[Diff-in-Diff (DiD)]
    H --> H3[Regression Discontinuity (RDD)]
    H --> H4[Instrumental Variables (IV)]

    K --> K1[Spatial Autocorrelation (Moran's I)]
    K --> K2[Sequence Analysis]
```

---

## 1. Primary Research Question Classification

Start here. What is the fundamental nature of your inquiry?

*   **Structure & Relationship**: "How are concepts linked? Who influences whom?" -> **Jump to [Network Analysis]**
*   **Content & Meaning**: "What are they talking about? How is it framed?" -> **Jump to [NLP & Content Analysis]**
    *   *Sub-question*: "I need to code 50k tweets for specific stance." -> **Jump to [Automated Annotation]**
*   **Causality & Effect**: "Did event X change discourse Y? Does framing Z cause higher engagement?" -> **Jump to [Causal Inference]**
*   **Emergence & Dynamics**: "How does this rumor spread in a realistic population?" -> **Jump to [Agent-Based Modeling]**

---

## 2. Network Analysis (SNA)

**When to use**: Your theory is about *structure*, *connection*, *flow*, or *position*.

### A. Semantic Network Analysis (Text)
*   **Concept**: Words define meaning by the company they keep (Distributional Semantics).
*   **Logic**: Construct a network where Nodes=Words, Edges=Co-occurrence.
*   **Key Metrics**:
    *   *Modularity*: Are there distinct echo chambers or topical clusters?
    *   *Betweenness*: Which words bridge different discourses?
    *   *Density*: How conceptually tight is the discourse?
*   **Tools**: `networkx`, `community-louvain`.

### B. Social Network Analysis (Actors)
*   **Concept**: Social capital, influence, and diffusion.
*   **Nodes**: People, Accounts, Organizations.
*   **Key Metrics**:
    *   *Degree Centrality*: Popularity.
    *   *PageRank*: Influence/Prestige.
    *   *Structural Holes (Constraint)*: Brokerage power.

---

## 2. Natural Language Processing (NLP)

**When to use**: Your theory is about *content*, *framing*, *bias*, or *ideology*.

### A. Topic Modeling
*   **Goal**: Discover latent themes in a large corpus.
*   **Methods**:
    *   *LDA (Latent Dirichlet Allocation)*: Classical, probabilistic. Good for broad themes.
    *   *BERTopic*: BERT-based, dense clusters. Good for micro-topics and short text.
*   **Output**: Topic 1: [virus, vaccine, pandemic]; Topic 2: [economy, jobs, market].

### B. Embedding-Based Analysis (Bias/Stance)
*   **Goal**: Quantify subtle ideological slants.
*   **Logic**: "King" - "Man" + "Woman" = "Queen". Vectors capture relationships.
*   **Methods**:
    *   *Projection*: Project document vectors onto a "Conservative-Progressive" axis.
    *   *Semantic Decoupling*: Measure distance between "Standard Meaning" and "Observed Usage".

### C. Dictionary Methods
*   **Goal**: Count frequency of pre-defined concepts.
*   **Logic**: Bag-of-Words.
*   **Tools**: LIWC, Custom Dictionaries (e.g., Moral Foundations Dictionary).
*   **Pros**: Transparent, interpretable. **Cons**: Misses context, irony.

---

## 3. Automated Annotation (New Paradigm)

**Choice: How to scale qualitative coding?**

*   **Scenario A: High Definition / Low Ambiguity** (e.g., "Is this post about sports?")
    *   *Method*: **Zero-Shot Classification** (Bart-Large-MNLI) or **Keyword Dictionary**.
    *   *Pros*: Fast, cheap, reproducible.

*   **Scenario B: High Nuance / Complex Context** (e.g., "Is this populism or mere critique?")
    *   *Method*: **LLM Annotation (Prompt Engineering)**.
    *   *Strategy*: Use GPT-4/Claude-3 for Gold Standard -> Fine-tune small model (e.g., Mistral/Llama-3) for scale.
    *   *Validation*: **Strict Inter-Coder Reliability (ICR)** between LLM and Human.

## 4. Causal Inference with Text

**Choice: How to prove X caused Y with text involved?**

*   **Scenario A: Text is the Outcome** (e.g., "Did the policy change discussion quality?")
    *   *Method*: **Panel Fixed Effects** or **Interrupted Time Series (ITS)**.
    *   *Variable*: Semantic Density, Sentiment Score, Topic Prevalence.

*   **Scenario B: Text is the Confounder** (e.g., "Effect of Gender on Citations, controlling for Paper Topic")
    *   *Method*: **Double Machine Learning (DML)** / `DoWhy`.
    *   *Logic*: Use embeddings/topics as high-dimensional controls to block backdoor paths.

*   **Scenario C: Text is the Treatment** (e.g., "Does 'emotional' framing cause more shares?")
    *   *Method*: **CausalNLP** / **Meta-Learners** (S-Learner/T-Learner).
    *   *Logic*: Estimate Conditional Average Treatment Effect (CATE).

## 5. Classical Econometrics (Panel Data)

**When to use**: Your theory is about *impact* over *time* (No text variables, just structure).

*   **Panel Fixed Effects (FE)**: The Gold Standard for observational data.
*   **Use when**: You have repeated measures of the same units (Users, Cities) over time.
*   **Logic**: Controls for all time-invariant confounders (Culture, History, Personality).
*   **Equation**: $Y_{it} = \beta X_{it} + \alpha_i + \delta_t + \epsilon_{it}$.

### B. Difference-in-Differences (DiD)
*   **Use when**: A policy/shock affected one group but not another at a specific time.
*   **Key Assumption**: Parallel Trends (Pre-treatment trends were identical).

### C. Regression Discontinuity (RDD)
*   **Use when**: Treatment is assigned based on a strict cut-off (e.g., Score > 50).
*   **Logic**: Units just above (51) and just below (49) are virtually identical except for treatment.

## 6. Geospatial Analysis

**When to use**: Your theory involves *location*, *distance*, or *neighborhood effects*.

*   **Spatial Autocorrelation**: "Is poverty clustered?" (Moran's I).
    *   *Logic*: Check if values at location $i$ are correlated with values at neighbors $j$.
*   **Geographically Weighted Regression (GWR)**: "Does the effect of X on Y vary by location?"
    *   *Logic*: Run regressions locally for each region.

## 7. Agent-Based Modeling (ABM)

**When to use**: You want to explain *macro-emergence* from *micro-interactions* (e.g., Segregation, Polarization).
*   **Schelling Model**: Show how slight strict preferences lead to total segregation.
*   **Opinion Dynamics**: Deffuant / Hegselmann-Krause models.
