import os
import sys

from dotenv import load_dotenv

load_dotenv()

os.environ["DEPLOYMENT"] = "development"
ROOT_PATH = os.path.expanduser(os.environ["ROOT_PATH"])
assert os.path.exists(ROOT_PATH), ROOT_PATH
sys.path.append(ROOT_PATH)

RQ_PATH = os.path.expanduser(os.environ["RQ_PATH"])


def run_rq(file_name: str):
    from tgen.scripts.modules.script_runner import ScriptRunner

    file_path = os.path.join(RQ_PATH, file_name)
    script_runner = ScriptRunner(file_path)
    script_runner.run()
    sys.exit()


if __name__ == "__main__":
    run_rq(sys.argv[1])
