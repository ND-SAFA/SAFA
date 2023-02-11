from scripts.util.script_runner import ScriptRunner


class ScriptAnalyzer:
    """
    Reads evaluation output of jobs in experiment and runs statistics on them.
    """

    def __init__(self, script_runner: ScriptRunner):
        self.script_runner = script_runner

    def analyze(self):
        """
        Runs analysis on script
        :return:
        """
        experiment = self.script_runner.get_experiment()
        # Set the model used for evaluation (best)
        # Iterate through jobs and target jobs with evaluation output
        # Construct entities needed for analysis
