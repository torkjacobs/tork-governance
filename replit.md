# Tork Governance

A universal governance SDK for AI agents.

## Overview

This project provides a comprehensive governance framework for AI agent systems, including:
- **Core Engine**: Central governance orchestration
- **Adapters**: Integration with various AI frameworks
- **Identity**: Agent identity management
- **Compliance**: Policy validation and enforcement
- **API**: REST endpoints via FastAPI

## Project Structure

```
tork-governance/
├── src/tork/           # Main package
│   ├── core/           # Governance engine
│   ├── adapters/       # Integration adapters
│   ├── identity/       # Identity management
│   ├── compliance/     # Policy validation
│   └── api/            # FastAPI endpoints
├── cli/                # Command line tools
├── tests/              # Test suite
└── templates/policies/ # YAML policy templates
```

## Tech Stack

- Python 3.11
- FastAPI for REST API
- Pydantic 2.x for data validation
- PyYAML for policy files
- Typer + Rich for CLI
- structlog for logging
- pytest for testing

## Development Commands

```bash
# Run tests
pytest

# Run API server
uvicorn src.tork.api.app:app --host 0.0.0.0 --port 5000

# CLI usage
python -m cli.scanner scan --policy templates/policies/
```

## Recent Changes

- 2024-12-23: Initial project setup with complete module structure
