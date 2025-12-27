# Workflows

Agent chaining and workflow orchestration with governance.

## Overview

The Workflows module enables you to define multi-step agent workflows where outputs from one step can be passed as inputs to the next. Each step is governed by policies and generates compliance receipts.

## Core Concepts

### WorkflowStep

A single step in a workflow:

```python
from tork.workflows import WorkflowStep

step = WorkflowStep(
    id="analyze",
    name="Analyze Data",
    agent_id="analyst-agent",
    input_mapping={"data": "previous.output"},
    timeout_seconds=60,
)
```

### WorkflowDefinition

A complete workflow with multiple steps:

```python
from tork.workflows import WorkflowDefinition

workflow = WorkflowDefinition(
    id="research-pipeline",
    name="Research Pipeline",
    steps=[step1, step2, step3],
    max_cost=10.0,
)
```

## WorkflowEngine

Execute workflows with governance:

```python
from tork.workflows import WorkflowEngine

engine = WorkflowEngine()

# Register agent executors
engine.register_executor("researcher", research_fn)
engine.register_executor("writer", write_fn)

# Execute the workflow
result = engine.execute(workflow, initial_input={"topic": "AI Safety"})
```

## WorkflowBuilder

Fluent API for building workflows:

```python
from tork.workflows import WorkflowBuilder

workflow = (
    WorkflowBuilder("my-workflow")
    .add_step(
        id="research",
        name="Research Topic",
        agent_id="researcher",
    )
    .add_step(
        id="write",
        name="Write Article",
        agent_id="writer",
        input_mapping={"research": "research.output"},
    )
    .add_step(
        id="review",
        name="Review Article",
        agent_id="reviewer",
        input_mapping={"article": "write.output"},
    )
    .with_max_cost(5.0)
    .build()
)
```

## Input Mapping

Pass outputs between steps:

```python
step = WorkflowStep(
    id="step2",
    name="Process",
    agent_id="processor",
    input_mapping={
        "data": "step1.output",        # From step1's output
        "context": "initial.context",   # From initial input
    },
)
```

## Human Approval Gates

Pause workflows for human review:

```python
step = WorkflowStep(
    id="approve",
    name="Approval Gate",
    agent_id="human",
    requires_approval=True,
)

# Engine will pause at this step
result = engine.execute(workflow, {"data": "..."})

if result.status == "paused":
    # Get human approval
    engine.resume(workflow.id, approved=True)
```

## Failure Strategies

Handle step failures:

```python
from tork.workflows import FailureStrategy

step = WorkflowStep(
    id="risky-step",
    failure_strategy=FailureStrategy.RETRY,
    max_retries=3,
)

# Available strategies:
# - STOP: Halt workflow on failure (default)
# - SKIP: Skip failed step, continue
# - RETRY: Retry with backoff
# - FALLBACK: Use fallback agent
```

## Cost Limits

Enforce budget constraints:

```python
workflow = WorkflowDefinition(
    id="budget-workflow",
    steps=[...],
    max_cost=10.0,  # Stop if total cost exceeds $10
)

# Each step tracks tokens and cost
result = engine.execute(workflow, {...})
print(f"Total cost: ${result.total_cost}")
```

## Pre-built Templates

Ready-to-use workflow patterns:

```python
from tork.workflows.templates import (
    research_critique_rewrite,
    multi_agent_consensus,
    review_and_approve,
)

# Research → Critique → Rewrite pipeline
workflow = research_critique_rewrite()

# Multi-agent consensus workflow
workflow = multi_agent_consensus(agent_ids=["agent1", "agent2", "agent3"])

# Review and approval workflow
workflow = review_and_approve(reviewer_id="senior-reviewer")
```

## Compliance Receipts

Each step generates a signed receipt:

```python
result = engine.execute(workflow, {...})

for step_result in result.step_results:
    receipt = step_result.receipt
    print(f"Step: {step_result.step_id}")
    print(f"Receipt ID: {receipt.receipt_id}")
    print(f"Signature: {receipt.signature}")
```

## Async Execution

Execute workflows asynchronously:

```python
async def run_workflow():
    engine = WorkflowEngine()
    result = await engine.execute_async(workflow, {"data": "..."})
    return result
```
