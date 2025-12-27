# Tork Governance SDK

A universal, production-ready governance SDK for AI agents.

## Overview

Tork Governance provides a comprehensive framework for managing AI agent behavior, ensuring security, and maintaining compliance. It handles everything from policy evaluation and PII redaction to security scanning, agent orchestration, and multi-agent coordination.

## Key Features

- **Governance Engine**: Declarative policy evaluation (ALLOW/DENY/REDACT)
- **PII Redactor**: Automatic detection and redaction of sensitive data (Email, Phone, SSN, etc.)
- **MCP Security Scanner**: Security scanning for agent configurations and code
- **Agent Identity**: JWT-based identity management and authentication
- **Compliance Receipts**: Tamper-evident audit trails with HMAC signatures
- **Framework Integrations**: Native support for LangChain, CrewAI, AutoGen, OpenAI Agents SDK, and HTTP Proxy
- **Workflows**: Agent chaining and workflow orchestration with governance
- **Consensus**: Multi-agent debate and consensus building system
- **ACL**: Agent Communication Language message schema with FIPA protocols
- **Personas**: Custom agents/personas with governance-enforced execution
- **Capabilities**: Agent capability labels with proficiency levels and task matching
- **Routing**: Role/sector-based request routing with governance
- **Prompts**: Agent-selectable prompts with multi-agent generation and selection
- **Interactive Playground**: Web-based UI for testing policies and scanning

## Test Coverage

The SDK includes **450+ tests** covering all major systems:

- Core governance engine and policy evaluation
- PII detection with 6 data types
- MCP security scanner with 10 rules
- JWT identity management
- Compliance receipts and audit trails
- 5 framework integrations (LangChain, CrewAI, AutoGen, OpenAI Agents, HTTP Proxy)
- Workflow orchestration
- Consensus and debate systems
- ACL message schemas with FIPA protocols
- Custom personas with templates
- Capability labels and task matching
- Role/sector routing
- Agent-selectable prompts

## Quick Installation

```bash
pip install tork-governance
```

## Documentation Map

| Section | Description |
|---------|-------------|
| [Getting Started](getting-started.md) | Installation and basic usage |
| [Framework Integrations](integrations.md) | LangChain, CrewAI, AutoGen, OpenAI Agents |
| [Workflows](workflows.md) | Agent chaining and orchestration |
| [Consensus](consensus.md) | Multi-agent debate and decision-making |
| [ACL](acl.md) | Agent Communication Language protocols |
| [Personas](personas.md) | Custom agent personas |
| [Capabilities](capabilities.md) | Agent proficiency labels and matching |
| [Routing](routing.md) | Role and sector-based routing |
| [Prompts](prompts.md) | Agent-selectable prompt generation |
| [API Reference](api.md) | Detailed class and method documentation |

## Architecture

```
tork-governance/
├── src/tork/
│   ├── core/           # Engine, models, policies, redactor
│   ├── scanner/        # MCP security scanning
│   ├── adapters/       # Framework integrations
│   ├── workflows/      # Agent chaining
│   ├── consensus/      # Multi-agent debate
│   ├── acl/            # Agent Communication Language
│   ├── personas/       # Custom personas
│   ├── capabilities/   # Agent capability labels
│   ├── routing/        # Role/sector routing
│   ├── prompts/        # Agent-selectable prompts
│   ├── identity/       # JWT authentication
│   ├── compliance/     # Audit trails
│   └── api/            # FastAPI endpoints
```
