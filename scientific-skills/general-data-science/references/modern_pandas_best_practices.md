# Modern Pandas Best Practices (The "Vectorized" Way)

**Goal**: Write Pandas code that is fast, readable, and production-ready.
**Target Version**: Pandas 2.0+

## 1. Vectorization is Non-Negotiable
*   **Legacy**: Using `df.iterrows()` or `for i in range(len(df))`. (Slow, Python-speed).
*   **Modern**: Use Vectorized Operations. (Fast, C-speed).

### Basic Arithmetic
```python
# BAD
for i, row in df.iterrows():
    df.at[i, 'C'] = row['A'] * row['B']

# GOOD
df['C'] = df['A'] * df['B']
```

### Complex Logic (Apply vs Vectorized)
If you have complex `if-else` logic:
```python
# BAD (Apply is just a hidden loop)
df['category'] = df['age'].apply(lambda x: 'Adult' if x > 18 else 'Child')

# GOOD (Numpy Select / Where)
import numpy as np
df['category'] = np.where(df['age'] > 18, 'Adult', 'Child')
```

## 2. Method Chaining (The Functional Style)
Avoid creating intermediate variables (`df_temp`, `df2`). Use the Fluent Interface.

```python
# OLD WAY (Mutating State)
df = load_data()
df = df.dropna()
df['log_x'] = np.log(df['x'])
df = df[df['log_x'] > 0]
plot(df)

# MODERN WAY (Chaining)
(
    load_data()
    .dropna()
    .assign(log_x=lambda x: np.log(x['x']))
    .query("log_x > 0")
    .pipe(plot)
)
```
*   **assign()**: Create new columns.
*   **query()**: Filter rows (SQL-style string).
*   **pipe()**: Pass the dataframe to a custom function.

## 3. Strict Typing (Pandas 2.0 / Arrow)
Use strict types to save memory and catch bugs.

*   **Strings**: Use `dtype="category"` (for low cardinality) or `string[pyarrow]`.
*   **Integers**: Use `Int64` (Capital 'I') which supports `NaN`. (Standard `int` crashes on null).

```python
df = pd.read_parquet(
    "data.parquet", 
    dtype_backend="pyarrow"
)
```

## 4. File Formats
*   **CSV**: Avoid for intermediate storage. No types, slow (text parsing).
*   **Parquet**: The Gold Standard. Types preserved, compression (Snappy), fast I/O.
*   **Feather**: Faster than Parquet for ephemeral transfer, but less compatible.

## 5. Aggregation
Use `.groupby().agg()` with named tuples for clarity.

```python
# BAD
df.groupby('group')['value'].mean()

# GOOD (Explicit naming)
(
    df.groupby('group')
    .agg(
        mean_val=('value', 'mean'),
        count_val=('value', 'count')
    )
    .reset_index()
)
```
