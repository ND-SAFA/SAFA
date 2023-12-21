import uuid
from dataclasses import dataclass, field
from typing import Union


@dataclass
class DeterministicUniqueIDManager:
    base_seed: Union[str, uuid.UUID] = field(default_factory=uuid.uuid4)
    _iteration_num: int = field(init=False, default=0)
    _uuid: str = field(init=False, default=None)

    def generate_new_id(self) -> None:
        """
        Creates a new id for using the same base seed.
        :return: None
        """
        self._uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, str(self.base_seed) + str(self._iteration_num)))
        self._iteration_num += 1

    def get_uuid(self) -> str:
        """
        Gets the current id.
        :return: The current id.
        """
        if self._uuid is None:
            self.generate_new_id()
        return self._uuid


