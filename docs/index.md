# Tork Governance SDK

A universal, production-ready governance SDK for AI agents.

## Overview

Tork Governance provides a comprehensive framework for managing AI agent behavior, ensuring security, and maintaining compliance. It handles everything from policy evaluation and PII redaction to security scanning and audit trails.

## Key Features

- **Governance Engine**: Declarative policy evaluation (ALLOW/DENY/REDACT).
- **PII Redactor**: Automatic detection and redaction of sensitive data (Email, Phone, SSN, etc.).
- **MCP Security Scanner**: Security scanning for agent configurations and code.
- **Agent Identity**: JWT-based identity management and authentication.
- **Compliance Receipts**: Tamper-evident audit trails with HMAC signatures.
- **Interactive Playground**: Web-based UI for testing policies and scanning.

## Quick Installation

```bash
pip install tork-governance
```

## Documentation Map

- [Quickstart](quickstart.md): Get up and running in minutes.
- [API Reference](api-reference.md): Detailed class and method documentation.
- [Integrations](integrations.md): Guides for LangChain, FastAPI, and more.
- [Examples](examples.md): Practical code samples for common use cases.
