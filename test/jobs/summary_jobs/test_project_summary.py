from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.jobs.summary_jobs.project_summary_job import ProjectSummaryJob
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.test_data_manager import TestDataManager


class TestProjectSummary(BaseTest):
    def test_single_artifact(self):
        project_reader = TestDataManager.get_project_reader()
        dataset_creator = TraceDatasetCreator(project_reader=project_reader)
        job = ProjectSummaryJob(dataset_creator=dataset_creator)
