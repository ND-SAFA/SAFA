import uuid
from dataclasses import dataclass


@dataclass
class PromptArgs:
    prompt_id: str = None
    title: str = None
    allow_formatting: bool = True
    system_prompt: bool = False
    structure_with_new_lines: bool = False

    def set_id(self, seed: int, overwrite_existing: bool = False) -> None:
        """
        Creates and updates the id for the prompt.
        :param seed: The seed for the id generation.
        :param overwrite_existing: If True, will set the id even if one already exists.
        :return: None.
        """
        if overwrite_existing or self.prompt_id is None:
            self.prompt_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, str(seed)))
