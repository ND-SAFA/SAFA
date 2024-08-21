import asyncio
from typing import Any, Dict

from langchain_core.runnables.base import Runnable

from gen_common.util.pythonisms_util import default_mutable


class ExceptionOptions:
    ALL = "all"
    NONE = "none"
    ASYNC_ONLY = "async_only"
    SYNC_ONLY = "sync_only"


class LangchainUtil:

    @staticmethod
    @default_mutable()
    def optionally_run_async(runnable: Runnable, run_async: bool, inputs: Dict = None,
                             raise_exception: str = ExceptionOptions.ALL) -> Any:
        """
        Optionally runs the langchain runnable async otherwise normal invocation.
        :param runnable: The langchain runnable.
        :param run_async: If True, runs async.
        :param inputs: The inputs to the runnable.
        :param raise_exception: When to raise exception (see exception options abooe).
        :return: The result from the runnable.
        """
        try:
            if run_async:
                response = asyncio.run(runnable.ainvoke(inputs))
            else:
                response = runnable.invoke(inputs)
            return response

        except Exception as e:
            match (raise_exception, run_async):
                case (ExceptionOptions.ALL, _) | (ExceptionOptions.ASYNC_ONLY, True) | (ExceptionOptions.SYNC_ONLY, False):
                    raise e
            return e
