# Prompts

Agent-selectable prompts with multi-agent generation and selection.

## Overview

The Prompts module enables multiple AI agents to generate prompt candidates, which are then scored and selected based on quality criteria. This allows for iterative prompt improvement and multi-perspective prompt engineering.

## Core Concepts

### PromptType

Eight prompt types:

```python
from tork.prompts import PromptType

PromptType.SYSTEM       # System/persona prompts
PromptType.USER         # User query prompts
PromptType.ASSISTANT    # Assistant response templates
PromptType.CRITIQUE     # Critique/feedback prompts
PromptType.SYNTHESIS    # Combining multiple views
PromptType.REFINEMENT   # Improving existing prompts
PromptType.EXPANSION    # Adding detail
PromptType.COMPRESSION  # Summarizing/condensing
```

### PromptQuality

Five quality levels:

```python
from tork.prompts import PromptQuality

PromptQuality.EXCELLENT    # Top tier (score >= 0.85)
PromptQuality.GOOD         # High quality (score >= 0.70)
PromptQuality.ACCEPTABLE   # Usable (score >= 0.50)
PromptQuality.POOR         # Below threshold (score < 0.50)
PromptQuality.REJECTED     # Safety issues (safety < 0.50)
```

### PromptCandidate

A generated prompt with scores:

```python
from tork.prompts import PromptCandidate, PromptType, PromptQuality

candidate = PromptCandidate(
    prompt_type=PromptType.SYSTEM,
    content="You are an expert assistant...",
    generator_agent="gpt-4",
    generator_model="gpt-4-turbo",
    quality=PromptQuality.GOOD,
    clarity_score=0.85,
    specificity_score=0.80,
    safety_score=0.95,
    token_count=50,
)
```

### PromptSelectionCriteria

Criteria for selecting prompts:

```python
from tork.prompts import PromptSelectionCriteria, PromptQuality

criteria = PromptSelectionCriteria(
    min_clarity=0.6,
    min_specificity=0.5,
    min_safety=0.8,
    max_tokens=1000,
    preferred_generators=["gpt-4", "claude-3"],
    blocked_generators=["untrusted-model"],
    prefer_quality=PromptQuality.GOOD,
    clarity_weight=0.3,
    specificity_weight=0.3,
    safety_weight=0.4,
)
```

## PromptGenerator

Generate prompts using agents:

```python
from tork.prompts import PromptGenerator, PromptType

generator = PromptGenerator()

# Register agent executors
def gpt4_executor(meta_prompt):
    # Call GPT-4 API
    return {"content": response, "model": "gpt-4"}

generator.register_executor("gpt-4", gpt4_executor)

# Generate a single prompt
candidate = generator.generate(
    task="Create a customer service chatbot",
    prompt_type=PromptType.SYSTEM,
    agent_id="gpt-4",
    context="E-commerce platform",
)

print(f"Content: {candidate.content}")
print(f"Quality: {candidate.quality}")
```

### Generate Multiple Candidates

```python
# Generate from multiple agents
candidates = generator.generate_multiple(
    task="Write a code review prompt",
    prompt_type=PromptType.SYSTEM,
    agent_ids=["gpt-4", "claude-3", "gemini"],
)

for c in candidates:
    print(f"{c.generator_agent}: {c.quality.value}")
```

## PromptSelector

Select the best prompt:

```python
from tork.prompts import PromptSelector

selector = PromptSelector()

# Select best from candidates
result = selector.select(candidates, criteria)

print(f"Selected: {result.selected.content}")
print(f"Confidence: {result.confidence}")
print(f"Reasoning: {result.selection_reasoning}")
```

### Rank Candidates

```python
# Get all candidates ranked by quality
ranked = selector.rank(candidates, criteria)

for i, candidate in enumerate(ranked, 1):
    print(f"{i}. {candidate.generator_agent}: {candidate.quality.value}")
```

## PromptOrchestrator

End-to-end prompt generation and selection:

```python
from tork.prompts import PromptOrchestrator, PromptType

orchestrator = PromptOrchestrator()

# Register executors
orchestrator.generator.register_executor("gpt-4", gpt4_fn)
orchestrator.generator.register_executor("claude-3", claude_fn)

# Generate and select in one call
result = orchestrator.orchestrate(
    task="Create an AI tutor prompt",
    prompt_type=PromptType.SYSTEM,
    agent_ids=["gpt-4", "claude-3"],
    criteria=criteria,
    context="For high school math students",
)

print(f"Best prompt: {result.selected.content}")
```

