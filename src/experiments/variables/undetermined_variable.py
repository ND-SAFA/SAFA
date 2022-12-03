from experiments.variables.variable import Variable


class UndeterminedVariable(Variable):

    def __init__(self):
        super().__init__("UNDETERMINED")
