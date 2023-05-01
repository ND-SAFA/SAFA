import os
import sys

from dotenv import load_dotenv

load_dotenv()

ROOT_PATH = os.path.expanduser(os.environ["ROOT_PATH"])
assert os.path.exists(ROOT_PATH), ROOT_PATH
sys.path.append(ROOT_PATH)

RQ_PATH = os.path.expanduser(os.environ["RQ_PATH"])
if __name__ == "__main__":
    from tgen.scripts.modules.script_runner import ScriptRunner

    file_name = sys.argv[1]
    file_path = os.path.join(RQ_PATH, file_name)
    script_runner = ScriptRunner(file_path)
    script_runner.run()
    script_runner.print_results()
    script_runner.upload_results()
    sys.exit()
