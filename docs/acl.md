# Agent Communication Language (ACL)

Structured message passing between AI agents using FIPA-compliant protocols.

## Overview

The ACL module provides a standardized way for AI agents to communicate using performatives (speech acts), structured messages, and formal protocols. All messages pass through governance and generate compliance receipts.

## Core Concepts

### Performatives

The 12 standard speech acts for agent communication:

```python
from tork.acl import Performative

# Requesting and informing
Performative.REQUEST       # Ask agent to perform action
Performative.INFORM        # Share information
Performative.QUERY_IF      # Ask if something is true
Performative.QUERY_REF     # Ask for a value

# Proposing and negotiating
Performative.PROPOSE       # Make a proposal
Performative.ACCEPT        # Accept a proposal
Performative.REJECT        # Reject a proposal

# Task management
Performative.CFP           # Call for proposals
Performative.AGREE         # Agree to perform action
Performative.REFUSE        # Refuse to perform action
Performative.CANCEL        # Cancel a request
Performative.FAILURE       # Report failure
```

### ACLMessage

Structured message format:

```python
from tork.acl import ACLMessage, Performative

message = ACLMessage(
    performative=Performative.REQUEST,
    sender="coordinator",
    receiver="worker-1",
    content={"task": "analyze_data", "file": "data.csv"},
    protocol="fipa-request",
    ontology="data-analysis",
    conversation_id="conv-123",
)
```

## MessageBuilder

Fluent API for creating messages:

```python
from tork.acl import MessageBuilder

message = (
    MessageBuilder()
    .request()
    .from_agent("coordinator")
    .to_agent("worker-1")
    .with_content({"task": "process"})
    .using_protocol("fipa-request")
    .in_conversation("conv-123")
    .build()
)
```

## FIPA Protocols

### Request Protocol

Simple request-response pattern:

```python
from tork.acl import FIPAProtocol

protocol = FIPAProtocol.REQUEST

# States: INITIATED -> AGREED/REFUSED -> COMPLETED/FAILED
```

### Contract Net Protocol

Negotiation for task assignment:

```python
from tork.acl import FIPAProtocol

protocol = FIPAProtocol.CONTRACT_NET

# Flow:
# 1. Initiator sends CFP (Call for Proposals)
# 2. Participants send PROPOSE or REFUSE
# 3. Initiator sends ACCEPT or REJECT
# 4. Winner sends INFORM (result) or FAILURE
```

### Query Protocol

Information retrieval:

```python
from tork.acl import FIPAProtocol

protocol = FIPAProtocol.QUERY

# States: INITIATED -> INFORMED/REFUSED
```

## ACLRouter

Route messages between agents with governance:

```python
from tork.acl import ACLRouter

router = ACLRouter()

# Register message handlers
router.register_handler("worker-1", worker1_handler)
router.register_handler("worker-2", worker2_handler)

# Route a message
response = router.route(message)

# Broadcast to multiple agents
responses = router.broadcast(
    message,
    receivers=["worker-1", "worker-2", "worker-3"],
)
```

## Conversation Management

Track message threads:

```python
from tork.acl import Conversation

conversation = Conversation(id="conv-123")

# Add messages
conversation.add_message(request_message)
conversation.add_message(response_message)

# Get conversation history
for msg in conversation.messages:
    print(f"{msg.sender} -> {msg.receiver}: {msg.performative}")

# Check conversation state
print(f"State: {conversation.state}")
print(f"Is complete: {conversation.is_complete}")
```

## Protocol Validation

Ensure messages follow protocol rules:

```python
from tork.acl import validate_protocol_transition

# Check if a transition is valid
is_valid = validate_protocol_transition(
    protocol=FIPAProtocol.REQUEST,
    current_state="INITIATED",
    message_type=Performative.AGREE,
)

if not is_valid:
    raise ValueError("Invalid protocol transition")
```

## Governance Integration

All messages pass through governance:

```python
from tork.core import GovernanceEngine
from tork.acl import ACLRouter

gov_engine = GovernanceEngine(policies=[security_policy])
router = ACLRouter(governance_engine=gov_engine)

# Messages with PII will be redacted
# Blocked actions will be denied
response = router.route(message)
```

## Compliance Receipts

Each message generates a signed receipt:

```python
response = router.route(message)

print(f"Receipt ID: {response.receipt.receipt_id}")
print(f"Sender: {response.receipt.agent_id}")
print(f"Signature: {response.receipt.signature}")
```

## Example: Contract Net Negotiation

```python
from tork.acl import MessageBuilder, ACLRouter, Performative

router = ACLRouter()

# 1. Send Call for Proposals
cfp = (
    MessageBuilder()
    .cfp()
    .from_agent("manager")
    .to_agent("worker-1")
    .with_content({"task": "process_batch", "deadline": "1h"})
    .using_protocol("fipa-contract-net")
    .build()
)

# 2. Receive proposals
proposal = router.route(cfp)

# 3. Accept best proposal
accept = (
    MessageBuilder()
    .accept()
    .from_agent("manager")
    .to_agent("worker-1")
    .with_content({"selected": True})
    .in_conversation(cfp.conversation_id)
    .build()
)

# 4. Get result
result = router.route(accept)
```
