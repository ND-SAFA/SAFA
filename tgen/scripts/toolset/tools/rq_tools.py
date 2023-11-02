import os

from tgen.scripts.modules.script_definition import ScriptDefinition
from tgen.scripts.run import run_rq


def train(model: str, dataset_path: str):
    """
    Runs RQ.
    :param rq: RQ path.
    :return:
    """
    data_path = os.environ["CURRENT_PROJECT"]
    replacements = {
        "MODEL": model,
        "CURRENT_PROJECT": os.path.relpath(dataset_path, start="MODEL")
    }
    experiment_path = "base/huggingface/train.json"
    ScriptDefinition.read_experiment_definition()
    run_rq(rq)


RQ_TOOLS = [train]
