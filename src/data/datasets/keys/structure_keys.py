class StructureKeys:
    """
    Keys used in the STRUCTURE project format.
    """

    class Trace:
        SOURCE = "source"
        TARGET = "target"

    class Artifact:
        ID = "id"
        BODY = "content"

    PARSER = "parser"
    COLS = "cols"
    PATH = "path"
    CONVERSIONS = "conversions"
    PARAMS = "params"
    ARTIFACTS = "artifacts"
    TRACES = "traces"
