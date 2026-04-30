# SOTA Topic Modeling: STM & Dynamic BERTopic

**Goal**: Go beyond "What are the topics?" to "How do topics vary by Author/Time?"

## 1. The Methodological Shift
*   **Old Way (LDA)**: "Here is a bag of words." (Static)
*   **SOTA Way (STM/BERTopic)**: "Here is a bag of words + Metadata (Party, Date, Gender)."
    *   *Question*: "Do Republicans use Topic A (Freedom) more than Democrats?"
    *   *Question*: "Did Topic B (Public Health) spike after 2020-03?"

---

## 2. Python Pattern: BERTopic (The Modern Standard)

BERTopic uses Transformers (Embeddings) + c-TF-IDF to find dense, coherent styles.

### A. Setup
```bash
pip install bertopic
```

### B. Analytical Pipeline

```python
from bertopic import BERTopic
import pandas as pd

# Load Data (Text + Covariates)
df = pd.read_parquet("data/processed/corpus.parquet")
docs = df['text'].tolist()
timestamps = df['date'].tolist()
measurements = df['party_id'].tolist() # Categorical covariate

# 1. Initialize & Fit
# 'all-MiniLM-L6-v2' is fast and efficient for English.
topic_model = BERTopic(language="english", calculate_probabilities=True, verbose=True)
topics, probs = topic_model.fit_transform(docs)

# 2. Dynamic Topic Modeling (Time Effect)
topics_over_time = topic_model.topics_over_time(docs, timestamps, nr_bins=20)
topic_model.visualize_topics_over_time(topics_over_time)

# 3. Covariate Analysis (The "STM" Equivalent)
# "How does 'Party' affect topic distribution?"
topics_per_class = topic_model.topics_per_class(docs, classes=measurements)
topic_model.visualize_topics_per_class(topics_per_class)
```

---

## 3. R Pattern: Structural Topic Modeling (The Political Science Gold Standard)

If you are submitting to *APSR* or *AJPS*, reviewers may still strictly prefer R's `stm` package because it formalizes the probabilistic model of covariates.

### A. R Script Template

```r
library(stm)
library(tm)

# 1. Ingest
metadata <- read.csv("corpus.csv")
processed <- textProcessor(metadata$text, metadata = metadata)
out <- prepDocuments(processed$documents, processed$vocab, processed$meta)

# 2. Structural Model
# prevalence =~ Party + s(Year): Covariates affect topic frequency
# content =~ Party: Covariates affect word choice within topic (Framing)
model_fit <- stm(
  documents = out$documents, 
  vocab = out$vocab, 
  K = 20, 
  prevalence = ~ Party + s(Year), 
  data = out$meta, 
  init.type = "Spectral"
)

# 3. Estimate Effects
effect <- estimateEffect(1:20 ~ Party + s(Year), stmobj = model_fit, metadata = out$meta)
summary(effect)

# 4. Visualization (Difference Plot)
plot(effect, covariate = "Party", topics = c(1, 4, 7), model = model_fit, method = "difference",
     cov.value1 = "Republican", cov.value2 = "Democrat")
```

## 4. Reporting Checklist (Nature/Science Standard)
*   [ ] **Validation**: Did you run `find_topic_number` (coherence score) to justify $K$?
*   [ ] **Labeling**: Did you list top 10 Frex (Frequency-Exclusivity) words for each topic?
*   [ ] **Robustness**: Did you check results with a different seed or embedding model?
