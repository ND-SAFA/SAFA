from experiments.variables.variable import Variable


class UndeterminedVariable(Variable):

    def __init__(self):
        """
        A variable that has an unknown value (used in experiments where previous runs influence values in subsequent runs)
        """
        super().__init__("UNDETERMINED")
