import os
from typing import List

from tgen.scripts.modules.script_definition import ScriptDefinition
from tgen.scripts.modules.script_runner import ScriptRunner
from tgen.scripts.toolset.core.rq_proxy import RQProxy
from tgen.scripts.toolset.core.selector import inquirer_selection
from tgen.testres.object_creator import ObjectCreator

DATA_PATH = os.environ.get("DATA_PATH", None)


def run() -> None:
    """
    Navigates and runs RQ.
    :return: None
    """
    base_rq_path = os.path.join(get_rq_path(), "base")
    rq_to_run = navigate_to_rq(base_rq_path)
    run_rq(rq_to_run)


def navigate_to_rq(curr_path: str) -> str:
    items = os.listdir(curr_path)
    item_paths = [os.path.join(curr_path, i) for i in items]
    files = [i for i in item_paths if os.path.isfile(i) and ".json" in i]
    if len(files) > 0:
        return navigate_to_rq_from_files(curr_path, files)
    return navigate_to_rq_from_folder(curr_path, item_paths)


def navigate_to_rq_from_folder(curr_path: str, item_paths: List[str]):
    folders = [i for i in item_paths if os.path.isdir(i)]
    folder_names = [os.path.basename(f) for f in folders]
    folder_selected = inquirer_selection(folder_names, "Select RQ Folder", allow_back=True)
    if folder_selected is None:
        return go_back(curr_path)
    return navigate_to_rq(os.path.join(curr_path, folder_selected))


def navigate_to_rq_from_files(curr_path: str, files: List[str]):
    file_names = [os.path.basename(f) for f in files]
    file_selected = inquirer_selection(file_names, "Select RQ to run", allow_back=True)
    if file_selected is not None:
        return os.path.join(curr_path, file_selected)
    else:
        return go_back(curr_path)


def go_back(curr_path):
    back_path = os.path.normpath(os.path.join(curr_path, ".."))
    return navigate_to_rq(back_path)


def run_rq(rq_path: str):
    experiment_path = os.path.expanduser(rq_path)
    rq_proxy = RQProxy(experiment_path)

    os_variables = {f"[{env_key}]": env_value for env_key, env_value in os.environ.items()}
    replacements = rq_proxy.inquirer_unknown_variables(os_variables)

    experiment_definition = ScriptDefinition.read_experiment_definition(experiment_path, replacements)
    experiment_class = ScriptRunner.get_experiment_class(experiment_definition)
    experiment = ObjectCreator.create(experiment_class, override=True, **experiment_definition)
    experiment.run()


def get_rq_path() -> str:
    return os.path.expanduser(os.environ["RQ_PATH"])


RQ_TOOLS = [run]
