# Conjoint Analysis (Survey Experiments)

**Goal**: Disentangle multidimensional preferences. "What attributes of a candidate/product matter most?"

## 1. The Logic
Asking "Do you like Candidate A?" is biased.
Instead, present two profiles with randomized attributes:
*   **Profile A**: [Democrat, Female, Moderate, 40yo]
*   **Profile B**: [Republican, Male, Extreme, 60yo]
By analyzing thousands of choices, we estimate the **Average Marginal Component Effect (AMCE)**.

---

## 2. Python Pattern: OLS with Dummies (cjmodels)

In Conjoint Analysis, because attributes are fully randomized (independent), simple OLS performs exceptionally close to complex logit models for estimating AMCE.

```python
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

# Data Structure: Long Format
# Each row is ONE profile seen by ONE respondent.
# y = 1 (Chosen), 0 (Not Chosen)
# cols = all attributes dummies

# 1. Load Data
df = pd.read_csv("data/processed/conjoint_data.csv")

# 2. Variable Selection (Get Dummies)
# Pandas get_dummies automatically handles categorical variables
X = pd.get_dummies(df[['party', 'gender', 'policy_stance', 'age']], drop_first=True)
y = df['chosen']
X = sm.add_constant(X)

# 3. Estimate AMCE (Clustered SEs by Respondent)
model = sm.OLS(y, X).fit(cov_type='cluster', cov_kwds={'groups': df['respondent_id']})

print(model.summary())

# 4. Visualization (Forest Plot)
# Plot coefficients with 95% CIs
coefs = model.params.drop('const')
errors = model.bse.drop('const')

fig, ax = plt.subplots(figsize=(6, 8))
coefs.plot(kind='barh', xerr=errors*1.96, ax=ax, color='black', capsize=3)
ax.axvline(x=0, color='grey', linestyle='--')
ax.set_xlabel("Average Marginal Component Effect (AMCE)")
plt.savefig("figures/amce_plot.png")
```

## 3. R Pattern: `cregg` (Specialized)

For publication-ready (Nature/Science) plots and subgroup analysis (Marginal Means), R's `cregg` is superior.

```r
library(cregg)
library(ggplot2)

# Load Data
data(immigration) # Example dataset

# Estimate AMCEs
# formula: Chosen ~ Gender + Education + Language + Origin
mm <- cj(immigration, Chosen ~ Gender + Education + Language + Origin, id = ~CaseID)

# Plot
plot(mm) + 
  theme_bw() + 
  labs(x = "AMCE")
```

## 4. Best Practices
*   **Randomization Integrity**: Ensure your survey platform (Qualtrics) truly randomized the attributes.
*   **Attention Checks**: Filter out respondents who failed simple attention checks ("Click 'Disagree'").
*   **Subgroup Analysis**: "Do Republicans prefer different attributes than Democrats?" (Interaction Effects).
