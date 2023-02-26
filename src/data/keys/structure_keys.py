from typing import Dict, Iterable, List, Tuple


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

    @staticmethod
    def create_task_definition(base_definition: Dict, update_iterator: Iterable[Tuple[str, List[str]]]) -> Dict:
        """
        Creates task definition by constructing subset of base definition.
        :param base_definition: The base definition containing referenced artifacts, traces, and overrides.
        :param update_iterator: Iterator containing instructions for what properties to copy over.
        :return: Task definition.
        """
        task_definition = StructuredKeys.create_empty_definition()
        for parent_prop_name, child_keys in update_iterator:
            for child_key in child_keys:
                task_definition[parent_prop_name][child_key] = base_definition[parent_prop_name][child_key]
        return task_definition

    @staticmethod
    def create_empty_definition() -> Dict:
        """
        Creates empty structure definition file.
        :return: Dictionary containing artifact, traces, and override properties.
        """
        return {StructuredKeys.ARTIFACTS: {}, StructuredKeys.TRACES: {}, StructuredKeys.OVERRIDES: {}}
