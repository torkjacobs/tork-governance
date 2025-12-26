# Examples

Practical examples of using the Tork Governance SDK.

## PII Redaction

```python
from tork.core.redactor import PIIRedactor

redactor = PIIRedactor()
text = "Contact me at alice@example.com"
redacted = redactor.redact(text)
# Result: "Contact me at [EMAIL]"
```

## Security Scanning

```python
from tork.scanner.scanner import MCPScanner

scanner = MCPScanner()
findings = scanner.scan_content('{"api_key": "sk-12345"}', "config.json")
# findings will contain a 'Hardcoded Secret' vulnerability
```

## Receipt Generation

```python
from tork.compliance.receipts import ReceiptGenerator

generator = ReceiptGenerator(secret_key="secret")
receipt = generator.create_receipt(agent_id="agent-1", result=eval_result)
# receipt contains an HMAC signature for tamper-proofing
```
