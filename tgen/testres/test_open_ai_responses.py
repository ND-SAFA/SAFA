from copy import deepcopy

from tgen.data.summarizer.summarizer import Summarizer
from tgen.hgen.hierarchy_generator import HierarchyGenerator
from tgen.models.llm.anthropic_manager import AnthropicManager
from tgen.models.llm.open_ai_manager import OpenAIManager
from tgen.util.attr_dict import AttrDict

FINE_TUNE_REQUEST = AttrDict({
    "training_file": "training_id",
    "validation_file": "validation_id",
    "model": "text-davinci-003",
    "n_epochs": 2,
    "batch_size": 4,
    "learning_rate_multiplier": 0.05,
    "prompt_loss_weight": 0.01,
    "compute_classification_metrics": False,
    "classification_n_classes": 2,
    "classification_positive_class": " yes",
    "suffix": "custom-model-name"
})

COMPLETION_REQUEST = AttrDict({
    "model": "text-davinci-003",
    "prompt": "Say this is a test",
    "max_tokens": 7,
    "temperature": 0,
    "top_p": 1,
    "n": 1,
    "stream": False,
    "logprobs": None,
    "stop": "\n"
})

FINE_TUNE_RESPONSE_DICT = AttrDict({
    "id": "ft-AF1WoRqd3aJAHsqc9NY7iL8F",
    "object": "fine-tune",
    "model": "curie",
    "created_at": 1614807352,
    "events": [
        AttrDict({
            "object": "fine-tune-event",
            "created_at": 1614807352,
            "level": "info",
            "message": "Job enqueued. Waiting for jobs ahead to complete. Queue number: 0."
        })
    ],
    "fine_tuned_model": None,
    "hyperparams": AttrDict({
        "batch_size": 4,
        "learning_rate_multiplier": 0.1,
        "n_epochs": 4,
        "prompt_loss_weight": 0.1,
    }),
    "organization_id": "org-...",
    "result_files": [],
    "status": "pending",
    "validation_files": [],
    "training_files": [
        AttrDict({
            "id": "file-XGinujblHPwGLSztz8cPS8XY",
            "object": "file",
            "bytes": 1547276,
            "created_at": 1610062281,
            "filename": "my-data-train.jsonl",
            "purpose": "fine-tune-train"
        })
    ],
    "updated_at": 1614807352,
})

COMPLETION_RESPONSE_DICT = AttrDict({
    "id": "cmpl-uqkvlQyYK7bGYrRHQ0eXlWi7",
    "object": "text_completion",
    "created": 1589478378,
    "model": "text-davinci-003",
    "choices": [
        AttrDict({
            "text": "\n\nThis is indeed a test",
            "index": 0,
            "logprobs": AttrDict({"top_logprobs": [
                AttrDict({
                    " yes": -0.6815379,
                    " no": -1.0818866
                })
            ]}),

            "finish_reason": "length"
        })
    ],
    "usage": AttrDict({
        "prompt_tokens": 5,
        "completion_tokens": 7,
        "total_tokens": 12
    })})

SUMMARY_FORMAT = "Summary of {}"


def fake_open_ai_completion(prompt, **args):
    choice = deepcopy(COMPLETION_RESPONSE_DICT["choices"][0])
    choice["text"] = SUMMARY_FORMAT
    tags = [HierarchyGenerator.GENERATION_TAG, Summarizer.SUMMARY_TAG]
    tag = None
    for t in tags:
        if f"<{t}>" in prompt[0]:
            tag = t
            break
    for prompt_suffix in [AnthropicManager.prompt_args.prompt_suffix, OpenAIManager.prompt_args.prompt_suffix]:
        success = False
        for p in prompt:
            if p.endswith(prompt_suffix):
                success = True
        if success:
            prompt = ["".join(p.rsplit(prompt_suffix, 1)) for p in prompt]
            break
    tokens = [p.replace("\n", "").split(f"</{tag}>")[-1] for p in prompt]
    choices = [deepcopy(choice) for _ in tokens]
    for i, c in enumerate(choices):
        c['text'] = c['text'].format(tokens[i])
        if tag:
            c['text'] = f"<{tag}>{c['text']}</{tag}>"
    res = AttrDict({"choices": choices, "id": "id"})
    return res
