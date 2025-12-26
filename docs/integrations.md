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

## CrewAI

Governance for CrewAI agents and crews:

```python
from tork.adapters.crewai import TorkCrewAIMiddleware

middleware = TorkCrewAIMiddleware()
governed_agent = middleware.wrap_agent(my_agent)
```

## AutoGen

Governance for Microsoft AutoGen agents and group chats:

```python
from tork.adapters.autogen import TorkAutoGenMiddleware

middleware = TorkAutoGenMiddleware()
governed_agent = middleware.wrap_agent(my_agent)
```

## OpenAI Agents SDK

The OpenAI Agents SDK integration provides comprehensive governance for OpenAI agents, including input/output filtering and tool call validation.

### Installation

The OpenAI Agents adapter is an optional dependency:

```bash
pip install tork-governance[openai]
```

### Basic Usage

```python
from tork.adapters.openai_agents import TorkOpenAIAgentsMiddleware

# Initialize middleware
middleware = TorkOpenAIAgentsMiddleware(agent_id="my-openai-agent")

# Wrap your agent
governed_agent = middleware.wrap_agent(openai_agent)

# Run with governance (supports sync and async)
result = governed_agent.run("Process this request")
# or
# result = await governed_agent.run_async("Process this request")
```

### Features

- **wrap_agent**: Intercepts `run` and `run_async` methods to apply governance.
- **Tool Call Validation**: Automatically blocks dangerous tool calls (shell, exec, etc.) based on security policies.
- **Async Support**: Full support for asynchronous agent execution.
- **Compliance Receipts**: Automatically generates signed audit receipts for all agent outputs.

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
