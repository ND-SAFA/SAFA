import os
from typing import List

from sklearn.model_selection import train_test_split

from data.creators.trace_dataset_creator import TraceDatasetCreator
from data.exporters.safa_exporter import SafaExporter
from data.keys.structure_keys import StructuredKeys
from jobs.abstract_job import AbstractJob
from jobs.components.job_args import JobArgs
from jobs.components.job_result import JobResult


class CreateSourceSplits(AbstractJob):

    def __init__(self, job_args: JobArgs, trace_dataset_creator: TraceDatasetCreator, export_path: str, splits: List[float],
                 artifact_type: str):
        super().__init__(job_args)
        self.trace_dataset_creator = trace_dataset_creator
        self.export_path = export_path
        self.splits = splits
        self.artifact_type = artifact_type

    def _run(self) -> JobResult:
        trace_dataset = self.trace_dataset_creator.create()
        artifacts_df = self.trace_dataset_creator.artifact_df
        layer_mapping_df = self.trace_dataset_creator.layer_mapping_df
        assert self.artifact_type in artifacts_df[
            StructuredKeys.Artifact.LAYER_ID].unique(), "Type not contained in layer artifact df."
        target_artifacts = artifacts_df[artifacts_df[StructuredKeys.Artifact.LAYER_ID] == self.artifact_type]

        target_ids = list(target_artifacts[StructuredKeys.Artifact.ID])
        val_total = self.splits[0] + self.splits[1]
        train_ids, val_ids = train_test_split(target_ids, test_size=val_total)
        val_ids, test_ids = train_test_split(val_ids, test_size=self.splits[1] / val_total)
        split_id_batches = [train_ids, val_ids, test_ids]

        for split_ids, stage in zip(split_id_batches, ["train", "val", "eval"]):
            all_ids = set(target_ids + val_ids + test_ids)
            other_ids = all_ids - set(split_ids)
            split_artifact_ids_mask = artifacts_df[StructuredKeys.Artifact.ID].isin(other_ids)
            layer_mask = artifacts_df[StructuredKeys.Artifact.LAYER_ID] == self.artifact_type
            split_artifact_df = artifacts_df[~(split_artifact_ids_mask & layer_mask)]
            split_links = {trace.id: trace for trace in
                           list(filter(lambda t: t.source not in other_ids and t.target not in other_ids,
                                       trace_dataset.links.values()))}
            export_path = os.path.join(self.export_path, f"{stage}")
            os.makedirs(export_path, exist_ok=True)
            exporter = SafaExporter()
            exporter.export(export_path, split_links, split_artifact_df, layer_mapping_df)
        return JobResult.from_dict({"status": "ok"})
