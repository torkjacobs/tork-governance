"""
Pytest configuration and fixtures.
"""

import pytest


@pytest.fixture
def sample_policy() -> dict:
    """Provide a sample policy for testing."""
    return {
        "name": "test-policy",
        "version": "1.0.0",
        "rules": [
            {
                "id": "rule-001",
                "description": "Test rule",
                "message": "Test rule violation",
            }
        ],
    }


@pytest.fixture
def sample_action() -> dict:
    """Provide a sample action for testing."""
    return {
        "type": "agent_action",
        "agent_id": "test-agent-001",
        "action": "execute",
        "parameters": {},
    }
