# Reproducibility & Robustness Checklist

> **Code-as-Truth**: Before showing any result to the PI, verify against this list.

## 1. Data Integrity
- [ ] **Raw Data Immutable**: Verify that scripts NEVER write to the `data/raw` folder.
- [ ] **Config Separation**: Are all magic numbers (dates, thresholds) in `config.json`?
- [ ] **Audit Trail**: Does the ETL script log exactly how many rows were dropped and why?
- [ ] **Type Safety**: Are categorical variables actually cast as `category` (not string)?

## 2. Analysis Rigor
- [ ] **Seed Fixed**: Is `random_state=42` set for all stochastic processes (LDA, t-SNE, Train/Test Split)?
- [ ] **Code-Output Sync**: Did you re-run the *entire* pipeline from scratch (`Raw -> Result`) before taking the screenshot?
- [ ] **Unit Tests**: Did you sanity check the variables? (e.g., Is Age > 0? Is Probability between 0 and 1?).
## 2.5 GenAI & LLM Rigor (New Standard)
- [ ] **Temperature Zero**: Is `temperature=0` hardcoded? (Unless generating creative fiction).
- [ ] **Model Version Pinned**: Do NOT use `gpt-4` or `gemini-pro`. Use specific snapshots: `gemini-2.0-pro-001`, `claude-3-opus-20240229`.
- [ ] **Prompt Auditing**: Is the System Prompt versioned? (`prompts/v1` vs `prompts/v2`).
- [ ] **Stochasticity Check**: Did you run the same prompt on 20 examples 5 times to check stability?
- [ ] **Hallucination Guard**: Does the prompt explicitly say "Output 'NA' if unclear"?

## 3. Visualization "Nature" Standard
- [ ] **Font**: Arial/Helvetica only.
- [ ] **Resolution**: 300+ DPI.
- [ ] **Clarity**: No "chartjunk" (3D effects, unnecessary shadows).
- [ ] **Captions**: Does the figure file name match the script that generated it?

## 4. Robustness
- [ ] **Placebo**: Did you run a placebo test? (e.g., Randomized treatment, pre-treatment analysis).
- [ ] **Sensitivity**: If you change the `time_window` by 1 month, does the result hold?
- [ ] **Outliers**: Did you check if the result is driven by the top 1% of data?
