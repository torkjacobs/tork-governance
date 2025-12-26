# Tork Governance

A universal governance SDK for AI agents.

## Overview

This project provides a comprehensive governance framework for AI agent systems:
- **Governance Engine**: Policy evaluation with ALLOW/DENY/REDACT decisions
- **PII Redactor**: Detects and redacts sensitive data (email, phone, SSN, credit cards, IPs, API keys)
- **Adapters**: Integration with AI frameworks (LangChain, CrewAI, AutoGen, OpenAI Agents)
- **Workflows**: Agent chaining and workflow orchestration with governance
- **Consensus**: Multi-agent debate and consensus building system
- **Identity**: Agent identity management
- **Compliance**: Policy validation and enforcement
- **API**: REST endpoints via FastAPI
- **CLI**: Command-line scanning and policy management

## Core Features

### Policy Engine
- Declarative policy rules with operators: equals, contains, regex, exists
- Rule actions: ALLOW, DENY, REDACT
- Policy priority-based evaluation
- Nested field support (dot notation)

### Agent Identity & Authentication
- JWT-based token issuance and verification
- Agent registration with permissions
- Token refresh and revocation
- Support for custom metadata and organization context
- Expiration validation

### Compliance Receipts & Audit Trails
- PolicyReceipt model with HMAC-SHA256 tamper detection
- ReceiptGenerator for creating audit receipts from evaluations
- Payload hashing (SHA256) for original and modified payloads
- ReceiptStore (ABC) with MemoryReceiptStore and FileReceiptStore implementations
- Query by agent ID and date range

### PII Detection & Redaction
- 6 PII types: EMAIL, PHONE, SSN, CREDIT_CARD, IP_ADDRESS, API_KEY
- Regex patterns with Luhn validation for credit cards
- Automatic overlap detection and filtering (prioritizes more specific types)
- Recursive dict/list redaction
- Integration with GovernanceEngine for auto-redaction

### MCP Security Scanner
- 10 security rules (MCP001-MCP010)
- Detects: hardcoded secrets, missing auth, permissive CORS, debug mode, insecure transport
- Also detects: missing rate limiting, verbose errors, no input validation, privileged access, missing audit logs
- Output formats: text (rich), JSON, SARIF
- Severity filtering: critical, high, medium, low, info
- Exit codes: 1 for critical/high findings, 0 otherwise

### Workflow System
- WorkflowStep and WorkflowDefinition models for defining multi-step agent workflows
- WorkflowEngine for executing governed workflows with chaining support
- WorkflowBuilder fluent API for building workflows programmatically
- Pre-built templates: research_critique_rewrite, multi_agent_consensus, review_and_approve
- Input mapping between steps (previous outputs → next inputs)
- Failure strategies: stop, skip, retry, fallback
- Human approval gates with pause/resume
- Max cost limits and token tracking
- Compliance receipts per step

### Debate & Consensus System
- DebateParticipant model with roles (debater, critic, synthesizer, judge) and voting weights
- DebateRound model tracking responses, critiques, tokens, and costs
- ConsensusConfig with methods: synthesis, voting, judge, unanimous
- DebateEngine for orchestrating multi-agent debates
- Consensus strategies: SynthesisStrategy, VotingStrategy, JudgeStrategy, UnanimousStrategy
- Pre-built templates: two_agent_critique, three_way_debate, expert_panel
- Cost limit enforcement and stop-on-consensus support
- Governance applied to all responses with compliance receipts

### Policy Playground API & Web UI
- Interactive web interface at root URL (/)
- Three tabs: Evaluate, Redact, Scan
- PlaygroundService class for programmatic access
- REST endpoints:
  - POST /playground/evaluate - Evaluate payloads against policies
  - POST /playground/redact - Redact PII from text with type filtering
  - POST /playground/scan - Scan config content for security issues
  - GET /playground/policies - List available policies
  - GET /health - Health check endpoint
- Dark theme UI with Tailwind CSS
- Real-time processing time display

## Project Structure

