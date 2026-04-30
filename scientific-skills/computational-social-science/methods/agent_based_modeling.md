# Agent-Based Modeling (ABM) for CSS

**Goal**: Simulate emergent social phenomena (Polarization, Segregation, Panic) by modeling individual agents.

## 1. The Logic of Generative Social Science
Instead of strictly analyzing variable correlations ($X \to Y$), we "grow" the phenomenon.
*   **Micro-Rule**: "I prefer to live near people like me."
*   **Macro-Result**: "Total Segregation." (Schelling, 1971)

---

## 2. Python Pattern: Mesa (The Standard)

Mesa is the Python alternative to NetLogo.

### A. The Setup (Schelling Segregation)

```python
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector

class SchellingAgent(Agent):
    def __init__(self, pos, model, agent_type):
        super().__init__(pos, model)
        self.pos = pos
        self.type = agent_type

    def step(self):
        similar = 0
        for neighbor in self.model.grid.neighbor_iter(self.pos):
            if neighbor.type == self.type:
                similar += 1
        
        # If unhappy, move to empty spot
        if similar < self.model.homophily:
            self.model.grid.move_to_empty(self)

class SchellingModel(Model):
    def __init__(self, width=20, height=20, density=0.8, homophily=3):
        self.grid = SingleGrid(width, height, torus=True)
        self.schedule = RandomActivation(self)
        self.homophily = homophily
        
        # Place agents
        for cell in self.grid.coord_iter():
            x, y = cell[1], cell[2]
            if self.random.random() < density:
                agent_type = 1 if self.random.random() < 0.5 else 0
                agent = SchellingAgent((x, y), self, agent_type)
                self.grid.place_agent(agent, (x, y))
                self.schedule.add(agent)

        self.datacollector = DataCollector(
            {"Happy": lambda m: self.count_happy(m)}
        )

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
```

## 3. The Future: LLM-Agents (Cognitive ABM)

Instead of hardcoded rules ("If similar < 3, move"), we give agents a **Brain**.

### Pattern: DSPy Agents

```python
class CognitiveAgent(dspy.Module):
    def __init__(self, persona):
        self.persona = persona # "You are a working class voter..."
        self.memory = []
        
    def decide_vote(self, news_feed):
        # The agent "thinks" based on persona + memory + input
        thought = dspy.ChainOfThought("Please reflect on the news based on your values.")(
            persona=self.persona, 
            news=news_feed
        )
        return thought
```
*   **Advantage**: Realistic adherence to complex psychology.
*   **Cost**: Very slow and expensive compared to Rule-Based ABM.

## 4. Calibration & Validation
*   **Calibration**: Adjust parameters (homophily threshold) until the simulation matches historical data.
*   **Validation**: Does the simulation predict *future* unseen data?
