from dataclasses import dataclass

from tgen.util.base_object import BaseObject


@dataclass
class PipelineArgs:
    """
    The pipeline configuration and arguments.
    """
    pass


@dataclass
class PipelineState(BaseObject):
    """
    Represents a state of an object in time
    """
    pass
