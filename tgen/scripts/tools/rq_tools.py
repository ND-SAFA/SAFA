import os
from typing import List, Optional

from tgen.scripts.constants import FOLDER_NAV_MESSAGE, PARENT_FOLDER, RQ_NAV_MESSAGE, RQ_PATH_PARAM
from tgen.scripts.modules.script_definition import ScriptDefinition
from tgen.scripts.modules.script_runner import ScriptRunner
from tgen.scripts.toolset.rq_definition import RQDefinition
from tgen.scripts.toolset.selector import inquirer_selection
from tgen.testres.object_creator import ObjectCreator


def find_and_run_rq() -> None:
    """
    Navigates and runs RQ.
    :return: None
    """
    base_rq_path = os.path.join(get_rq_path(), "base")
    rq_path = navigate_to_rq(base_rq_path)
    run_rq(rq_path)


def navigate_to_rq(curr_path: str) -> str:
    """
    Navigates the user from current path until they have selected a RQ.
    :param curr_path: The current path in the selection process.
    :return: Path to selected RQ.
    """
    items = os.listdir(curr_path)
    item_paths = [os.path.join(curr_path, i) for i in items]
    files = [i for i in item_paths if os.path.isfile(i) and ".json" in i]
    folders = [i for i in item_paths if os.path.isdir(i)]
    if len(files) > 0:
        rq_selected = navigate_to_rq_from_files(files)
    else:
        rq_selected = select_folder_to_navigate(folders)

    if rq_selected is None:
        return navigate_parent_folder(curr_path)
    else:
        return rq_selected


def select_folder_to_navigate(folder_paths: List[str]) -> Optional[str]:
    """
    Allows users to navigate within a selected folder.
    :param folder_paths: Paths of folders to select from.
    :return: Path to selected RQ or None if user selected to go back.
    """
    folder_names = [os.path.basename(f) for f in folder_paths]
    folder_selected = inquirer_selection(folder_names, FOLDER_NAV_MESSAGE, allow_back=True)
    folder_index = folder_names.index(folder_selected)
    folder_selected_path = folder_paths[folder_index]
    if folder_selected is None:
        return None
    return navigate_to_rq(folder_selected_path)


def navigate_to_rq_from_files(file_paths: List[str]) -> Optional[str]:
    """
    Allows users to select an RQ file.
    :param file_paths: List of RQ paths to select from.
    :return: Path to selected RQ or None if user selected to go back.
    """
    file_names = [os.path.basename(f) for f in file_paths]
    file_selected = inquirer_selection(file_names, RQ_NAV_MESSAGE, allow_back=True)
    file_selected_index = file_names.index(file_selected)
    if file_selected is None:
        return None
    return file_paths[file_selected_index]


def navigate_parent_folder(curr_path: str) -> str:
    """
    Allows user to navigate the parent direct of given path.
    :param curr_path: The current path the user is wanting to search above.
    :return: Path to selected RQ.
    """
    back_path = os.path.normpath(os.path.join(curr_path, PARENT_FOLDER))
    return navigate_to_rq(back_path)


def run_rq(rq_path: str) -> None:
    """
    Runs the RQ by prompting user to fill in any missing variables.
    :param rq_path: The path to the RQ to run.
    :return: None
    """
    experiment_path = os.path.expanduser(rq_path)
    rq_definition = RQDefinition(experiment_path)

    rq_definition.set_default_values(use_os_values=True)
    rq_definition.inquirer_variables()
    final_rq_json = rq_definition.build_rq(error_on_fail=True)

    final_rq_json = ScriptDefinition.set_output_paths(final_rq_json, rq_definition.script_name)
    experiment_class = ScriptRunner.get_experiment_class(final_rq_json)
    experiment = ObjectCreator.create(experiment_class, override=True, **final_rq_json)
    experiment.run()


def get_rq_path() -> str:
    """
    :return: Returns expanded RQ path.
    """
    return os.path.expanduser(os.environ[RQ_PATH_PARAM])


RQ_TOOLS = [find_and_run_rq]
