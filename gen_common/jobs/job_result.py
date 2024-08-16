import json
from dataclasses import dataclass, field
from typing import Any, Dict, Union
from uuid import UUID

from gen_common.llm.args.hugging_face_args import HuggingFaceArgs
from gen_common.tools.util.base_object import BaseObject
from gen_common.tools.util.json_util import JsonUtil
from gen_common.tools.util.status import Status


@dataclass
class JobResult(BaseObject):
    job_id: Union[UUID, str]
    status: Union[Status, int] = Status.UNKNOWN
    body: Any = None
    experimental_vars: Dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        """
        Sets the job ID to be proper UUID.
        :return:  None
        """
        if not isinstance(self.job_id, UUID):
            self.job_id = UUID(self.job_id)

    def to_json(self, as_dict: bool = False) -> Union[str, Dict]:
        """
        Returns the job output as json
        :param as_dict: Whether to return job result as JSON string or dictionary.
        :return: the output as json
        """
        obj = self.as_dict()
        if as_dict:
            return obj
        return JsonUtil.dict_to_json(obj)

    def as_dict(self) -> dict:
        """
        Returns the results as a dictionary
        :return: the results as a dictionary
        """
        return vars(self)

    @staticmethod
    def from_dict(dict_: Dict) -> "JobResult":
        """
        Creates a JobResult from a dictionary
        :param dict_: The dictionary used to initialize the job result.
        :return: a new JobResult
        """
        return JobResult.initialize_from_definition(dict_)

    @staticmethod
    def from_json(json_input: str) -> "JobResult":
        """
        Creates a JobResult from json
        :param json_input: The JSON String to parse as a job result.
        :return: a new JobResult
        """
        dict_ = json.loads(json_input)
        return JobResult.from_dict(dict_)

    def get_printable_experiment_vars(self) -> str:
        """
        Gets the experimental vars as a string which can be printed
        :return: Experimental vars as a string
        """
        if len(self.experimental_vars) < 1:
            return "No experimental vars."
        printable = {}
        for name, val in self.experimental_vars.items():
            from gen_common.tools.util.base_object import BaseObject
            if not isinstance(val, BaseObject) and not isinstance(val, HuggingFaceArgs):
                printable[name] = val
        return repr(printable)

    def __eq__(self, other: "JobResult") -> bool:
        """
        Returns True if the two results are equal
        :param other: The other job result to compare
        :return: True if the two results are equal
        """
        for name, val in vars(self).items():
            if getattr(self, name) != getattr(other, name):
                return False
        return True
