import os
from typing import List, Optional

from gen_common.infra.t_logging.logger_manager import logger
from gen_common.tools.cli.inquirer_selector import inquirer_selection
from gen_common.tools.rq.rq_definition import RQDefinition
from gen_common.util.file_util import FileUtil

from gen.infra.cli.constants import FOLDER_NAV_MESSAGE, PARENT_FOLDER, RQ_PATH_PARAM
from gen.infra.cli.modules.script_definition import ScriptDefinition
from gen.infra.cli.modules.script_runner import ScriptRunner
from gen_test.res import ObjectCreator


def find_and_run_rq() -> None:
    """
    Navigates and runs RQ.
    :return: None
    """
    rq_path = navigate_to_rq(get_rq_path())
    run_rq(rq_path)


def navigate_to_rq(curr_path: str) -> str:
    """
    Navigates the user from current path until they have selected a RQ.
    :param curr_path: The current path in the selection process.
    :return: Path to selected RQ.
    """
    items = os.listdir(curr_path)
    item_paths = [os.path.join(curr_path, i) for i in items]
    files = [i for i in item_paths if os.path.isfile(i) and FileUtil.JSON_EXT in i]
    folders = [i for i in item_paths if os.path.isdir(i)]
    if len(files) > 0:
        rq_selected = navigate_to_rq_from_files(files)
    else:
        rq_selected = select_folder_to_navigate(folders)

    if rq_selected is None:
        return navigate_parent_folder(curr_path)
    else:
        return rq_selected


def navigate_to_rq_from_files(file_paths: List[str]) -> Optional[str]:
    """
    Allows users to select an RQ file.
    :param file_paths: List of RQ paths to select from.
    :return: Path to selected RQ or None if user selected to go back.
    """
    return select_navigation_items(file_paths)


def select_folder_to_navigate(folder_paths: List[str]) -> Optional[str]:
    """
    Allows users to navigate within a selected folder.
    :param folder_paths: Paths of folders to select from.
    :return: Path to selected RQ or None if user selected to go back.
    """
    folder_selected = select_navigation_items(folder_paths)
    return None if folder_selected is None else navigate_to_rq(folder_selected)


def select_navigation_items(items: List[str]):
    """
    Prompts the user to select one of the items with the option to select the back command.
    :param items: The items to choose from.
    :return: The selected item or None is back is selected.
    """
    folder_names = [os.path.basename(f) for f in items]
    folder_selected = inquirer_selection(folder_names, FOLDER_NAV_MESSAGE, allow_back=True)
    if folder_selected is None:
        return None
    folder_index = folder_names.index(folder_selected)
    folder_selected_path = items[folder_index]
    return folder_selected_path


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

    ScriptDefinition.set_output_paths(rq_definition)
    rq_definition.set_default_values(use_os_values=True)
    try:
        rq_definition.fill_variables()
    except Exception:
        logger.warning("Going back to menu...")
        return
    final_rq_json = rq_definition.build_rq()

    experiment_class = ScriptRunner.get_experiment_class(final_rq_json)
    experiment = ObjectCreator.create(experiment_class, override=True, **final_rq_json)
    experiment.run()


def get_rq_path() -> str:
    """
    :return: Returns expanded RQ path.
    """
    return os.path.expanduser(os.environ[RQ_PATH_PARAM])


RQ_TOOLS = [find_and_run_rq]
