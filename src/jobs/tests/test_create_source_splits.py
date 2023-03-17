import itertools
import os

import pandas as pd

from data.creators.trace_dataset_creator import TraceDatasetCreator
from data.dataframes.artifact_dataframe import ArtifactDataFrame, ArtifactKeys
from data.exporters.safa_exporter import SafaExporter
from data.keys.structure_keys import StructuredKeys
from jobs.abstract_job import AbstractJob
from jobs.components.job_args import JobArgs
from jobs.create_source_splits_job import CreateSourceSplitsJob
from jobs.tests.base_job_test import BaseJobTest
from testres.paths.paths import TEST_OUTPUT_DIR
from util.object_creator import ObjectCreator

ARTIFACT_TYPE = "source_type_{}"
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

    def _assert_success(self, job: CreateSourceSplitsJob, output_dict: dict):
        """
        Verifies that source artifacts are not overlappign between splits.
        """
        stages = ["train", "val", "eval"]
        for layer_mapping_i, layer_mapping_row in job.exporter.dataset.layer_mapping_df.iterrows():
            task_name = f"task_{layer_mapping_i}"
            source_artifacts = {}
            for stage in stages:
                stage_path = os.path.join(TEST_OUTPUT_DIR, task_name, stage)
                assert os.path.exists(stage_path)
                stage_path = os.path.join(stage_path, ARTIFACT_TYPE.format(layer_mapping_i) + ".csv")
                df = pd.read_csv(stage_path)
                df[ArtifactKeys.LAYER_ID.value] = [ARTIFACT_TYPE for i in range(len(df.index))]
                artifact_df = ArtifactDataFrame(df)
                source_artifacts[stage] = set(artifact_df.index.unique())

            for s1, s2 in itertools.product(stages, stages):
                if s1 == s2:
                    continue
                s_set = source_artifacts[s1]
                t_set = source_artifacts[s2]
                diff_set = s_set.intersection(t_set)
                self.assertEqual(0, len(diff_set), msg=f"Task: {task_name}, {s1} x {s2}: {diff_set}")

    def _get_job(self, artifact_type=ARTIFACT_TYPE) -> AbstractJob:
        """
        Constructs source split job.
        """
        job_args = JobArgs()
        trace_dataset_creator = ObjectCreator.create(TraceDatasetCreator)
        return CreateSourceSplitsJob(SafaExporter(export_path=TEST_OUTPUT_DIR, dataset_creator=trace_dataset_creator),
                                     SPLITS, job_args)
