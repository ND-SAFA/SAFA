from typing import Dict, List

from tgen.data.keys.structure_keys import TraceKeys
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.requirements_contradictions.contradiction_decision_nodes import SupportedContradictionDecisionNodes
from tgen.requirements_contradictions.contradictions_tree_builder import ContradictionsTreeBuilder
from tgen.requirements_contradictions.requirements_converter import RequirementsConverter


class ContradictionsDetector:

    def __init__(self, trace_dataset: TraceDataset):
        """
        Handles detecting contradictions in requirements.
        :param trace_dataset: Contains the requirements.
        """
        self.trace_dataset = trace_dataset

    def detect(self) -> Dict[str, List[int]]:
        """
        Traverses a decision tree for each requirement pair to determine if a contradiction exists.
        :return: A dictionary mapping type of contradiction to the id of all links identified as having that type of contradiction.
        """
        artifacts = [a for _, a in self.trace_dataset.artifact_df.itertuples()]
        requirements = RequirementsConverter().convert_artifacts(artifacts)
        id2requirement = {req.id: req for req in requirements}
        decision_tree = ContradictionsTreeBuilder().build_tree()
        contradictions = {contradiction.value.description: [] for contradiction in SupportedContradictionDecisionNodes
                          if contradiction.name != SupportedContradictionDecisionNodes.NONE}
        for link in self.trace_dataset.trace_df.get_links():
            req1 = id2requirement[link[TraceKeys.child_label()]]
            req2 = id2requirement[link[TraceKeys.parent_label()]]
            path = decision_tree.traverse((req1, req2))
            decision = path.get_final_decision()
            if decision in contradictions:
                contradictions[decision].append(link[TraceKeys.LINK_ID])
        return contradictions
