# Data Quality Assurance (QA) Checklist

**Usage**: Run this manual audit before finalizing any `data/processed` dataset.

## 1. Schema Integrity
- [ ] **Column Names**: Are they snake_case? (e.g., `user_id`, not `UserID`).
- [ ] **Data Types**: 
    - [ ] Are IDs strings/categories? (Not integers).
    - [ ] Are dates actual `datetime64[ns]` objects?
    - [ ] Are categorical variables set to `category` dtype?
- [ ] **Unexpected Columns**: Are there any "Unnamed: 0" or temporary columns?

## 2. Completeness (Missing Data)
- [ ] **Primary Keys**: Ensure `id` columns have 0% missingness.
- [ ] **Key Variables**: Is missingness in critical columns (e.g., `date`, `group`) acceptable?
- [ ] **Coding**: Are missing values consistently `NaN`? (Not -999, "N/A", or "").

## 3. Uniqueness
- [ ] **Duplicates**: check `df.duplicated().sum()`. Should be 0.
- [ ] **Primary Key Constraint**: `df['id'].is_unique` must be True.

## 4. Validity (Business Logic)
- [ ] **Ranges**:
    - [ ] Dates: Are they within the project scope? (e.g., 2020-2025).
    - [ ] Numerical: Are values positive where required? (e.g., Price > 0).
- [ ] **categories**: Do columns contain only allowed values? (e.g., "Male", "Female", "Other").

## 5. Consistency
- [ ] **String Normalization**: Are "USA", "usa", and "U.S.A" unified?
- [ ] **Units**: Is `price` consistently in USD? Is `weight` in kg?

## 6. Privacy (PII)
- [ ] **Redaction**: Are Names, Emails, Phones removed/hashed?
- [ ] **Aggregation**: Is data aggregated to a safe level (k-anonymity)?
