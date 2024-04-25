import os
import sys

from dotenv import load_dotenv

RQ_PATH = os.path.expanduser(os.environ["RQ_PATH"])

sys.path.append(ROOT_PATH)
assert os.path.exists(ROOT_PATH), ROOT_PATH
load_dotenv()

os.environ["DEPLOYMENT"] = "development"
ROOT_PATH = os.path.expanduser(os.environ["ROOT_PATH"])


def run_script_runner(script_rel_path: str):
    """
    Runs the given script name.
    :param script_rel_path: Relative path to RQ from RQ path.
    :return: None
    """
    from tgen.scripts.modules.script_runner import ScriptRunner

    file_path = os.path.join(RQ_PATH, script_rel_path)
    script_runner = ScriptRunner(file_path)
    script_runner.run()
    sys.exit()


if __name__ == "__main__":
    run_script_runner(sys.argv[1])
