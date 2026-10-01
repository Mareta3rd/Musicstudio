from musicstudio.agents.registry import AgentRegistry, CostClass


def test_registry_contains_full_core_team():
    registry = AgentRegistry()
    ids = {agent.id for agent in registry.all()}
    assert {"producer", "lyricist", "prosody", "mixer", "polisher", "mastering", "qa"} <= ids


def test_capability_lookup():
    registry = AgentRegistry()
    agents = registry.capable_of("rhyme")
    assert any(agent.id == "lyricist" for agent in agents)
    assert any(agent.id == "prosody" for agent in agents)


def test_cost_policy_defaults_to_local():
    registry = AgentRegistry()
    assert all(agent.default_cost == CostClass.FREE_LOCAL for agent in registry.all())
