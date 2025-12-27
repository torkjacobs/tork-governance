# API Reference

Detailed documentation of all Tork Governance classes and methods.

## Core Module

### GovernanceEngine

The main entry point for policy evaluation.

```python
from tork import GovernanceEngine

engine = GovernanceEngine(policies=None, auto_redact=True)
```

**Parameters:**
- `policies`: List of Policy objects (optional)
- `auto_redact`: Enable automatic PII redaction (default: True)

**Methods:**

| Method | Description |
|--------|-------------|
| `evaluate(request)` | Evaluate a request against policies |
| `add_policy(policy)` | Add a policy to the engine |
| `remove_policy(name)` | Remove a policy by name |

### EvaluationRequest

Request model for policy evaluation.

```python
from tork.core.models import EvaluationRequest

request = EvaluationRequest(
    payload=dict,           # The data to evaluate
    agent_id=str,           # Agent identifier
    action=str,             # Action being performed
    metadata=dict,          # Optional metadata
)
```

### PolicyDecision

Enum for evaluation decisions.

```python
from tork.core.models import PolicyDecision

PolicyDecision.ALLOW   # Request is allowed
PolicyDecision.DENY    # Request is denied
PolicyDecision.REDACT  # Request allowed with modifications
```

## PII Redactor

### PIIRedactor

Detect and redact personally identifiable information.

```python
from tork.core.redactor import PIIRedactor

redactor = PIIRedactor()
```

**Methods:**

| Method | Description |
|--------|-------------|
| `detect(text)` | Find PII in text, returns list of PIIMatch |
| `redact_text(text)` | Redact PII from text string |
| `redact_dict(data)` | Recursively redact PII from dict |

**Supported PII Types:**
- `EMAIL` - Email addresses
- `PHONE` - Phone numbers
- `SSN` - Social Security Numbers
- `CREDIT_CARD` - Credit card numbers (with Luhn validation)
- `IP_ADDRESS` - IP addresses
- `API_KEY` - API keys and secrets

## Scanner

### MCPScanner

Security scanner for agent configurations.

```python
from tork.scanner import MCPScanner

scanner = MCPScanner(severity_filter=None)
```

**Methods:**

| Method | Description |
|--------|-------------|
| `scan_file(path)` | Scan a single file |
| `scan_directory(path)` | Scan all files in directory |
| `scan_content(content)` | Scan content string |

## Identity

### IdentityHandler

JWT-based agent identity management.

```python
from tork.identity import IdentityHandler

handler = IdentityHandler(secret_key="your-secret")
```

**Methods:**

| Method | Description |
|--------|-------------|
| `issue_token(agent_id)` | Issue a JWT token |
| `verify_token(token)` | Verify and decode token |
| `revoke_token(token)` | Revoke a token |
| `register_agent(agent_id)` | Register a new agent |

## Workflows

### WorkflowEngine

Execute multi-step agent workflows.

```python
from tork.workflows import WorkflowEngine

engine = WorkflowEngine(governance_engine=None)
```

**Methods:**

| Method | Description |
|--------|-------------|
| `register_executor(agent_id, fn)` | Register an agent executor |
| `execute(workflow, input)` | Execute a workflow |
| `execute_async(workflow, input)` | Async execution |
| `pause(workflow_id)` | Pause at approval gate |
| `resume(workflow_id)` | Resume paused workflow |

### WorkflowBuilder

Fluent API for building workflows.

```python
from tork.workflows import WorkflowBuilder

workflow = (
    WorkflowBuilder("my-workflow")
    .add_step(id="step1", name="Step 1", agent_id="agent-1")
    .with_max_cost(5.0)
    .build()
)
```

## Consensus

### DebateEngine

Orchestrate multi-agent debates.

```python
from tork.consensus import DebateEngine

engine = DebateEngine(governance_engine=None)
```

**Methods:**

| Method | Description |
|--------|-------------|
| `register_executor(agent_id, fn)` | Register an agent executor |
| `debate(topic, participants, config)` | Run a debate |

## ACL

### ACLRouter

Route messages between agents.

```python
from tork.acl import ACLRouter

router = ACLRouter(governance_engine=None)
```

**Methods:**

| Method | Description |
|--------|-------------|
| `register_handler(agent_id, fn)` | Register message handler |
| `route(message)` | Route a single message |
| `broadcast(message, receivers)` | Send to multiple agents |

### MessageBuilder

Fluent API for creating ACL messages.

```python
from tork.acl import MessageBuilder

message = (
    MessageBuilder()
    .request()
    .from_agent("sender")
    .to_agent("receiver")
    .with_content({"task": "..."})
    .build()
)
```

## Personas

### PersonaRuntime

Execute custom personas.

```python
from tork.personas import PersonaRuntime

runtime = PersonaRuntime(governance_engine=None)
```

**Methods:**

| Method | Description |
|--------|-------------|
| `register_executor(model, fn)` | Register model executor |
| `execute(persona_id, input, store)` | Execute a persona |
| `start_session(persona_id, store)` | Start a session |
| `end_session(session)` | End a session |

### PersonaBuilder

Fluent API for building personas.

```python
from tork.personas import PersonaBuilder

config = (
    PersonaBuilder("my-persona")
    .with_name("My Persona")
    .with_system_prompt("...")
    .with_capabilities([...])
    .build()
)
```

## Capabilities

### CapabilityRegistry

Manage agent capability profiles.

```python
from tork.capabilities import CapabilityRegistry

registry = CapabilityRegistry()
```

**Methods:**

| Method | Description |
|--------|-------------|
| `register(profile)` | Register an agent profile |
| `get(agent_id)` | Get profile by ID |
| `list_all()` | List all profiles |
| `filter_by_capability(name, level)` | Filter by capability |
| `compare(agent_ids)` | Compare multiple agents |

### TaskMatcher

Match tasks to best agents.

```python
from tork.capabilities import TaskMatcher

matcher = TaskMatcher(registry)
```

**Methods:**

| Method | Description |
|--------|-------------|
| `match(task, capabilities)` | Find best agent |
| `rank(task, capabilities)` | Rank all agents |
| `recommend(task)` | Get recommendations |

## Routing

### SectorRouter

Route requests by sector and role.

```python
from tork.routing import SectorRouter

router = SectorRouter(fallback_route=None)
```

**Methods:**

| Method | Description |
|--------|-------------|
| `register_route(sector, roles, config)` | Register a route |
| `route(context, request)` | Route a request |
| `route_by_sector(sector, request)` | Route by sector only |
| `route_by_role(role, request)` | Route by role only |

## Prompts

### PromptOrchestrator

End-to-end prompt generation and selection.

```python
from tork.prompts import PromptOrchestrator

orchestrator = PromptOrchestrator()
```

**Methods:**

| Method | Description |
|--------|-------------|
| `orchestrate(task, type, agents)` | Generate and select |
| `refine(prompt, agent, feedback)` | Refine a prompt |
| `iterate(task, agents, max_iter)` | Iterative improvement |
