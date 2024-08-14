from dataclasses import dataclass, field
from typing import Any, Dict, List, Set, Union

from common_resources.data.tdatasets.prompt_dataset import PromptDataset
from common_resources.data.tdatasets.trace_dataset import TraceDataset
from common_resources.tools.state_management.state import State

from tgen.clustering.base.cluster_type import ClusterIdType
from tgen.common.objects.trace import Trace
from tgen.common.util.clustering_util import ClusteringUtil
from tgen.relationship_manager.embeddings_manager import EmbeddingsManager


@dataclass
class HGenState(State):
    """
    Step 1 - Dataset Construction
    """
    source_dataset: PromptDataset = None  # The dataset containing the original artifacts.
    original_dataset: Union[TraceDataset, PromptDataset] = None

    """
    Step 2 - Input generation
    """
    description_of_artifact: str = None  # describes what the target type is
    format_of_artifacts: str = None  # The format to use for the generated artifacts
    questions: List[str] = None  # The questions to use to probe the model for a good summary
    example_artifact: str = None  # An example of the desired artifact

    """
    Optional Step 3 - Break project into parts and generate for each part
    """
    cluster2artifacts: dict = None  # maps cluster id to the list of artifacts in that cluster
    cluster2cohesion: dict = None  # maps cluster id to the avg pairwise sim for that cluster
    seed2artifact_ids: ClusterIdType = None  # If given seeds, maps seeds to cluster artifacts.
    cluster_id2seeds: Dict = None  # If given seeds, maps cluster to seed.
    cluster_dataset: PromptDataset = None  # contains prompt dataset with just the artifact df of the clusters.
    embedding_manager: EmbeddingsManager = None  # allows embeddings to be reused

    """
    Step 4 - Artifact generation
    """
    generations2sources: Dict[str, Set[str]] = None  # dictionary mapping generated content to a list of related source ids
    cluster2generations: Dict[Any, List[str]] = None  # Maps cluster id to the generation that was produced for that cluster

    """
    Optional Step 5 - Refine content on rerun of hgen
    """
    # maps cluster id to the list of artifacts in that cluster
    refined_cluster2artifacts: Dict[int, Dict] = field(default_factory=dict)
    # The final selected artifact content
    refined_generations2sources: Dict[int, Dict[str, Set[str]]] = field(default_factory=dict)
    # Maps cluster id to the generation produced for that cluster
    refined_cluster2generation: Dict[int, Dict[Any, List[str]]] = field(default_factory=dict)

    """
    Step 6 - Rename the artifacts generated.
    """
    new_artifact_dataset: PromptDataset = None  # Dataset containing only the new generated artifacts.
    id_to_related_children: Dict[str, Set[str]] = None  # Maps new artifact names to the artifacts in their cluster.
    all_artifacts_dataset: PromptDataset = None  # Dataset containing source and new artifacts.

    """
    Optional Step 7 - generate trace links between source and target artifacts
    """
    trace_predictions: List[Trace] = None  # list of traces between source and target artifacts
    selected_predictions: List[Trace] = None  # met the criteria required to count as a trace

    """
    Step 8 - remove duplicate artifacts
    """
    selected_artifacts_dataset: PromptDataset = None  # contains all artifacts except those that were duplicated

    """
    Step Final - Dataset Construction
    """
    final_dataset: PromptDataset = None  # The final dataset with generated artifacts.

    def get_cluster_ids(self) -> List[str]:
        """
        :return: Returns the ordered list of clustered ids.
        """
        return list(self.cluster_dataset.artifact_df.index)

    def get_cluster2artifacts(self, ids_only: bool = False):
        """
        Optionally returns the map from cluster ids to list of artifacts in cluster if clustering is enabled.
        :param ids_only: If True, only returns the ids of th artifacts in the cluster else the full artifacts.
        :return: Map if clusters are available, otherwise none.
        """
        cluster2artifacts = self.get_most_recent_refinement_run(self.refined_cluster2artifacts) \
            if self.refined_cluster2artifacts else self.cluster2artifacts
        if not ids_only:
            cluster2artifacts = ClusteringUtil.replace_ids_with_artifacts(cluster2artifacts, self.source_dataset.artifact_df) \
                if self.cluster2artifacts else None
        return cluster2artifacts

    def get_generations2sources(self) -> Dict[str, Set[str]]:
        """
        Gets the dictionary mapping the generated targets to the suggested sources.
        :return: The dictionary mapping the generated targets to the suggested sources.
        """
        return self.get_most_recent_refinement_run(self.refined_generations2sources) \
            if self.refined_generations2sources else self.generations2sources

    def get_cluster2generation(self) -> Dict[Any, List[str]]:
        """
        Gets the dictionary mapping cluster id to the generations that came from it.
        :return: The dictionary mapping cluster id to   the generations that came from it.
        """
        return self.get_most_recent_refinement_run(self.refined_cluster2generation) \
            if self.refined_cluster2generation else self.cluster2generations

    @staticmethod
    def get_most_recent_refinement_run(refinement_dict: Dict) -> Any:
        """
        Gets the most recent refinement version.
        :param refinement_dict: The refinement dictionary to get the most recent version from.
        :return: The most recent refinement version.
        """
        latest_version = max(refinement_dict.keys())
        return refinement_dict[latest_version]
