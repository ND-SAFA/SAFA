import os
import sys

from dotenv import load_dotenv

ROOT_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..")
ROOT_PATH = os.path.normpath(ROOT_PATH)


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
    script_name, *envs = sys.argv[1:]
    if ".env" not in envs:
        envs.insert(0, ".env")
    for env in envs:
        env_path = os.path.join(ROOT_PATH, env)
        assert os.path.isfile(env_path), f"{env_path} is not file."
        load_dotenv(env_path)

    assert os.path.exists(ROOT_PATH), ROOT_PATH
    sys.path.append(ROOT_PATH)
    os.environ["DEPLOYMENT"] = "development"
    RQ_PATH = os.path.expanduser(os.environ["RQ_PATH"])
    run_script_runner(script_name)
