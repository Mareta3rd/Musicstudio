from musicstudio.agent_audit import build_agent_audit
from musicstudio.agent_loop import AgentEvaluation, AgentIteration


def test_agent_audit_is_reconstructable():
    iterations = (
        AgentIteration(1, {'answer': 'a'}, AgentEvaluation('continue', 'refine')),
        AgentIteration(2, {'answer': 'b'}, AgentEvaluation('accept', 'ok')),
    )
    audit = build_agent_audit('lyricist', 'project-1', {'brief': 'x'}, iterations, 'accepted')
    assert audit.agent_id == 'lyricist'
    assert len(audit.iterations) == 2
    assert audit.iterations[0]['decision'] == 'continue'
    assert audit.final_reason == 'ok'
    assert len(audit.input_fingerprint) == 64