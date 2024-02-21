from typing import Dict, List

from tgen.common.logging.logger_manager import logger
from tgen.contradictions.contradiction_decision_nodes import SupportedContradictionDecisionNodes
from tgen.contradictions.contradictions_tree_builder import ContradictionsTreeBuilder
from tgen.contradictions.requirements_converter import RequirementsConverter
from tgen.data.keys.structure_keys import TraceKeys
from tgen.data.tdatasets.trace_dataset import TraceDataset


class ContradictionsDetector:

    def __init__(self, trace_dataset: TraceDataset, export_path: str = None):
        """
        Handles detecting contradictions in requirements.
        :param trace_dataset: Contains the requirements.
        """
        self.trace_dataset = trace_dataset
        self.export_path = export_path

    def detect(self) -> Dict[str, List[int]]:
        """
        Traverses a decision tree for each requirement pair to determine if a contradiction exists.
        :return: A dictionary mapping type of contradiction to the id of all links identified as having that type of contradiction.
        """
        artifacts = [a for _, a in self.trace_dataset.artifact_df.itertuples()]
        requirements = RequirementsConverter(export_path=self.export_path).convert_artifacts(artifacts)
        id2requirement = {req.id: req for req in requirements}
        decision_tree = ContradictionsTreeBuilder().build_tree()
        contradictions = {contradiction.value.description: [] for contradiction in SupportedContradictionDecisionNodes
                          if contradiction.name != SupportedContradictionDecisionNodes.NONE}
        for link in self.trace_dataset.trace_df.get_links():
            r_id1, r_id2 = link[TraceKeys.child_label()], link[TraceKeys.parent_label()]
            req1, req2 = id2requirement[r_id1], id2requirement[r_id2]
            try:
                path = decision_tree.traverse((req1, req2))
                decision = path.get_final_decision()
            except Exception:
                logger.exception(f"Unable to run contradiction detector between requirement {r_id1} and {r_id2}")
                decision = SupportedContradictionDecisionNodes.NONE.value
            if decision in contradictions:
                contradictions[decision].append(link[TraceKeys.LINK_ID])
        return contradictions
