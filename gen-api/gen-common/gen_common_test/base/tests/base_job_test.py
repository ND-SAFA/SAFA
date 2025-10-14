import json
from abc import ABC, abstractmethod

from gen_common.jobs.abstract_job import AbstractJob
from gen_common.jobs.job_result import JobResult
from gen_common.util.status import Status
from gen_common_test.base.tests.base_trace_test import BaseTraceTest


class BaseJobTest(BaseTraceTest, ABC):
    def _test_run_success(self):
        job = self.get_job()
        job.run()
        self.assert_output_on_success(job, job.result)

    def get_job(self):
        return self._get_job()

    @staticmethod
    def _load_job_output(job: AbstractJob):
        with open(job.get_output_filepath(output_dir=job.job_args.output_dir)) as out_file:
            return JobResult.from_dict(json.load(out_file))

    def assert_output_on_success(self, job: AbstractJob, job_result: JobResult, **kwargs):
        self.assert_job_succeeded(job_result)
        self._assert_success(job, job_result, **kwargs)

    def assert_job_succeeded(self, job_result):
        if job_result.status == Status.FAILURE:
            failure_msg = job_result.body
            self.fail(failure_msg)
        self.assertEqual(job_result.status, Status.SUCCESS)

    def assert_output_on_failure(self, job_output: JobResult):
        self.assertEqual(job_output.status, Status.FAILURE)

    @abstractmethod
    def _assert_success(self, job: AbstractJob, job_result: JobResult):
        pass

    @abstractmethod
    def _get_job(self) -> AbstractJob:
        pass
