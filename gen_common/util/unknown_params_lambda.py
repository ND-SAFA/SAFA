from typing import Callable

from gen_common.util.param_specs import ParamSpecs


class UnknownParamsLambda:

    def __init__(self, runnable: Callable, **known_params):
        """
        Used as lambda with kwargs and args.
        :param runnable: The runnable to call.
        :param known_params: Params to set ahead of time.
        """
        self.runnable = runnable
        self.known_params = known_params

    def __call__(self, *args, **kwargs):
        """
        Calls the runnable with all params.
        :param args:  Args to runnable.
        :param kwargs: Kwargs to runnable.
        :return: Tesult of runnable.
        """
        all_params = {**kwargs, **self.known_params}
        params = ParamSpecs.create_from_method(self.runnable).get_accepted_params(all_params)
        return self.runnable(**params)
