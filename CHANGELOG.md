# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-12-25

### Added

- **Governance Engine**: Core policy evaluation with ALLOW/DENY/REDACT decisions
  - Declarative policy rules with operators: equals, contains, regex, exists
  - Policy priority-based evaluation
  - Nested field support using dot notation

- **PII Redactor**: Automatic detection and redaction of sensitive data
  - Email addresses
  - Phone numbers
  - Social Security Numbers (SSN)
  - Credit card numbers with Luhn validation
  - IP addresses
  - API keys (Stripe, GitHub, AWS, Google, OpenAI patterns)
  - Overlap detection with priority filtering

- **MCP Security Scanner**: Configuration security scanning
  - 10 security rules (MCP001-MCP010)
  - Detects hardcoded secrets, missing auth, permissive CORS
  - Detects debug mode, insecure transport, missing rate limiting
  - Detects verbose errors, no input validation, privileged access
  - Detects missing audit logs
  - Output formats: text (rich), JSON, SARIF
  - Severity filtering: critical, high, medium, low, info
  - CLI integration via `tork scan`

- **JWT Identity Handler**: Agent authentication system
  - Token issuance with configurable expiration
  - Token verification with expiration validation
  - Token refresh and revocation
  - Agent registration and permission management
  - Custom exceptions: InvalidTokenError, ExpiredTokenError, RevokedTokenError

- **Compliance Receipts**: Audit trail system
  - PolicyReceipt model with HMAC-SHA256 tamper detection
  - ReceiptGenerator for creating signed audit receipts
  - SHA256 payload hashing for original and modified payloads
  - MemoryReceiptStore for testing
  - FileReceiptStore for persistent JSON storage
  - Query by agent ID and date range

- **LangChain Integration**: Middleware for LangChain applications
  - TorkCallbackHandler for LLM, chain, and tool callbacks
  - GovernedChain wrapper for chain-level governance
  - Automatic GovernanceViolation on DENY decisions
  - Receipt generation support

- **HTTP Proxy Adapter**: Governed HTTP proxying
  - GovernedProxy class with request/response evaluation
  - FastAPI server with GET/POST/PUT/DELETE/PATCH routes
  - X-Agent-ID header support
  - X-Tork-Decision and X-Tork-Receipt-ID response headers

- **Policy Templates**: Ready-to-use governance policies
  - pii-protection.yaml: Email, phone, SSN, credit card detection
  - api-security.yaml: Block internal IPs, SQL injection, XSS
  - content-moderation.yaml: Filter spam, excessive caps, offensive content
  - compliance-hipaa.yaml: HIPAA-compliant PII and medical data redaction

- **FastAPI Integration**: REST API endpoints
  - Evaluation endpoints
  - Policy management
  - Health checks

- **CLI Tools**: Command-line interface
  - `tork scan` for security scanning
  - Multiple output formats
  - Severity filtering
  - Exit codes for CI/CD integration
