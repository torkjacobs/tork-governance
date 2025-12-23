# Tork Governance

A universal governance SDK for AI agents.

## Overview

Tork Governance provides a comprehensive framework for implementing governance, compliance, and identity management for AI agent systems.

## Installation

```bash
pip install tork-governance
```

## Quick Start

```python
from tork.core import GovernanceEngine
from tork.compliance import PolicyValidator

# Initialize the governance engine
engine = GovernanceEngine()

# Load and validate policies
validator = PolicyValidator()
validator.load_policies("templates/policies/")
```

## Project Structure

```
tork-governance/
├── src/tork/
│   ├── core/           # Core governance engine
│   ├── adapters/       # Integration adapters
│   ├── identity/       # Identity management
│   ├── compliance/     # Compliance and policy validation
│   └── api/            # FastAPI endpoints
├── cli/                # Command line scanner
├── tests/              # Test suite
└── templates/policies/ # YAML policy templates
```

## CLI Usage

```bash
# Run the governance scanner
tork scan --policy templates/policies/default.yaml
```

## Development

```bash
# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run tests
pytest

# Format code
black src/ tests/ cli/

# Type checking
mypy src/
```

## License

MIT License
