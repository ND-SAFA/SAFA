from typing import List
from unittest import TestCase

from gen_common.data.tdatasets.prompt_dataset import PromptDataset
from gen_common.jobs.job_args import JobArgs
from gen_common.util.status import Status
from gen_common_test.base.mock.decorators.anthropic import mock_anthropic
from gen_common_test.base.mock.decorators.chat import mock_chat_model
from gen_common_test.base.mock.langchain.test_chat_model import TestResponseManager
from gen_common_test.base.mock.test_ai_manager import TestAIManager

from gen.health.health_job import HealthCheckJob
from gen.health.health_state import HealthState
from gen.health.types.health_tasks import HealthTask
from gen_test.health.health_task_verifier import HealthTaskVerifier


def run_health_test_case(tc: TestCase,
                         task: HealthTask,
                         verifier: HealthTaskVerifier):
    """
    Runs test case where health task is performed.
    :param tc: Test case used to make assertions.
    :param task: Task to be performed.
    :param verifier: Verifier used to create mock responses and verifier state.
    :return:  None
    """

    @mock_chat_model
    @mock_anthropic
    def test_func(_, ai_manager: TestAIManager, chat_manager: TestResponseManager):
        verifier.mock_responses(ai_manager, chat_manager)
        dataset, query_ids = verifier.get_test_data()
        job = _create_job(task, dataset=dataset, query_ids=query_ids)
        state = _run_task(tc, job)
        verifier.verify_state(tc, state)

    test_func()


def _create_job(task: HealthTask, dataset: PromptDataset, query_ids: List[str]) -> HealthCheckJob:
    """
    Creates health check job.
    :param task: The task to perform in the job.
    :param dataset: The dataset to run job on.
    :param query_ids: Ids of target artifacts
    :return: Health Job.
    """
    job = HealthCheckJob(
        JobArgs(dataset=dataset),
        query_ids=query_ids,
        tasks=[task]
    )
    return job


def _run_task(tc, job: HealthCheckJob) -> HealthState:
    """
    Runs health task.
    :param job: The job to run.
    :return: The state containing task result.
    """
    job_result = job.run()
    tc.assertEqual(Status.SUCCESS, job_result.status, msg="Job was not successfully executed.")
    state: HealthState = job_result.body
    return state
