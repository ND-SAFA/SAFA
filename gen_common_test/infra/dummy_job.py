from typing import Any

from gen_common.jobs.abstract_job import AbstractJob


class DummyJob(AbstractJob):
    def _run(self) -> Any:
        print("hi")

    def get_output_filepath(self) -> str:
        return "hello"
