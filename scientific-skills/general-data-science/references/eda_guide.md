# The Systematic EDA Protocol

**Goal**: Profile data to understand its "Physics" before blindly running models.
**Philosophy**: EDA is not just "plotting histograms". It is "Quality Assurance".

## Phase 1: The "Health Check" (Pre-Analysis)
Before you plot anything, check the pulse.

1.  **Shape & Types**: 
    *   Do we have 1M rows or 100? 
    *   Are IDs numerical or string? (Fix these in ETL).
2.  **Missingness Map**:
    *   Is missingness random (MCAR) or systemic?
    *   *Action*: Visualize using `msno.matrix(df)`.
3.  **Duplication**:
    *   Are there duplicate Primary Keys?
    *   *Action*: `df[df.duplicated(subset=['id'], keep=False)]`.

## Phase 2: Univariate Profiling
Analyze one variable at a time.

### Categorical
*   **Cardinality**: High cardinality (e.g., User Agents) needs grouping.
*   **Rare Labels**: Labels with < 1% frequency should often be grouped into "Other".

### Numerical
*   **Distribution**: Gaussian vs. Power Law (Log-normal).
    *   *Action*: If Skew > 1, try `np.log1p()`.
*   **Outliers**:
    *   *Tukey's Fences*: $Q3 + 1.5 * IQR$. (Conservative).
    *   *Z-Score*: $> 3$ SDs. (Assumes Normality).

## Phase 3: Bivariate Relations (Signal Hunting)
"Does X correlate with Y?"

*   **Continuous vs Continuous**: Scatterplot + Correlation Matrix.
*   **Categorical vs Continuous**: Boxplot per category.
*   **Time Series**: Line plot with Rolling Mean.

## Phase 4: The "Sanity" Check
Does the data make *sense* in reality?
*   *Example*: "Age" column has a max of 200. (Impossible).
*   *Action*: Define business rules and filter.

## Tools
*   **Pandas Profiling / YData Profiling**: Great for automated reports.
    *   *Note*: Can be slow on large data.
*   **Sweetviz**: Good for Train vs Test comparison.
*   **Great Expectations**: For rigorous production data validation.
