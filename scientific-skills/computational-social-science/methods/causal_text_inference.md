# Causal Inference with Text (Text-as-Data)

**Goal**: Move beyond "Correlation" to "Causality" when Text is involved.
**Scenario**: "Does using emotional language (Treatment) cause more retweets (Outcome), controlling for the topic (Confounder)?"

---

## 1. The Challenge
Text is high-dimensional. If you just control for "Topic", you miss subtle confounders.
*   **Naive Approach**: $Y \sim T + Topic$. (Omitted Variable Bias).
*   **SOTA Approach**: **Double Machine Learning (DML)**. Use the text embedding $Z$ to predicting both $T$ and $Y$, then regress the residuals.

---

## 2. Python Pattern: Double Machine Learning (DML)

Using `EconML` or `DoWhy`.

```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LassoCV, LogisticRegressionCV
from sklearn.ensemble import RandomForestRegressor
from econml.dml import LinearDML

# Load Data
# T = Binary Treatment (e.g., "Has Hashtag?")
# Y = Outcome (e.g., "Log Retweets")
# Z = High-Dim Text Embeddings (BERT Vectors, dim=768)
df = pd.read_parquet("data/processed/causal_df.parquet")

Y = df['y'].values
T = df['t'].values
X_text = np.stack(df['embedding'].values) # Confounders (Text)
W_controls = df[['author_followers', 'account_age']].values # Other Controls

# Double Machine Learning
# 1. Model Y ~ Text + Controls
# 2. Model T ~ Text + Controls
# 3. Partially out the non-linear effect of Text
est = LinearDML(
    model_y=RandomForestRegressor(),
    model_t=LogisticRegressionCV(),
    discrete_treatment=True,
    random_state=42
)

est.fit(Y, T, X=None, W=np.hstack([X_text, W_controls]))

# Get Effect
effect = est.effect(X=None) # Average Treatment Effect (ATE)
summary = est.summary()
print(summary)
```

## 3. Causal Discovery (DAGs)

Before running regressions, use **Causal Discovery** to find the graph structure.

```python
import cdt
from cdt.causality.graph import LiNGAM

# LiNGAM assumes linear non-Gaussian data
# Input: Dataframe of numeric variables
obj = LiNGAM()
output_graph = obj.predict(df_numeric)

# Visualize
import networkx as nx
nx.draw_networkx(output_graph)
```

## 4. Checklist for Rigor
*   [ ] **Positivity Assumption**: Do we have treated/untreated units for all types of text? (Check Propensity Score overlap).
*   [ ] **Sensitivity Analysis**: Run `DoWhy` refuters (Placebo Treatment).
