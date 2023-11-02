import os
from typing import Dict

from tgen.common.constants.hugging_face_constants import SMALL_EMBEDDING_MODEL
from tgen.scripts.modules.script_definition import ScriptDefinition
from tgen.scripts.modules.script_runner import ScriptRunner
from tgen.testres.object_creator import ObjectCreator


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


def train(dataset_path: str, model: str = SMALL_EMBEDDING_MODEL):
    """
    Trains a model on the given dataset.
    :param dataset_path: Path to folder defining dataset.
    :param model: The starting model to train off with.
    :return: None
    """
    dataset_path = os.path.expanduser(dataset_path)
    replacements = {
        "[MODEL]": model,
        "[DATA_PATH]": os.path.dirname(dataset_path),
        "[CURRENT_PROJECT]": os.path.basename(dataset_path),
        "[OUTPUT_PATH]": os.path.expanduser(os.environ["OUTPUT_PATH"])
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
