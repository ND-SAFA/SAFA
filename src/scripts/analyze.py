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
    from scripts.modules.script_runner import ScriptRunner
    from scripts.modules.script_analyzer import ScriptAnalyzer

    DEFAULT_ANALYSIS_OUTPUT = os.path.join(os.environ["OUTPUT_PATH"], "analysis-output")
    parser = argparse.ArgumentParser(
        prog='Experiment',
        description='Runs experiment definitions')
    parser.add_argument('file', nargs="+")
    parser.add_argument('--output_path', default=DEFAULT_ANALYSIS_OUTPUT)
    args = parser.parse_args()
    script_runners = []
    for file in args.file:
        file_path = os.path.join(RQ_PATH, file)
        script_runner = ScriptRunner(file_path)
        script_runners.append(script_runner)
    scripter_analyzer = ScriptAnalyzer(script_runners, args.output_path)
    scripter_analyzer.analyze()
    print("Analysis finished")
