from typing import Any, Dict

from tgen.clustering.base.cluster import Cluster

ClusterType = Cluster
ClusterMapType = Dict[Any, ClusterType]
MethodClusterMapType = Dict[str, ClusterMapType]
