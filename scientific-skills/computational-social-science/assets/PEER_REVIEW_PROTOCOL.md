# Internal Peer Review Protocol (The "Red Team")

> **Purpose**: Stand in the shoes of "Reviewer #2" (The Hostile Reviewer). Before any manuscript leaves this lab, it must survive this interrogation.
> **Source**: Adapted from `academic-reviewer` skill for Computational Social Science.

## 1. The Identification Police (Causal Logic)

*   **Reviewer Question**: "Is the observed effect purely due to the treatment, or is it selection bias?"
*   [ ] **Endogeneity Check**:
    *   If using OLS: Did you control for all confounders? If not, what unobserved variable could kill your result?
    *   *Defense*: "We ran a sensitivity analysis (Oster's $\delta$) showing bias would need to be 3x stronger than observed controls."
*   **The "Bad Control" Trap**:
    *   Did you control for a variable occurring *after* the treatment (e.g., Mediator)?
    *   *Rule*: Never control for outcomes.
*   **SUTVA / Spillover**:
    *   In a social network, did Treatment Group users talk to Control Group users?
    *   *Check*: Verify network distance required to assume independence.

## 2. GenAI / Content Analysis Validity

*   **Reviewer Question**: "Are these LLM annotations just hallucinations or noise?"
*   [ ] **Validation Gold Standard**:
    *   Where is the Confusion Matrix vs. Human Experts?
    *   *Requirement*: F1-Score > 0.8 on strict test set.
*   [ ] **Prompt Rigor**:
    *   Was `temperature=0` used?
    *   Did you change the prompt mid-stream? (Drift check).
*   [ ] **Concept Drift**:
    *   Does the definition of "Hate Speech" change between 2010 and 2024?
    *   *Defense*: Use time-invariant anchor terms or dynamic embeddings.

## 3. Statistical Inference & Robustness

*   **Reviewer Question**: "Is this p-value hacking?"
*   [ ] **Multiple Hypothesis Testing**:
    *   If you tested 10 outcomes and reported the 1 significant one...
    *   *Correction*: Apply Bonferroni or False Discovery Rate (FDR) correction.
*   [ ] **Clustering**:
    *   "Standard Errors Clustered at [Level]."
    *   *Rule*: Cluster at the level of assignment (e.g., User, not Tweet).
*   [ ] **Placebo Tests**:
    *   If you randomize a fake treatment, is the effect Zero? (It MUST be Zero).

## 4. Theoretical Coherence (The "So What?")

*   **Reviewer Question**: "This is just strict description. Where is the theory?"
*   [ ] **Mechanism**:
    *   Can you empirically distinguish *why* X causes Y?
    *   *Action*: Test the Mediator ($M$).
*   [ ] **Novelty**:
    *   Is this extending *Nature* (2023) or just replicating it?

## 5. Final Verdict Simulation

*   **[ ] Accept**: Flawless execution, novel theory.
*   **[ ] Minor Revision**: Needs better robustness checks or clarity.
*   **[ ] Major Revision**: Identification strategy is weak but fixable (e.g., add new controls).
*   **[ ] Reject**: Fatal flaw (Endogeneity, Bad Controls, Hallucinated Data).

---
*Signed: Internal Reviewer (Self)*
