import argparse
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

    parser = argparse.ArgumentParser(
        prog='Experiment',
        description='Runs experiment definitions')
    parser.add_argument('file')
    args = parser.parse_args()
    file_path = os.path.join(RQ_PATH, args.file)
    script_runner = ScriptRunner(file_path)
    script_runner.print_results()
    sys.exit()
