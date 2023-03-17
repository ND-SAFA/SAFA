import itertools
import os
from unittest import skip

import pandas as pd

from data.creators.trace_dataset_creator import TraceDatasetCreator
from data.keys.structure_keys import StructuredKeys
from jobs.abstract_job import AbstractJob
from jobs.components.job_args import JobArgs
from jobs.create_source_splits_job import CreateSourceSplitsJob
from jobs.tests.base_job_test import BaseJobTest
from testres.paths.paths import TEST_OUTPUT_DIR
from util.object_creator import ObjectCreator

ARTIFACT_TYPE = "source_type_0"
SPLITS = [0.2, 0.2]


class TestCreateSourceSplits(BaseJobTest):
    """
    Tests job's ability to slice sources and create new datasets while avoiding
    overlap between source artifacts.
    """

    def test_run_success(self):
        """
        Verifies that job completes successfully.
        :return:
        """
        self._test_run_success()

    def _assert_success(self, job: AbstractJob, output_dict: dict):
        """
        Verifies that source artifacts are not overlappign between splits.
        """
        stages = ["train", "val", "eval"]
        source_artifacts = {}
        for stage in stages:
            stage_path = os.path.join(TEST_OUTPUT_DIR, stage)
            assert os.path.exists(stage_path)
            stage_path = os.path.join(stage_path, ARTIFACT_TYPE + ".csv")
            artifact_df = pd.read_csv(stage_path)
            source_artifacts[stage] = list(artifact_df.index.unique())

        for s, t in itertools.product(stages, stages):
            if s == t:
                continue
            s_set = set(source_artifacts[s])
            t_set = set(source_artifacts[t])
            diff_set = s_set.intersection(t_set)
            self.assertEqual(0, len(diff_set), msg=f"{s} x {t}: {diff_set}")

    def _get_job(self, artifact_type=ARTIFACT_TYPE) -> AbstractJob:
        """
        Constructs source split job.
        """
        job_args = JobArgs()
        trace_dataset_creator = ObjectCreator.create(TraceDatasetCreator)
        return CreateSourceSplitsJob(job_args, trace_dataset_creator, TEST_OUTPUT_DIR, SPLITS, artifact_type)
