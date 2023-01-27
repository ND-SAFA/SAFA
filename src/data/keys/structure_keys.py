from typing import List


class StructuredKeys:
    """
    Keys used in the STRUCTURE project format.
    """

    class Trace:
        SOURCE = "source"
        TARGET = "target"
        LABEL = "label"

    class Artifact:
        ID = "id"
        BODY = "content"
        LAYER_ID = "layer_id"

    class LayerMapping:
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

    @staticmethod
    def get_artifact_cols() -> List[str]:
        """
        :return:Returns the columns of the DataFrame containing artifacts.
        """
        return [StructuredKeys.Artifact.ID, StructuredKeys.Artifact.BODY, StructuredKeys.Artifact.LAYER_ID]

    @staticmethod
    def get_trace_cols() -> List[str]:
        """
        :return:Returns the columns of the DataFrame containing trace links.
        """
        return [StructuredKeys.Trace.SOURCE, StructuredKeys.Trace.TARGET, StructuredKeys.Trace.LABEL]
