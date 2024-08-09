from common_resources.tools.variables.variable import Variable


class UndeterminedVariable(Variable):
    SYMBOL = "?"

    def __init__(self):
        """
        A variable that has an unknown value (used in experiments where previous runs influence values in subsequent runs)
        """
        super().__init__("UNDETERMINED")
