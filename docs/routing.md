# Routing

Role and sector-based request routing with governance.

## Overview

The Routing module directs AI requests to appropriate agents based on the user's sector (industry) and role. Each route can have its own governance policy, allowed actions, and target persona.

## Core Concepts

### Sectors

11 industry sectors:

```python
from tork.routing import Sector

Sector.EDUCATION      # Schools, universities
Sector.HEALTHCARE     # Hospitals, clinics
Sector.FINANCE        # Banks, investment
Sector.LEGAL          # Law firms, courts
Sector.TECHNOLOGY     # Software, IT
Sector.MARKETING      # Advertising, PR
Sector.RETAIL         # Stores, e-commerce
Sector.MANUFACTURING  # Factories, production
Sector.GOVERNMENT     # Public sector
Sector.NONPROFIT      # Charities, NGOs
Sector.GENERAL        # Default/other
```

### Roles

24 user roles across sectors:

```python
from tork.routing import Role

# Education
Role.STUDENT, Role.TEACHER, Role.ADMINISTRATOR

# Healthcare
Role.DOCTOR, Role.NURSE, Role.PATIENT

# Finance
Role.ANALYST, Role.TRADER, Role.ACCOUNTANT

# Legal
Role.LAWYER, Role.PARALEGAL, Role.CLIENT

# Technology
Role.DEVELOPER, Role.DEVOPS, Role.PRODUCT_MANAGER

# And more...
Role.EXECUTIVE, Role.MANAGER, Role.SUPPORT
```

### RoutingContext

Context for routing decisions:

```python
from tork.routing import RoutingContext, Sector, Role

context = RoutingContext(
    sector=Sector.HEALTHCARE,
    role=Role.DOCTOR,
    user_id="dr-smith",
    permissions=["view_patient_data", "prescribe"],
    metadata={"department": "cardiology"},
)
```

### RouteConfig

Define a route:

```python
from tork.routing import RouteConfig

route = RouteConfig(
    id="healthcare-doctor",
    target_agent="medical-assistant",
    target_persona="clinical-advisor",
    governance_policy="hipaa-compliant",
    allowed_actions=["diagnose_support", "drug_lookup", "cite_research"],
    blocked_actions=["prescribe", "diagnose_final"],
    max_cost=2.0,
)
```

## SectorRouter

Route requests based on context:

```python
from tork.routing import SectorRouter

router = SectorRouter()

# Register routes
router.register_route(
    sector=Sector.HEALTHCARE,
    roles=[Role.DOCTOR, Role.NURSE],
    config=healthcare_route,
)

# Route a request
result = router.route(context, request="What are the symptoms of...")

print(f"Routed to: {result.target_agent}")
print(f"Using persona: {result.target_persona}")
```

### Fallback Routes

Handle unmatched requests:

```python
router = SectorRouter(
    fallback_route=RouteConfig(
        id="default",
        target_agent="general-assistant",
    )
)

# If no sector/role match, uses fallback
result = router.route(unknown_context, request)
```

## RuleEngine

Flexible rule-based routing:

```python
from tork.routing import RoutingRule, RuleEngine

rule = RoutingRule(
    id="high-value-finance",
    priority=10,
    conditions={
        "sector": Sector.FINANCE,
        "role": Role.EXECUTIVE,
        "permission": "high_value_transactions",
    },
    route_config=premium_finance_route,
)

engine = RuleEngine()
engine.add_rule(rule)

# Evaluate rules
matched_route = engine.evaluate(context)
```

### Rule Priorities

Higher priority rules are evaluated first:

```python
# Priority 10 - checked first
vip_rule = RoutingRule(id="vip", priority=10, ...)

# Priority 5 - checked second
standard_rule = RoutingRule(id="standard", priority=5, ...)

# First matching rule wins
engine.add_rule(vip_rule)
engine.add_rule(standard_rule)
```

## Default Sector Routes

Pre-configured routes for common sectors:

```python
from tork.routing.defaults import (
    education_routes,
    healthcare_routes,
    finance_routes,
    legal_routes,
    technology_routes,
)

router = SectorRouter()

# Load all education routes
for route in education_routes():
    router.register_route(Sector.EDUCATION, route.roles, route.config)

# Load healthcare routes with HIPAA compliance
for route in healthcare_routes():
    router.register_route(Sector.HEALTHCARE, route.roles, route.config)
```

### Default Route Characteristics

| Sector | Governance Policy | Key Constraints |
|--------|------------------|-----------------|
| Education | content-appropriate | Age-appropriate content |
| Healthcare | hipaa-compliant | PII protection, medical disclaimers |
| Finance | financial-regulations | No financial advice, disclosures |
| Legal | legal-disclaimers | Not legal advice, jurisdiction limits |
| Technology | security-focused | Code safety, no credentials |

## Governance Per Route

Each route can have its own policy:

```python
from tork.core import GovernanceEngine

route = RouteConfig(
    id="hipaa-route",
    governance_policy="hipaa-compliant",
    # This route uses stricter PII redaction
)

# Router applies route-specific governance
result = router.route(healthcare_context, request)
# PII automatically redacted per HIPAA policy
```

## Example: Multi-Sector Application

```python
from tork.routing import SectorRouter, RoutingContext, Sector, Role, RouteConfig

# Create router
router = SectorRouter()

# Education routes
router.register_route(
    sector=Sector.EDUCATION,
    roles=[Role.STUDENT],
    config=RouteConfig(
        id="student-helper",
        target_persona="tutor",
        allowed_actions=["explain", "quiz", "encourage"],
        blocked_actions=["solve_homework"],
    ),
)

router.register_route(
    sector=Sector.EDUCATION,
    roles=[Role.TEACHER],
    config=RouteConfig(
        id="teacher-assistant",
        target_persona="curriculum-advisor",
        allowed_actions=["plan_lesson", "create_quiz", "grade_rubric"],
    ),
)

# Healthcare routes
router.register_route(
    sector=Sector.HEALTHCARE,
    roles=[Role.DOCTOR],
    config=RouteConfig(
        id="clinical-support",
        target_persona="medical-reference",
        governance_policy="hipaa",
        allowed_actions=["lookup_drug", "cite_research"],
    ),
)

# Route based on user context
def handle_request(user_sector, user_role, request):
    context = RoutingContext(sector=user_sector, role=user_role)
    result = router.route(context, request)
    
    # Execute with the matched persona/agent
    return execute_with_persona(result.target_persona, request)
```

## Convenience Methods

Quick routing shortcuts:

```python
# Route by sector only
result = router.route_by_sector(Sector.HEALTHCARE, request)

# Route by role only
result = router.route_by_role(Role.DEVELOPER, request)

# Get all routes for a sector
routes = router.get_sector_routes(Sector.FINANCE)
```

## Integration with Personas

Combine with the Personas module:

```python
from tork.routing import SectorRouter
from tork.personas import PersonaRuntime, PersonaStore

router = SectorRouter()
runtime = PersonaRuntime()
store = PersonaStore()

# Route determines which persona to use
result = router.route(context, request)

# Execute the matched persona
output = runtime.execute(
    result.target_persona,
    request,
    store,
)
```
