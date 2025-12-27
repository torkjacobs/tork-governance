# Personas

Custom AI agent personas with governance-enforced execution.

## Overview

The Personas module allows you to define, store, and execute custom AI personas with specific capabilities, system prompts, and governance settings. Each persona can have its own cost limits, allowed/blocked actions, and behavior constraints.

## Core Concepts

### PersonaCapability

The 12 capability types a persona can have:

```python
from tork.personas import PersonaCapability

PersonaCapability.RESEARCH      # Information gathering
PersonaCapability.ANALYSIS      # Data analysis
PersonaCapability.CODING        # Code generation
PersonaCapability.LEGAL         # Legal advice
PersonaCapability.MEDICAL       # Medical information
PersonaCapability.FINANCIAL     # Financial analysis
PersonaCapability.CREATIVE      # Creative writing
PersonaCapability.TECHNICAL     # Technical writing
PersonaCapability.TRANSLATION   # Language translation
PersonaCapability.SUMMARIZATION # Content summarization
PersonaCapability.QA            # Question answering
PersonaCapability.CONVERSATION  # General conversation
```

### PersonaConfig

Define a persona's configuration:

```python
from tork.personas import PersonaConfig, PersonaCapability

config = PersonaConfig(
    id="legal-analyst",
    name="Legal Analyst",
    system_prompt="You are an expert legal analyst...",
    capabilities=[PersonaCapability.LEGAL, PersonaCapability.ANALYSIS],
    max_cost_per_request=1.0,
    allowed_actions=["analyze", "summarize", "cite"],
    blocked_actions=["provide_legal_advice"],
)
```

## PersonaStore

Persist and manage personas:

```python
from tork.personas import PersonaStore

store = PersonaStore(storage_path="./personas")

# Save a persona
store.save(config)

# Get a persona by ID
config = store.get("legal-analyst")

# List all personas
all_personas = store.list_all()

# Filter by capability
legal_personas = store.filter_by_capability(PersonaCapability.LEGAL)

# Delete a persona
store.delete("legal-analyst")
```

### Import/Export

Share personas between systems:

```python
# Export to JSON
json_data = store.export_json("legal-analyst")

# Export to YAML
yaml_data = store.export_yaml("legal-analyst")

# Import from JSON
store.import_json(json_data)

# Import from YAML
store.import_yaml(yaml_data)
```

## PersonaRuntime

Execute personas with governance:

```python
from tork.personas import PersonaRuntime

runtime = PersonaRuntime()

# Register an executor for the persona's model
runtime.register_executor("gpt-4", gpt4_executor)

# Execute the persona
result = runtime.execute(
    persona_id="legal-analyst",
    input_text="Analyze this contract clause...",
    store=store,
)

print(f"Output: {result.output}")
print(f"Tokens: {result.tokens_used}")
print(f"Cost: ${result.cost}")
```

### Session Tracking

Track persona usage across sessions:

```python
# Start a session
session = runtime.start_session("legal-analyst", store)

# Execute multiple requests
result1 = runtime.execute_in_session(session, "First question...")
result2 = runtime.execute_in_session(session, "Follow-up...")

# Get session stats
print(f"Total tokens: {session.total_tokens}")
print(f"Total cost: ${session.total_cost}")
print(f"Request count: {session.request_count}")

# End session
runtime.end_session(session)
```

## PersonaBuilder

Fluent API for building personas:

```python
from tork.personas import PersonaBuilder

config = (
    PersonaBuilder("code-reviewer")
    .with_name("Code Reviewer")
    .with_system_prompt("You are an expert code reviewer...")
    .with_capabilities([
        PersonaCapability.CODING,
        PersonaCapability.ANALYSIS,
    ])
    .with_max_cost(0.5)
    .allow_actions(["review", "suggest", "explain"])
    .block_actions(["execute_code", "modify_files"])
    .with_metadata({"language": "python", "style": "pep8"})
    .build()
)
```

## Pre-built Templates

Ready-to-use persona configurations:

```python
from tork.personas.templates import (
    legal_analyst,
    code_reviewer,
    research_assistant,
    content_writer,
    data_analyst,
    financial_advisor,
)

# Get a pre-configured legal analyst
config = legal_analyst()

# Get a code reviewer with custom settings
config = code_reviewer(
    languages=["python", "javascript"],
    max_cost=0.25,
)

# Get a research assistant
config = research_assistant(
    domains=["AI", "machine learning"],
)
```

## Governance Integration

Personas are governed by policies:

```python
from tork.core import GovernanceEngine

gov_engine = GovernanceEngine(policies=[pii_policy])
runtime = PersonaRuntime(governance_engine=gov_engine)

# PII in inputs/outputs will be redacted
# Blocked actions will be denied
result = runtime.execute("legal-analyst", "Review this contract...")
```

### Action Enforcement

Personas can only perform allowed actions:

```python
config = PersonaConfig(
    id="safe-assistant",
    allowed_actions=["answer", "explain"],
    blocked_actions=["execute_code", "access_files"],
)

# If persona tries to execute code, it will be blocked
result = runtime.execute("safe-assistant", "Run this Python code...")
# Result will contain a governance denial
```

## Compliance Receipts

Each execution generates a signed receipt:

```python
result = runtime.execute("legal-analyst", "Analyze...")

receipt = result.receipt
print(f"Receipt ID: {receipt.receipt_id}")
print(f"Persona: {receipt.agent_id}")
print(f"Action: {receipt.action}")
print(f"Signature: {receipt.signature}")
```

## Example: Building a Legal Review System

```python
from tork.personas import PersonaStore, PersonaRuntime, PersonaBuilder

# Create store and runtime
store = PersonaStore("./personas")
runtime = PersonaRuntime()

# Build specialized personas
contract_reviewer = (
    PersonaBuilder("contract-reviewer")
    .with_name("Contract Reviewer")
    .with_system_prompt("""
        You are an expert contract reviewer. Analyze contracts for:
        - Unusual clauses
        - Potential risks
        - Missing standard provisions
    """)
    .with_capabilities([PersonaCapability.LEGAL, PersonaCapability.ANALYSIS])
    .with_max_cost(2.0)
    .build()
)

# Save to store
store.save(contract_reviewer)

# Execute review
result = runtime.execute(
    "contract-reviewer",
    "Please review this employment contract: ...",
    store,
)

print(result.output)
```
