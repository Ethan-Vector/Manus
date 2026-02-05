from manus_agent.guardrails.policy import OutputPolicy

def test_policy_trims_and_caps():
    p = OutputPolicy(max_chars=5)
    assert p.apply("  hello world ") == "hello…"
