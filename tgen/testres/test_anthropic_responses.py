from tgen.testres.test_open_ai_responses import fake_open_ai_completion


def fake_anthropic_completion(prompt, **args):
    res = fake_open_ai_completion(prompt, **args)
    return [{"completion": choice["text"]} for choice in res.choices]
