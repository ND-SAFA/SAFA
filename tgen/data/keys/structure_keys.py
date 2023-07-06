from enum import Enum
from typing import List


class StructuredKeys:
    """
    Keys used in the STRUCTURE project format.
    """

    class Trace(Enum):
        LINK_ID = "link_id"
        SOURCE = "source"
        SCORE = "score"
        TARGET = "target"
        LABEL = "label"

        @staticmethod
        def get_cols() -> List["Trace"]:
            """
            :return: Returns the list of columns in trace dataframe.
            """
            return [StructuredKeys.Trace.SOURCE, StructuredKeys.Trace.TARGET, StructuredKeys.Trace.LABEL]

    class Artifact(Enum):
        ID = "id"
        CONTENT = "content"
        LAYER_ID = "layer_id"

    class LayerMapping(Enum):
        SOURCE_TYPE = "source_type"
        TARGET_TYPE = "target_type"

    ARTIFACTS = "artifacts"
    TRACES = "traces"
    PARSER = "parser"
    COLS = "cols"
    PATH = "path"
    CONVERSIONS = "conversions"
    PARAMS = "params"
    OVERRIDES = "overrides"
