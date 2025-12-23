# Governance Policy Templates

This directory contains sample policy templates for common governance use cases.

## Policy Format

Policies are defined in YAML with the following structure:

```yaml
name: policy-name
description: What this policy does
enabled: true
priority: 100
rules:
  - field: field_name
    operator: operator_type
    value: comparison_value
    action: action_type
```

## Fields

- **name**: Unique policy identifier
- **description**: Human-readable description of the policy
- **enabled**: Whether the policy is active (default: true)
- **priority**: Evaluation order (higher number = evaluated first)

## Available Operators

- **equals**: Exact string match
- **contains**: Substring match
- **regex**: Regular expression pattern match
- **exists**: Check if field exists in payload

## Available Actions

- **allow**: Permit the operation
- **deny**: Block the operation
- **redact**: Remove/mask the matched content

## Available Policies

### pii-protection.yaml
Detects and redacts personally identifiable information:
- Email addresses
- Phone numbers
- Social Security numbers
- Credit card numbers

### api-security.yaml
Security policies for API requests:
- Blocks internal IP ranges (192.168.*, 10.*, 172.16.*)
- Blocks SQL injection patterns
- Blocks XSS attempts (script tags, javascript: URLs)

### content-moderation.yaml
Basic content filtering:
- Blocks excessive capitalization (shouting)
- Blocks common spam patterns
- Blocks spam punctuation

### compliance-hipaa.yaml
HIPAA compliance for healthcare data:
- Redacts SSN
- Redacts medical record numbers
- Redacts patient IDs
- Redacts health information markers

## Creating Custom Policies

1. Create a new YAML file in this directory
2. Define your policy name, description, and rules
3. Load the policy using PolicyLoader:

```python
from tork.core.policy import PolicyLoader

policy = PolicyLoader.load_from_yaml('templates/policies/my-policy.yaml')
engine = GovernanceEngine(policies=[policy])
```

## Example Custom Policy

```yaml
name: custom-sensitive-data
description: Custom policy for your sensitive data
enabled: true
priority: 50
rules:
  - field: api_key
    operator: regex
    value: '(sk_live_|sk_test_)[a-zA-Z0-9]{20,}'
    action: redact
  - field: database_connection
    operator: contains
    value: 'password='
    action: deny
  - field: request_path
    operator: equals
    value: '/admin/secret'
    action: deny
```
