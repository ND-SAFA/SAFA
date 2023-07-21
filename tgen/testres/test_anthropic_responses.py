from tgen.testres.test_open_ai_responses import TestResponseManager


def fake_anthropic_completion(prompt, **args):
    res = TestResponseManager(prompt, **args)
    return [{"completion": choice["text"]} for choice in res.choices]
