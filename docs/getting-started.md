# Getting Started

Get up and running with Tork Governance in minutes.

## Installation

```bash
pip install tork-governance
```

For optional framework integrations:

```bash
pip install tork-governance[langchain]    # LangChain integration
pip install tork-governance[crewai]       # CrewAI integration
pip install tork-governance[autogen]      # AutoGen integration
pip install tork-governance[openai]       # OpenAI Agents SDK
pip install tork-governance[all]          # All integrations
```

## Quick Start

### Basic Policy Evaluation

```python
from tork import GovernanceEngine
from tork.core.models import EvaluationRequest, PolicyDecision

# Create engine
engine = GovernanceEngine()

# Evaluate a request
request = EvaluationRequest(
    payload={"message": "Hello world"},
    agent_id="my-agent",
    action="chat",
)

result = engine.evaluate(request)

if result.decision == PolicyDecision.ALLOW:
    print("Request allowed")
elif result.decision == PolicyDecision.DENY:
    print("Request denied")
elif result.decision == PolicyDecision.REDACT:
    print(f"Redacted: {result.modified_payload}")
```

### PII Redaction

```python
from tork.core.redactor import PIIRedactor

redactor = PIIRedactor()

text = "Contact john@example.com or call 555-123-4567"
redacted = redactor.redact_text(text)
print(redacted)  # Contact [EMAIL REDACTED] or call [PHONE REDACTED]
```

### Security Scanning

```python
from tork.scanner import MCPScanner

scanner = MCPScanner()
results = scanner.scan_file("config.yaml")

for finding in results:
    print(f"{finding.severity}: {finding.message}")
```

## Core Concepts

### Policies

Policies define rules for allowing, denying, or redacting content:

```yaml
name: content-filter
priority: 10
rules:
  - field: "message"
    operator: "contains"
    value: "spam"
    action: "DENY"
```

### Agents

Every request is associated with an agent ID for tracking and auditing:

```python
request = EvaluationRequest(
    payload={"data": "..."},
    agent_id="assistant-v1",  # Track which agent made this request
    action="process",
)
```

### Compliance Receipts

All evaluations generate tamper-evident receipts:

```python
result = engine.evaluate(request)
receipt = result.receipt

print(f"Receipt ID: {receipt.receipt_id}")
print(f"Verified: {receipt.verify()}")
```

## Next Steps

- [Framework Integrations](integrations.md) - LangChain, CrewAI, AutoGen, OpenAI
- [Workflows](workflows.md) - Multi-step agent orchestration
- [Personas](personas.md) - Custom AI personas
- [API Reference](api.md) - Detailed documentation
