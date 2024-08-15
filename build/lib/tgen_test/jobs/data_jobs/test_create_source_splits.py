import itertools
import os

import pandas as pd

from common_resources.data.creators.trace_dataset_creator import TraceDatasetCreator
from common_resources.data.dataframes.artifact_dataframe import ArtifactDataFrame
from common_resources.data.keys.structure_keys import ArtifactKeys
from common_resources.data.exporters.safa_exporter import SafaExporter
from tgen.jobs.abstract_job import AbstractJob
from tgen.jobs.components.args.job_args import JobArgs
from tgen.jobs.data_jobs.create_source_splits_job import CreateSourceSplitsJob
from tgen.testres.base_tests.base_job_test import BaseJobTest
from tgen.testres.object_creator import ObjectCreator
from tgen.testres.paths.paths import TEST_OUTPUT_DIR

ARTIFACT_TYPE = "source_{}"
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
        for layer_mapping_i, layer_mapping_row in job.exporter._dataset.layer_df.itertuples():
            task_name = f"task_{layer_mapping_i}"
            source_artifacts = {}
            for stage in stages:
                stage_path = os.path.join(TEST_OUTPUT_DIR, task_name, stage)
                assert os.path.exists(stage_path)
                stage_path = os.path.join(stage_path, ARTIFACT_TYPE.format(layer_mapping_i + 1) + ".csv")
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
