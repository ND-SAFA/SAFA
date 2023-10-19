from typing import Any, List

from tgen.clustering.base.clustering_args import ClusteringArgs
from tgen.clustering.clustering_pipeline import ClusteringPipeline
from tgen.clustering.steps.add_clusters_to_dataset import AddClustersToDataset
from tgen.data.creators.prompt_dataset_creator import PromptDatasetCreator
from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.data.exporters.safa_exporter import SafaExporter
from tgen.jobs.abstract_job import AbstractJob


class ClusteringJob(AbstractJob):
    def __init__(self, dataset_creator: TraceDatasetCreator, export_dir: str, add_to_dataset: bool = True,
                 artifact_types: List[str] = None):
        """
        Initializes job for given dataset creator.
        :param dataset_creator: The creator used to get dataset to cluster.
        :param export_dir: Path to where clusters should be exported.
        :param add_to_dataset: Whether to add clusters to the dataset.
        """
        super().__init__()
        self.dataset_creator = dataset_creator
        self.export_dir = export_dir
        self.add_to_dataset = add_to_dataset
        self.artifact_types = artifact_types

    def _run(self) -> Any:
        """
        Runs clustering pipeline on dataset and exports the results
        """
        prompt_dataset_creator = PromptDatasetCreator(trace_dataset_creator=self.dataset_creator)
        args = ClusteringArgs(dataset_creator=prompt_dataset_creator, add_to_dataset=self.add_to_dataset,
                              export_dir=self.export_dir, artifact_types=self.artifact_types)
        pipeline = ClusteringPipeline(args, summarizer_args=None, skip_summarization=True)

        pipeline.run()

        if self.artifact_types is None:
            self.artifact_types = args.dataset.trace_dataset.artifact_df.get_artifact_types()

        if self.add_to_dataset:
            dataset = pipeline.args.dataset.trace_dataset
            artifact_types = self.artifact_types + [AddClustersToDataset.CLUSTER_ARTIFACT_TYPE]
            exporter = SafaExporter(export_path=self.export_dir, dataset=dataset, artifact_types=artifact_types)
            exporter.export()
            return {"success": True, "path": self.export_dir}
        return {"success": True, "path": self.export_dir}
