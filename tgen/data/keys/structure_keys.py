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
        def get_cols(cls) -> List["Trace"]:
            """
            :return: Returns the list of columns in trace dataframe.
            """
            trace_columns = [trace_col for trace_col in StructuredKeys.Trace if trace_col != StructuredKeys.Trace.LINK_ID]
            return trace_columns

    class Artifact(Enum):
        ID = "id"
        CONTENT = "content"
        LAYER_ID = "layer_id"

    class LayerMapping(Enum):
        SOURCE_TYPE = "source_type"
        TARGET_TYPE = "target_type"
