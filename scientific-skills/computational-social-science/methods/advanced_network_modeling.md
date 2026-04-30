# Advanced Network Modeling (ERGM & SAOM)

**Goal**: Explain *why* the network looks like this. Is it just "Rich get Richer" (Preferential Attachment) or "Birds of a feather" (Homophily)?

## 1. Beyond Descriptive Metrics
Centrality and Density are **descriptive**. They don't test hypotheses.
*   **Descriptive**: "Node A has high centrality."
*   **Inferential**: "The probability of an edge forming increases by 20% if both nodes are the same Gender, controlling for structural balance."

---

## 2. The Gold Standard: ERGM (R Pattern)

Exponential Random Graph Models (ERGM) are the regression equivalent for networks.
*   **Python limitations**: `networkx` cannot do ERGMs. We must use R (`statnet`).

```r
library(statnet)
library(ergm)

# 1. Load Network
net <- network(adj_matrix, directed = FALSE)

# 2. Add Attributes
net %v% "party" <- meta$party
net %v% "gender" <- meta$gender

# 3. Model Specification
# edges: Intercept (Density)
# nodematch("party"): Homophily (Do same parties link?)
# gwesp: Transitivity (Do friends of friends become friends?) - Structural Balance
model <- ergm(net ~ edges + nodematch("party") + nodefactor("gender") + gwesp(0.5, fixed=TRUE))

# 4. Summary (Odd-Ratios)
summary(model)

# 5. Goodness of Fit (GoF)
# Does the model generate networks that look like the real one?
gof_res <- gof(model)
plot(gof_res)
```

## 3. Longitudinal Networks: RSiena (SAOM)

If you have network snapshots at Time 1, Time 2, Time 3...
*   **Stochastic Actor-Oriented Models (SAOM)**: Model the evolution of the network.
*   **Question**: "Did I become friends with X because he is influential (Selection), or did I become influential because I'm friends with X (Influence)?"

```r
library(RSiena)

# Define Data
array_nets <- array(c(adj1, adj2), dim=c(50, 50, 2))
mydata <- sienaDataCreate(sienaDependent(array_nets))

# Define Effects
myeff <- getEffects(mydata)
myeff <- includeEffects(myeff, transTrip) # Transitivity
myeff <- includeEffects(myeff, sameX, interaction1 = "party") # Homophily

# Estimate
myalg <- sienaAlgorithmCreate(projname = 'sim_study')
res <- siena07(myalg, data = mydata, effects = myeff)
summary(res)
```

## 4. Python Alternative: Graph-Tool (SBM)

If you strictly stick to Python, the closest rigorous alternative is **Stochastic Block Modeling (SBM)** using `graph-tool` (Linux/Mac optimized) or `graspologic`.

```python
# Stochastic Block Model (Inference of Community Structure)
import graph_tool.all as gt

g = gt.load_graph("my_graph.xml")
state = gt.minimize_blockmodel_dl(g)
state.draw(output="sbm_fit.png")
```
