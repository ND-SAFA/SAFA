from dataclasses import dataclass

from tgen.common.util.base_object import BaseObject
from tgen.common.constants.deliminator_constants import EMPTY_STRING


@dataclass
class PipelineArgs(BaseObject):
    """
    The pipeline configuration and arguments.
    """
    export_dir: str = EMPTY_STRING
    load_dir: str = EMPTY_STRING
    interactive_mode: bool = False

    def __post_init__(self):
        """
        Updates the load dir to match export dir if none is provided
        :return: None
        """
        if not self.load_dir:
            self.load_dir = self.export_dir

