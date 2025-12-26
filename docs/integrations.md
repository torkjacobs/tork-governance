# Integration Guides

Learn how to integrate Tork Governance into your existing workflows.

## LangChain Middleware

Protect your LangChain agents with a few lines of code:

```python
from tork.adapters.langchain import GovernedChain
from langchain.chains import LLMChain

# Wrap your existing chain
governed_chain = GovernedChain(chain=my_chain)

# Run with governance
response = governed_chain.run("Hello world")
```

## HTTP Proxy

Secure your API endpoints using the governance proxy:

```python
from tork.adapters.http_proxy import GovernedProxy

proxy = GovernedProxy(target_url="http://internal-api:8000")
# This creates a FastAPI app that filters requests/responses
```

## Custom Policy Creation

Policies are defined in YAML:

```yaml
name: pii-protection
priority: 10
rules:
  - field: "user_message"
    operator: "pii_detect"
    action: "REDACT"
```
