# Quickstart Guide

Get started with Tork Governance in minutes.

## Installation

```bash
pip install tork-governance
```

## Basic Usage

Evaluate a payload against a simple policy:

```python
from tork.core.engine import GovernanceEngine

# Initialize the engine
engine = GovernanceEngine()

# Evaluate a payload
payload = {"user_input": "My phone number is 555-123-4567"}
result = engine.evaluate(payload)

print(f"Decision: {result.decision}")
print(f"Modified Payload: {result.modified_payload}")
```

## Running the Playground

Start the interactive web UI to test your policies:

```bash
tork playground
```
Then visit `http://localhost:5000` in your browser.

## CLI Commands

Scan a directory for security vulnerabilities:

```bash
# Scan a directory
tork scan ./configs

# Check the version
tork --version
```