### Refine Prompts

Improve existing prompts:

```python
# Take a prompt and refine it
refined = orchestrator.refine(
    prompt=result.selected,
    refiner_agent="gpt-4",
    feedback="Make it more encouraging for struggling students",
)

print(f"Refined: {refined.content}")
print(f"Original ID: {refined.metadata['original_id']}")
```

### Iterative Improvement

Keep refining until quality threshold:

```python
# Iterate until GOOD quality or max iterations
result = orchestrator.iterate(
    task="Create a legal document analyzer",
    agent_ids=["gpt-4", "claude-3"],
    max_iterations=3,
    criteria=PromptSelectionCriteria(prefer_quality=PromptQuality.GOOD),
)

print(f"Final quality: {result.selected.quality}")
print(f"Iterations: {result.total_evaluated}")
```

## Meta-Prompt Templates

Pre-built templates for generating prompts:

```python
from tork.prompts import (
    critique_meta_prompt,
    synthesis_meta_prompt,
    refinement_meta_prompt,
    expansion_meta_prompt,
    compression_meta_prompt,
)

# Generate a critique prompt
meta = critique_meta_prompt(
    task="Review code for security vulnerabilities",
    context="Python web application",
)

# Generate a synthesis prompt
meta = synthesis_meta_prompt(
    task="Combine expert opinions on climate change",
)

# Refine an existing prompt
meta = refinement_meta_prompt(
    original="You are a helpful assistant.",
    feedback="Add expertise in data science",
)

# Expand a brief prompt
meta = expansion_meta_prompt(
    task="Answer questions",
    context="Customer support for a SaaS product",
)

# Compress a verbose prompt
meta = compression_meta_prompt(
    task="Very long and detailed prompt here...",
)
```

## Scoring

Prompts are automatically scored on three dimensions:

### Clarity Score (0-1)

Based on sentence structure and readability:

```python
# Higher clarity:
"You are an expert Python developer. Your task is to review code for bugs."

# Lower clarity:
"Do Python stuff with code things"
```

### Specificity Score (0-1)

Based on actionable details:

```python
# Higher specificity:
"You must identify security vulnerabilities including SQL injection, XSS, and CSRF."

# Lower specificity:
"Find problems in the code"
```

### Safety Score (0-1)

Penalized for unsafe patterns:

```python
# Prompts mentioning "hack", "exploit", "bypass", etc. get lower scores
```

## Governance Integration

All generated prompts pass through governance:

```python
from tork.core import GovernanceEngine

gov_engine = GovernanceEngine(policies=[pii_policy])
generator = PromptGenerator(governance_engine=gov_engine)

# PII in generated prompts will be redacted
candidate = generator.generate(task, prompt_type, agent_id)
```

## Example: Prompt Engineering Pipeline

```python
from tork.prompts import (
    PromptOrchestrator,
    PromptType,
    PromptSelectionCriteria,
    PromptQuality,
)

# Set up orchestrator
orchestrator = PromptOrchestrator()
orchestrator.generator.register_executor("gpt-4", gpt4_executor)
orchestrator.generator.register_executor("claude-3", claude_executor)

# Define quality criteria
criteria = PromptSelectionCriteria(
    min_clarity=0.7,
    min_specificity=0.6,
    min_safety=0.9,
    prefer_quality=PromptQuality.EXCELLENT,
)

# Generate candidates from multiple models
result = orchestrator.orchestrate(
    task="Create a medical triage assistant that asks symptoms and suggests urgency",
    prompt_type=PromptType.SYSTEM,
    agent_ids=["gpt-4", "claude-3"],
    criteria=criteria,
    context="For a telemedicine app, must be cautious and recommend seeing doctors",
)

# Check quality
if result.selected.quality != PromptQuality.EXCELLENT:
    # Refine until excellent
    result = orchestrator.iterate(
        task=result.selected.content,
        agent_ids=["gpt-4"],
        max_iterations=2,
        criteria=criteria,
    )

print(f"Final prompt: {result.selected.content}")
print(f"Quality: {result.selected.quality}")
print(f"Scores: clarity={result.selected.clarity_score}, specificity={result.selected.specificity_score}")
```
