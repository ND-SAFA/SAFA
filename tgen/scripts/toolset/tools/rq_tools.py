import os

from tgen.common.constants.hugging_face_constants import SMALL_EMBEDDING_MODEL
from tgen.scripts.modules.script_definition import ScriptDefinition
from tgen.scripts.modules.script_runner import ScriptRunner
from tgen.testres.object_creator import ObjectCreator


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
    experiment_path = os.path.join(os.environ["RQ_PATH"], "base/huggingface/train.json")
    experiment_path = os.path.expanduser(experiment_path)
    experiment_definition = ScriptDefinition.read_experiment_definition(experiment_path, replacements)
    experiment_class = ScriptRunner.get_experiment_class(experiment_definition)
    experiment = ObjectCreator.create(experiment_class, override=True, **experiment_definition)
    experiment.run()


RQ_TOOLS = [train]
