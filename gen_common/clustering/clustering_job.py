from typing import Any, List

from gen_common.data.exporters.safa_exporter import SafaExporter
from gen_common.jobs.abstract_job import AbstractJob
from gen_common.jobs.job_args import JobArgs

from gen_common.clustering.base.clustering_args import ClusteringArgs
from gen_common.clustering.clustering_pipeline import ClusteringPipeline


class ClusteringJob(AbstractJob):
    def __init__(self, job_args: JobArgs, artifact_types: List[str] = None, add_to_dataset: bool = True, **kwargs):
        """
        Initializes job for given dataset creator.
        :param job_args: Arguments general to most jobs.
        :param add_to_dataset: Whether to add clusters to the dataset.
        :param artifact_types: The artifact types to cluster.
        """
        super().__init__(job_args, require_data=True)
        self.add_to_dataset = add_to_dataset
        self.artifact_types = artifact_types
        self.kwargs = kwargs

    def _run(self) -> Any:
        """
        Runs clustering pipeline on dataset and exports the results
        """
        args = ClusteringArgs(dataset=self.job_args.dataset, create_dataset=self.add_to_dataset,
                              artifact_types=self.artifact_types, export_dir=self.job_args.export_dir,
                              **self.kwargs)
        pipeline = ClusteringPipeline(args, summarizer_args=None, skip_summarization=True)

        pipeline.run()

        if self.artifact_types is None:
            self.artifact_types = args.dataset.trace_dataset.artifact_df.get_artifact_types()

        if self.add_to_dataset:
            dataset = pipeline.state.cluster_dataset.trace_dataset
            # TODO : Test with new cluster dataset creator.
            artifact_types = self.artifact_types + [args.cluster_artifact_type]
            exporter = SafaExporter(export_path=self.job_args.export_dir, dataset=dataset, artifact_types=artifact_types)
            exporter.export()
            return {"success": True, "path": self.job_args.export_dir}
        return {"success": True, "path": self.job_args.export_dir}
