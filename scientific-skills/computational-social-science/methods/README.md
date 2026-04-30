# CSS Advanced Methods Catalog

This directory contains specialized guides for "State-of-the-Art" (SOTA) Computational Social Science methods.

## Index

1.  **[Structural Topic Modeling (STM)](structural_topic_modeling.md)**
    *   **Goal**: Estimate how covariates (Party, Time, Gender) affect topic prevalence and content.
    *   **Tools**: `BERTopic` (Python), `stm` (R).
    
2.  **[Geospatial CSS](geospatial_css.md)**
    *   **Goal**: Analyze spatial inequality, polarization, and neighborhood effects.
    *   **Tools**: `geopandas`, `pysal` (Moran's I, GWR).

3.  **[Agent-Based Modeling (ABM)](agent_based_modeling.md)**
    *   **Goal**: Simulate emergent macro-phenomena from micro-interactions.
    *   **Tools**: `Mesa` (Python), `DSPy` (Cognitive Agents).

4.  **[Causal Inference with Text](causal_text_inference.md)**
    *   **Goal**: Estimate causal effects when text is a high-dimensional confounder.
    *   **Tools**: `DoWhy`, `EconML` (Double Machine Learning).

5.  **[Advanced Network Modeling](advanced_network_modeling.md)**
    *   **Goal**: Infer *mechanisms* of network formation (Homophily vs. Balance).
    *   **Tools**: `statnet/ergm` (R), `RSiena` (Longitudinal).

6.  **[Conjoint Analysis](conjoint_analysis.md)**
    *   **Goal**: Disentangle multidimensional preferences (Survey Experiments).
    *   **Tools**: `statsmodels` (Python), `cregg` (R).

7.  **[Multimodal CSS](multimodal_css.md)**
    *   **Goal**: Analyze images/video as high-dimensional social data.
    *   **Tools**: `CLIP` (Transformers), `Torch`.

## Usage
Refer to these guides when your `RESEARCH_DESIGN_MASTER.md` calls for specialized analysis beyond standard regression or NLP.
