# Tork Governance

A universal governance SDK for AI agents.

## Overview

This project provides a comprehensive governance framework for AI agent systems:
- **Governance Engine**: Policy evaluation with ALLOW/DENY/REDACT decisions
- **PII Redactor**: Detects and redacts sensitive data (email, phone, SSN, credit cards, IPs, API keys)
- **Adapters**: Integration with various AI frameworks
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

## Project Structure

```
tork-governance/
├── src/tork/
│   ├── core/           # Engine, models, policies, redactor
│   ├── scanner/        # MCP security scanning (rules, scanner)
│   ├── adapters/       # Framework integrations
│   ├── identity/       # Agent identity management
│   ├── compliance/     # Policy validation
│   ├── cli/            # Command-line tools
│   └── api/            # FastAPI endpoints
├── tests/              # Test suite (96 tests)
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

## Recent Changes

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
