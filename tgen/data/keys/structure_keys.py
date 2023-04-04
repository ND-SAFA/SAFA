from enum import Enum


class StructuredKeys:
    """
    Keys used in the STRUCTURE project format.
    """

    class Trace(Enum):
        LINK_ID = "link_id"
        SOURCE = "source"
        TARGET = "target"
        LABEL = "label"

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
