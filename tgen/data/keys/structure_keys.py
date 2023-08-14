from enum import Enum
from typing import List


class StructuredKeys:
    """
    Keys used in the STRUCTURE project format.
    """
    ARTIFACTS = "artifacts"
    TRACES = "traces"
    PARSER = "parser"
    COLS = "cols"
    PATH = "path"
    CONVERSIONS = "conversions"
    PARAMS = "params"
    OVERRIDES = "overrides"
    SCORE = "score"

    class Trace(Enum):
        LINK_ID = "link_id"
        SOURCE = "source"
        TARGET = "target"
        LABEL = "label"
        SCORE = "score"
        EXPLANATION = "explanation"

        @classmethod
        def get_cols(cls, excluded: List["Trace"] = None) -> List["Trace"]:
            """
            :param: excluded: The columns excluded in the returned list.
            :return: Returns the list of columns in trace dataframe.
            """
            if excluded is None:
                excluded = [cls.LINK_ID]
            trace_columns = [trace_col for trace_col in StructuredKeys.Trace if trace_col not in excluded]
            return trace_columns

    class Artifact(Enum):
        ID = "id"
        CONTENT = "content"
        LAYER_ID = "layer_id"

    class LayerMapping(Enum):
        SOURCE_TYPE = "source_type"
        TARGET_TYPE = "target_type"
