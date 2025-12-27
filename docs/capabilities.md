# Capabilities

Agent capability labels with proficiency levels and task matching.

## Overview

The Capabilities module provides a system for labeling AI agents with their capabilities and proficiency levels, then matching tasks to the best-suited agents. This enables intelligent task routing based on agent strengths.

## Core Concepts

### CapabilityLevel

Four proficiency levels:

```python
from tork.capabilities import CapabilityLevel

CapabilityLevel.BASIC        # Entry-level proficiency
CapabilityLevel.INTERMEDIATE # Moderate proficiency
CapabilityLevel.ADVANCED     # High proficiency
CapabilityLevel.EXPERT       # Top-tier proficiency
```

### PerformanceMetric

Six performance dimensions:

```python
from tork.capabilities import PerformanceMetric

PerformanceMetric.SPEED      # Response latency
PerformanceMetric.ACCURACY   # Correctness of outputs
PerformanceMetric.CREATIVITY # Novel solutions
PerformanceMetric.SAFETY     # Avoiding harmful outputs
PerformanceMetric.COST       # Token/API efficiency
PerformanceMetric.CONTEXT    # Long context handling
```

### AgentCapability

Define a single capability:

```python
from tork.capabilities import AgentCapability, CapabilityLevel

capability = AgentCapability(
    name="code_generation",
    level=CapabilityLevel.EXPERT,
    score=0.95,
    verified=True,
)
```

### AgentProfile

Complete agent profile with capabilities and metrics:

```python
from tork.capabilities import AgentProfile, PerformanceMetric

profile = AgentProfile(
    agent_id="gpt-4",
    model="gpt-4",
    capabilities=[
        AgentCapability("reasoning", CapabilityLevel.EXPERT, 0.95),
        AgentCapability("coding", CapabilityLevel.ADVANCED, 0.85),
        AgentCapability("creative_writing", CapabilityLevel.ADVANCED, 0.80),
    ],
    performance_metrics={
        PerformanceMetric.ACCURACY: 0.92,
        PerformanceMetric.SAFETY: 0.95,
        PerformanceMetric.COST: 0.3,  # Higher cost
    },
    strengths=["complex reasoning", "code analysis"],
    weaknesses=["real-time data", "image generation"],
)
```

## CapabilityRegistry

Manage agent profiles:

```python
from tork.capabilities import CapabilityRegistry

registry = CapabilityRegistry()

# Register profiles
registry.register(gpt4_profile)
registry.register(claude_profile)
registry.register(llama_profile)

# Get a profile
profile = registry.get("gpt-4")

# List all profiles
all_profiles = registry.list_all()

# Filter by capability
coders = registry.filter_by_capability("coding", min_level=CapabilityLevel.ADVANCED)

# Filter by metric threshold
fast_agents = registry.filter_by_metric(PerformanceMetric.SPEED, min_score=0.8)
```

### Compare Agents

Compare capabilities between agents:

```python
comparison = registry.compare(["gpt-4", "claude-3-opus"])

for agent_id, profile in comparison.items():
    print(f"{agent_id}:")
    for cap in profile.capabilities:
        print(f"  {cap.name}: {cap.level.value} ({cap.score})")
```

## TaskMatcher

Find the best agent for a task:

```python
from tork.capabilities import TaskMatcher

matcher = TaskMatcher(registry)

# Define task requirements
result = matcher.match(
    task_description="Generate Python code for a REST API",
    required_capabilities=["coding", "api_design"],
    min_level=CapabilityLevel.ADVANCED,
    performance_priorities={
        PerformanceMetric.ACCURACY: 0.5,
        PerformanceMetric.SPEED: 0.3,
        PerformanceMetric.COST: 0.2,
    },
)

print(f"Best agent: {result.best_match}")
print(f"Confidence: {result.confidence}")
print(f"Reasoning: {result.reasoning}")
```

### Rank Multiple Agents

Get a ranked list of suitable agents:

```python
rankings = matcher.rank(
    task_description="Analyze legal documents",
    required_capabilities=["legal_analysis", "summarization"],
)

for rank, (agent_id, score) in enumerate(rankings, 1):
    print(f"{rank}. {agent_id}: {score:.2f}")
```

### Get Recommendations

Get detailed recommendations:

```python
recommendations = matcher.recommend(
    task_description="Creative marketing copy",
    max_results=3,
)

for rec in recommendations:
    print(f"Agent: {rec.agent_id}")
    print(f"Score: {rec.score}")
    print(f"Strengths for task: {rec.relevant_strengths}")
    print(f"Potential issues: {rec.potential_issues}")
```

## Default Profiles

Pre-configured profiles for popular models:

```python
from tork.capabilities.defaults import (
    gpt4_profile,
    gpt4_turbo_profile,
    claude3_opus_profile,
    claude3_sonnet_profile,
    gemini_pro_profile,
    llama3_profile,
)

registry = CapabilityRegistry()

# Load all defaults
registry.register(gpt4_profile())
registry.register(gpt4_turbo_profile())
registry.register(claude3_opus_profile())
registry.register(claude3_sonnet_profile())
registry.register(gemini_pro_profile())
registry.register(llama3_profile())
```

### Default Profile Characteristics

| Model | Strengths | Cost |
|-------|-----------|------|
| GPT-4 | Reasoning, coding, analysis | High |
| GPT-4 Turbo | Speed, long context | Medium |
| Claude 3 Opus | Safety, nuance, writing | High |
| Claude 3 Sonnet | Balance of speed/quality | Medium |
| Gemini Pro | Multimodal, reasoning | Medium |
| Llama 3 | Open source, customizable | Low |

## Example: Building a Task Router

```python
from tork.capabilities import CapabilityRegistry, TaskMatcher
from tork.capabilities.defaults import (
    gpt4_profile,
    claude3_opus_profile,
    llama3_profile,
)

# Set up registry with available models
registry = CapabilityRegistry()
registry.register(gpt4_profile())
registry.register(claude3_opus_profile())
registry.register(llama3_profile())

# Create matcher
matcher = TaskMatcher(registry)

# Route different tasks
def route_task(task: str, capabilities: list[str]) -> str:
    result = matcher.match(
        task_description=task,
        required_capabilities=capabilities,
    )
    return result.best_match

# Examples
code_agent = route_task("Write a Python script", ["coding"])
legal_agent = route_task("Analyze this contract", ["legal_analysis"])
creative_agent = route_task("Write a poem", ["creative_writing"])
```

## Integration with Routing

Combine with the Routing module:

```python
from tork.capabilities import TaskMatcher
from tork.routing import SectorRouter

# Match capabilities first
best_agent = matcher.match(task, capabilities).best_match

# Then route based on sector
router = SectorRouter()
route = router.route(context, target_agent=best_agent)
```
