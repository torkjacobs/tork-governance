# Tork Governance SDK

[![PyPI version](https://badge.fury.io/py/tork-governance.svg)](https://badge.fury.io/py/tork-governance)
[![Python versions](https://img.shields.io/pypi/pyversions/tork-governance.svg)](https://pypi.org/project/tork-governance/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A universal governance SDK for AI agents. Provides comprehensive policy enforcement, PII detection, security scanning, and audit trails for AI agent systems.

## Installation

```bash
pip install tork-governance
```

With LangChain integration:
```bash
pip install tork-governance[langchain]
```

## Quick Start

```python
from tork.core import GovernanceEngine, PIIRedactor
from tork.core.policy import Policy, PolicyRule, PolicyAction, PolicyOperator
from tork.core.models import EvaluationRequest

# Create engine with PII protection
engine = GovernanceEngine(pii_redactor=PIIRedactor())

# Add a security policy
policy = Policy(
    name="block-sql-injection",
    rules=[PolicyRule(
        field="query",
        operator=PolicyOperator.REGEX,
        value=r"(?i)(drop|delete|truncate)\s+table",
        action=PolicyAction.DENY,
    )]
)
engine.add_policy(policy)

# Evaluate a request
result = engine.evaluate(EvaluationRequest(
    agent_id="agent-001",
    action="execute_query",
    payload={"query": "SELECT * FROM users", "email": "user@example.com"}
))

print(f"Decision: {result.decision}")  # REDACT (email detected)
print(f"Modified: {result.modified_payload}")  # email replaced with [REDACTED_EMAIL]
```

## Features

- **Policy Engine** - Declarative rules with ALLOW/DENY/REDACT decisions
- **PII Detection** - Automatic detection and redaction of 6 PII types:
  - Email addresses
  - Phone numbers
  - Social Security Numbers
  - Credit card numbers (with Luhn validation)
  - IP addresses
  - API keys
- **MCP Security Scanner** - 10 security rules for config scanning
- **JWT Authentication** - Agent identity management with token lifecycle
- **Compliance Receipts** - HMAC-signed audit trails with tamper detection
- **LangChain Integration** - Callback handlers and governed chain wrappers
- **HTTP Proxy** - Governed HTTP proxy with FastAPI server
- **Policy Templates** - Ready-to-use policies for PII, API security, HIPAA compliance

## CLI Usage

```bash
# Scan configuration files for security issues
tork scan ./configs

# Scan with severity filter
tork scan ./configs --severity high

# Output as JSON
tork scan ./configs --output json

# Output as SARIF (for CI/CD integration)
tork scan ./configs --output sarif
```

## LangChain Integration

```python
from tork.core import GovernanceEngine
from tork.adapters.langchain import TorkCallbackHandler, create_governed_chain

engine = GovernanceEngine()
handler = TorkCallbackHandler(engine=engine)

# Use with any LangChain chain
governed_chain = create_governed_chain(your_chain, engine)
result = governed_chain.invoke({"input": "Hello"})
```

## HTTP Proxy

```python
from tork.core import GovernanceEngine
from tork.adapters.http import ProxyConfig, create_proxy_app

config = ProxyConfig(target_base_url="https://api.example.com")
engine = GovernanceEngine()

app = create_proxy_app(config, engine)
# Run with: uvicorn module:app --host 0.0.0.0 --port 8000
```

## Documentation

For full documentation, visit [GitHub](https://github.com/torkjacobs/tork-governance).

## License

MIT License - see [LICENSE](LICENSE) for details.

## Links

- [Homepage](https://tork.network)
- [GitHub Repository](https://github.com/torkjacobs/tork-governance)
- [Issue Tracker](https://github.com/torkjacobs/tork-governance/issues)
