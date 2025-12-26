# API Reference

Detailed documentation for the Tork Governance SDK core components.

## GovernanceEngine

The main entry point for policy evaluation.

### Methods

- `evaluate(payload: Dict, agent_id: str = None) -> EvaluationResult`: Evaluates a payload against all loaded policies.
- `add_policy(policy: Policy)`: Manually adds a policy to the engine.

## PIIRedactor

Handles detection and redaction of sensitive information.

### Methods

- `redact(text: str, pii_types: List[str] = None) -> str`: Detects and redacts PII from text.
- `detect(text: str) -> List[PIIMatch]`: Returns a list of detected PII matches without redacting.

## MCPScanner

Security scanner for configuration and source files.

### Methods

- `scan_content(content: str, filename: str) -> List[ScanFinding]`: Scans text content for security vulnerabilities.
- `scan_directory(path: str) -> List[ScanFinding]`: Scans all supported files in a directory.

## IdentityHandler

Manages agent identity and JWT tokens.

### Methods

- `issue_token(agent_id: str, permissions: List[str]) -> str`: Creates a new JWT for an agent.
- `verify_token(token: str) -> Dict`: Validates a token and returns its claims.

## Policy Models

### Policy
- `name`: Unique name for the policy.
- `rules`: List of `Rule` objects.
- `priority`: Execution priority (lower numbers run first).

### Rule
- `field`: The payload field to evaluate (supports dot notation).
- `operator`: The comparison operator (equals, contains, regex, etc.).
- `value`: The target value for the comparison.
- `action`: Resulting action (ALLOW, DENY, REDACT).
