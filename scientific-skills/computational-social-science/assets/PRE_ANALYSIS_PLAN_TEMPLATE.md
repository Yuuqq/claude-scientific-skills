# Pre-Analysis Plan (PAP) Template

**Purpose**: Tie your hands *before* you see the data. Eliminate "p-hacking" and "Harking".
**Target**: Prepare this document for OSF (Open Science Framework) or *APSR* Registered Reports.

---

## 1. Abstract
*   **Research Question**: [1 sentence]
*   **Hypotheses**:
    *   H1: [Directional prediction]
    *   H2: [Directional prediction]

## 2. Data Collection Strategy
*   **Population**: Who? (e.g., active Twitter users in US).
*   **Sampling**: How will you select them? (e.g., Random 1% sample).
*   **Stopping Rule**: When do you stop collecting? (e.g., N=5,000 or Date=2026-01-01).
*   **Exclusion Criteria**: Who gets dropped? (e.g., Bots with < 5 followers).

## 3. Variables
*   **Dependent Variable (Y)**:
    *   *Concept*: e.g., "Political Polarization".
    *   *Operation*: "Cosine distance between User and Center vector, using `all-MiniLM-L6-v2`."
*   **Independent Variable (X)**:
    *   *Concept*: e.g., "Algorithm Exposure".
    *   *Operation*: "Binary: 1 if in Treatment Group, 0 if Control."
*   **Controls (Z)**:
    *   List ALL covariates. (Age, Gender, Activity Level).

## 4. Analysis Plan (The "Code-Contract")

### Primary Model
We will estimate the following OLS model:

$$ Y_i = \beta_0 + \beta_1 T_i + \beta_2 X_i + \epsilon_i $$

*   **Inference**: Robust Standard Errors clustered at the `User` level.
*   **Significance Level**: $\alpha = 0.05$ (Two-tailed).

### Multiple Testing Correction
Since we categorize "Polarization" into 3 sub-metrics, we will apply the **Benjamini-Hochberg (FDR)** correction.

### Heterogeneous Effects
We pre-register an interaction analysis for **Partisanship**:
$$ Y = \beta T + \gamma (T \times Party) + \dots $$
*We hypothesize exposure effects are stronger for Republicans.*

## 5. Robustness Checks
We commit to reporting the following checks in the Appendix:
1.  **Placebo Test**: Randomizing treatment labels 1,000 times.
2.  **Alternative Cutoffs**: Varying the "Bot" exclusion threshold (5, 10, 50 followers).
3.  **Model Class**: Re-running OLS with Logistic Regression (if Y is binary).

---
*Timestamp*: 2026-01-17
*Signed*: qcm
