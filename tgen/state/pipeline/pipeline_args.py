from dataclasses import dataclass

from tgen.common.util.base_object import BaseObject
from tgen.constants.deliminator_constants import EMPTY_STRING


@dataclass
class PipelineArgs(BaseObject):
    """
    The pipeline configuration and arguments.
    """
    export_dir: str = None
    load_dir: str = EMPTY_STRING

