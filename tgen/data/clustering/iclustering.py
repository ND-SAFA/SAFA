from abc import abstractmethod
from typing import Dict, List, Any, Union
from uuid import UUID

from tgen.data.tdatasets.trace_dataset import TraceDataset

Clusters = Dict[Union[UUID, str], List[Any]]


class iClustering:

    @staticmethod
    @abstractmethod
    def cluster(trace_dataset: TraceDataset, **kwargs) -> Clusters:
        """
        Creates clusters of artifacts
        :param trace_dataset: Contains the data for the clusters
        :param kwargs: Any input necessary to create the clusters
        :return: A mapping of cluster name to a list of artifacts in that cluster
        """
