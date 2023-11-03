import os
from typing import Dict

from tgen.common.constants.hugging_face_constants import SMALL_EMBEDDING_MODEL
from tgen.scripts.modules.script_definition import ScriptDefinition
from tgen.scripts.modules.script_runner import ScriptRunner
from tgen.testres.object_creator import ObjectCreator

DATA_PATH = os.environ.get("DATA_PATH", None)


def push(input_model_path: str, model_name: str):
    """
    Pushes input model to the bug (under thearod5)
    :param input_model_path: Path to model to push.
    :param model_name: The name of the model to save to.
    :return: None
    """
    input_model_path = os.path.expanduser(input_model_path)
    replacements = {
        "[MODEL_PATH]": input_model_path,
        "[MODEL_NAME]": model_name
    }
    run_rq("base/huggingface/push.json", replacements)


def train(train_path: str, eval_path: str, data_path: str = DATA_PATH, model: str = SMALL_EMBEDDING_MODEL):
    """
    Trains a model on the given dataset.
    :param train_path: Path to training data.
    :param eval_path: Path to evaluation data.
    :param data_path: Folder to where the data is stored. If none data paths are assumed to be complete.
    :param model: The starting model to train off with.
    :return: None
    """
    if data_path:
        data_path = os.path.expanduser(data_path)
        train_path = os.path.join(data_path, train_path)
        eval_path = os.path.join(data_path, eval_path)
    else:
        train_path = os.path.expanduser(train_path)
        eval_path = os.path.expanduser(eval_path)
    replacements = {
        "[MODEL]": model,
        "[TRAIN_PROJECT_PATH]": train_path,
        "[OUTPUT_PATH]": os.path.expanduser(os.environ["OUTPUT_PATH"]),
        "[EVAL_PROJECT_PATH]": eval_path
    }
    run_rq("base/huggingface/train_st.json", replacements)


def run_rq(rq_relative_path: str, replacements: Dict[str, str]):
    experiment_path = os.path.join(os.environ["RQ_PATH"], rq_relative_path)
    experiment_path = os.path.expanduser(experiment_path)
    experiment_definition = ScriptDefinition.read_experiment_definition(experiment_path, replacements)
    experiment_class = ScriptRunner.get_experiment_class(experiment_definition)
    experiment = ObjectCreator.create(experiment_class, override=True, **experiment_definition)
    experiment.run()


RQ_TOOLS = [train, push]
