# Research Design Master: [Project Title]

> **Macro-First Principle**: This document is the "Constitution" of the project. No analysis begins until this design is stable. Any change in logic must be updated here first.

## 1. Introduction & Problem Statement
*   **Research Question (RQ)**: What is the core causal or descriptive question?
*   **Significance**: Why does this matter for *Nature/Science* or *NM&S* audience?
*   **Literature Gap**: What specific void are we filling?

## 2. Theoretical Framework (The "Why")
*   **Core Concepts**:
    *   Concept A (e.g., Digital Labor): [Definition]
    *   Concept B (e.g., Algorithmic Alienation): [Definition]
*   **Hypotheses**:
    *   $H_1$: [Causal claim]
    *   $H_2$: [Mechanism claim]

## 3. Identification Strategy (The "How")
*   **Design Type**: (e.g., Panel Fixed Effects, DID, RDD, Textual Analysis)
*   **Causal DAG**:
    ```mermaid
    graph LR
    X[Treatment] --> Y[Outcome]
    Z[Confounder] --> X
    Z --> Y
    M[Mechanism] --> Y
    X --> M
    ```
*   **Threats to Validity**:
    *   Endogeneity: [How we address it]
    *   Selection Bias: [How we address it]

## 4. Data Engineering Plan
*   **Data Source**: [Raw Data Path]
*   **Observation Unit**: (e.g., "User-Day", "Article", "Comment")
*   **Sampling Logic**: [Inclusion/Exclusion Criteria]

### Variable Dictionary
| Variable | Symbol | Construction Logic | Source |
| :--- | :--- | :--- | :--- |
| **Outcome** | $Y_{it}$ | [Formula/Code] | [File] |
| **Treatment** | $X_{it}$ | [Formula/Code] | [File] |
| **Control** | $Z_{it}$ | [Formula/Code] | [File] |
### 4.5. GenAI & LLM Methodology (for Content Analysis)
*   **Model Specification**:
    *   **Primary Model**: `Claude Opus 4.5` (Reasoning/Complex Coding) or `Gemini 3 Pro` (Long-Context/Multimodal).
    *   **Fallback/Scale**: `Llama-3-70b` (Local) for bulk processing after validation.
*   **Parameters**:
    *   `temperature`: 0.0 (Mandatory for reproducibility).
    *   `top_p`: 0.1
*   **Prompt Strategy**:
    *   **System Prompt**: Located in `prompts/system_v1.md`.
    *   **Chain-of-Thought**: Required for complex classification (e.g., "Reason first, then output JSON").
*   **Validation**:
    *   **Gold Standard**: Human coding of N=100 samples.
    *   **Metric**: Agreement (F1 / Cohen's Kappa) > 0.8 required before running full scale.

## 5. Analysis Plan (Pre-Registered)
### Main Models
1.  **Baseline**: $Y = \beta_0 + \beta_1 X + \epsilon$
2.  **Full Control**: $Y = \beta_0 + \beta_1 X + \gamma Z + \delta_t + \alpha_i + \epsilon$

### Robustness Checks (Mandatory)
*   [ ] **Placebo Test**: Randomize $X$.
*   [ ] **Subsample Analysis**: Test on [Group A] vs [Group B].
*   [ ] **Alternative Measure**: Use $Y'$ instead of $Y$.

## 6. Execution Log & Notes
*   [YYYY-MM-DD]: Initial Design Frozen.
*   [YYYY-MM-DD]: Adjusted DAG after pilot analysis showed collider bias.
