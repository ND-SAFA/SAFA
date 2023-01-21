from typing import Dict, NamedTuple


class TraceOutputUtil:
    """
    Contains utility methods for processing the trace_output of the trace trainer.
    """

    @staticmethod
    def output_to_dict(output: NamedTuple, **kwargs) -> Dict:
        """
        Converts train/prediction trace_output to a dictionary
        :param output: trace_output from training or prediction
        :return: the trace_output represented as a dictionary
        """
        base_output = {field: kwargs[field] if (field in kwargs and kwargs[field]) else getattr(output, field) for field
                       in output._fields}
        additional_attrs = {field: kwargs[field] for field in kwargs.keys() if field not in base_output}
        return {**base_output, **additional_attrs}
