# Consensus

Multi-agent debate and consensus building system.

## Overview

The Consensus module enables multiple AI agents to debate topics, critique each other's responses, and reach consensus through various strategies. All responses are governed by policies and generate compliance receipts.

## Core Concepts

### DebateParticipant

Define agents that participate in debates:

```python
from tork.consensus import DebateParticipant, ParticipantRole

participant = DebateParticipant(
    agent_id="expert-1",
    role=ParticipantRole.DEBATER,
    voting_weight=1.0,
    model="gpt-4",
)
```

### Participant Roles

- `DEBATER`: Presents arguments and positions
- `CRITIC`: Critiques other participants' arguments
- `SYNTHESIZER`: Combines multiple perspectives
- `JUDGE`: Makes final decisions

### ConsensusConfig

Configure how consensus is reached:

```python
from tork.consensus import ConsensusConfig, ConsensusMethod

config = ConsensusConfig(
    method=ConsensusMethod.SYNTHESIS,
    max_rounds=3,
    stop_on_consensus=True,
    cost_limit=5.0,
)
```

## DebateEngine

Orchestrate multi-agent debates:

```python
from tork.consensus import DebateEngine

engine = DebateEngine()

# Register agent executors
engine.register_executor("expert-1", expert1_fn)
engine.register_executor("expert-2", expert2_fn)
engine.register_executor("synthesizer", synthesizer_fn)

# Run debate
result = engine.debate(
    topic="Should AI systems be open source?",
    participants=[participant1, participant2, synthesizer],
    config=config,
)

print(f"Consensus: {result.consensus}")
print(f"Rounds: {len(result.rounds)}")
```

## Consensus Strategies

### Synthesis Strategy

Combines all perspectives into a unified view:

```python
config = ConsensusConfig(method=ConsensusMethod.SYNTHESIS)

# A synthesizer agent combines all arguments
result = engine.debate(topic, participants, config)
```

### Voting Strategy

Participants vote on the best position:

```python
config = ConsensusConfig(
    method=ConsensusMethod.VOTING,
    voting_threshold=0.6,  # 60% agreement required
)

result = engine.debate(topic, participants, config)
print(f"Votes: {result.vote_counts}")
```

### Judge Strategy

A designated judge makes the final decision:

```python
judge = DebateParticipant(
    agent_id="judge",
    role=ParticipantRole.JUDGE,
)

config = ConsensusConfig(method=ConsensusMethod.JUDGE)

result = engine.debate(
    topic,
    participants=[debater1, debater2, judge],
    config,
)
```

### Unanimous Strategy

All participants must agree:

```python
config = ConsensusConfig(
    method=ConsensusMethod.UNANIMOUS,
    max_rounds=5,  # Keep debating until unanimous or max rounds
)
```

## Debate Rounds

Track the debate progression:

```python
result = engine.debate(topic, participants, config)

for round in result.rounds:
    print(f"Round {round.round_number}:")
    for response in round.responses:
        print(f"  {response.agent_id}: {response.content[:100]}...")
    for critique in round.critiques:
        print(f"  Critique from {critique.agent_id}")
```

## Cost Limit Enforcement

Stop debates when budget is exceeded:

```python
config = ConsensusConfig(
    method=ConsensusMethod.SYNTHESIS,
    cost_limit=2.0,  # Stop if cost exceeds $2
)

result = engine.debate(topic, participants, config)

if result.cost_exceeded:
    print(f"Stopped due to cost limit: ${result.total_cost}")
```

## Pre-built Templates

Ready-to-use debate configurations:

```python
from tork.consensus.templates import (
    two_agent_critique,
    three_way_debate,
    expert_panel,
)

# Two agents critique each other
participants, config = two_agent_critique()

# Three-way debate with synthesis
participants, config = three_way_debate()

# Expert panel with multiple specialists and a moderator
participants, config = expert_panel(
    expert_ids=["legal", "technical", "business"],
    moderator_id="moderator",
)
```

## Governance Integration

All debate responses pass through governance:

```python
from tork.core import GovernanceEngine

gov_engine = GovernanceEngine(policies=[pii_policy])
debate_engine = DebateEngine(governance_engine=gov_engine)

# PII will be redacted from all responses
result = debate_engine.debate(topic, participants, config)
```

## Compliance Receipts

Each response generates a signed receipt:

```python
for round in result.rounds:
    for response in round.responses:
        print(f"Receipt: {response.receipt.receipt_id}")
        print(f"Verified: {response.receipt.verify()}")
```