```
tork-governance/
├── src/tork/
│   ├── core/           # Engine, models, policies, redactor
│   ├── scanner/        # MCP security scanning (rules, scanner)
│   ├── adapters/       # Framework integrations (LangChain, CrewAI, AutoGen, OpenAI Agents)
│   ├── workflows/      # Agent chaining and workflow orchestration
│   ├── consensus/      # Multi-agent debate and consensus building
│   ├── identity/       # Agent identity management
│   ├── compliance/     # Policy validation
│   ├── cli/            # Command-line tools
│   └── api/            # FastAPI endpoints
├── tests/              # Test suite (272 tests)
└── templates/policies/ # YAML policy templates
```

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test module
pytest tests/test_engine.py -v
pytest tests/test_redactor.py -v
pytest tests/test_engine_redactor_integration.py -v
pytest tests/test_scanner.py -v
pytest tests/test_policies.py -v
pytest tests/test_openai_agents.py -v
pytest tests/test_workflows.py -v
```

## CLI Usage

```bash
# Scan for security vulnerabilities
tork scan ./configs

# Scan with severity filter
tork scan ./configs --severity high

# JSON output
tork scan ./configs --output json

# SARIF output for CI/CD
tork scan ./configs --output sarif
```

## Policy Templates

Sample governance policies available in `templates/policies/`:
- **pii-protection.yaml**: Detect and redact email, phone, SSN, credit cards
- **api-security.yaml**: Block internal IPs, SQL injection, XSS attempts
- **content-moderation.yaml**: Filter spam, excessive caps, offensive content
- **compliance-hipaa.yaml**: HIPAA-compliant PII and medical data redaction

See `templates/policies/README.md` for policy format documentation and examples.

## Test Coverage

- **14** Governance Engine tests (initialization, decisions, operators, nesting)
- **30** PII Redactor tests (all PII types, overlaps, dict redaction)
- **9** Integration tests (engine + redactor, auto-redaction, default engine)
- **6** Package import tests
- **37** MCP Scanner tests (all 10 rules, scanner class, output formats)
- **11** Policy template tests (loading, validation, execution)
- **13** JWT Identity tests (token issuance, verification, expiry, revocation, agent management)
- **19** Compliance Receipt tests (generation, signature verification, memory/file storage, queries)
- **20** LangChain adapter tests (callback handler, governed chain, violations, redaction)
- **11** CrewAI adapter tests (middleware, governed agents/crews, PII redaction)
- **10** AutoGen adapter tests (middleware, governed agents, group chat)
- **23** OpenAI Agents SDK adapter tests (middleware, governed agent/runner, tool validation, receipts)
- **27** Workflow tests (models, engine, builder, templates, pause/resume, async)
- **26** Consensus tests (debate models, engine, strategies, templates, cost limits)
- **18** HTTP proxy adapter tests (config, request/response evaluation, proxy app routes)
- **24** Playground API tests (service class, endpoints, UI serving)

## Recent Changes

- 2025-12-26: Debate/Consensus system with DebateEngine, strategies, and templates
- 2025-12-26: Agent Chaining/Workflow system with WorkflowEngine, WorkflowBuilder, and templates
- 2025-12-26: OpenAI Agents SDK integration adapter with middleware, governed wrappers, tool validation
- 2025-12-26: Professional README update with badges and framework integration examples
- 2025-12-26: Microsoft AutoGen integration adapter with governed agents and group chats
- 2025-12-26: CrewAI integration adapter with governed agents and crews
- 2025-12-26: Policy Playground API and interactive web UI with evaluate/redact/scan tabs
- 2025-12-25: PyPI publishing preparation (README, CHANGELOG, LICENSE, pyproject.toml)
- 2024-12-25: HTTP proxy adapter with GovernedProxy and FastAPI server
- 2024-12-25: LangChain middleware integration with callback handler and governed chain wrapper
- 2024-12-23: Compliance receipts system with audit trails, tamper detection, and storage backends
- 2024-12-23: JWT-based identity handler with token management and agent authentication
- 2024-12-23: Sample policy templates with 11 comprehensive tests
- 2024-12-23: Fixed test keys to use obviously fake patterns for secret scanner safety
- 2024-12-23: MCP Security Scanner with 10 rules, CLI integration, text/json/sarif output
- 2024-12-23: Full integration of PIIRedactor with GovernanceEngine
- 2024-12-23: Fixed overlapping PII detection with priority filtering
- 2024-12-23: Implemented comprehensive governance engine with policy evaluation
- 2024-12-23: Created PII redactor with 6 detection types and Luhn validation
- 2024-12-23: Initial project setup with module structure
