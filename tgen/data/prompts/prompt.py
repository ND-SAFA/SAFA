import re
from uuid import UUID


class Prompt(str):
    """
    Represents a prompt with special formatting that allows delaying the formatting of certain fields
    """

    def __init__(self, value: str):
        """
        Initialize with the value of the prompt
        :param value: The value of the prompt
        """
        self.value = value

    def format(self, *args: object, **kwargs: object) -> str:
        """
        Overrides string format to allow the formatting of only selective fields
        :param args: Ordered params to format the prompt with
        :param kwargs: Key, value pairs to format the prompt with
        """
        formatting_fields = re.findall(r'\{(\w*)\}', self.value)
        updated_args = [arg for arg in args]
        for i, field in enumerate(formatting_fields):
            if kwargs and field not in kwargs:
                kwargs[field] = '{%s}' % field
            if args and i >= len(args):
                updated_args.append('{%s}' % field)
        return self.__class__(super().format(*updated_args, **kwargs))


class ArtGenPrompt(Prompt):

    def format(self, *args: object, **kwargs: object) -> str:
        """
        Overrides string format to allow the formatting of only selective fields
        :param args: Ordered params to format the prompt with
        :param kwargs: Key, value pairs to format the prompt with
        """
        if isinstance(kwargs.get("artifact_id", None), UUID):
            kwargs["artifact_id"] = ""
        return super().format(*args, **kwargs)
