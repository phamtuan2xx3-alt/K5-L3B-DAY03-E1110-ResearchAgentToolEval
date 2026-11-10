from agent import ResearchAgent
from providers.base import ModelResponse, ToolCall


def test_eval_records_model_send_but_never_executes_it(monkeypatch):
    class Provider:
        def complete(self, *args, **kwargs):
            return ModelResponse(tool_calls=[ToolCall("send", {"text": "Unapproved", "confirmed": True})])
    def must_not_send(**kwargs):
        raise AssertionError("Eval must not send external messages")
    monkeypatch.setitem(__import__("tools").TOOL_FUNCTIONS, "send", must_not_send)
    result = ResearchAgent(Provider(), system_prompt="test").run([{"role": "user", "content": "test"}], allow_actions=False)
    assert result.tool_calls[0].args["confirmed"] is True
    assert result.tool_results[0]["result"]["status"] == "blocked_in_eval"
