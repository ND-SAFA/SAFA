from typing import Dict, List, Tuple, Set, Optional

from tgen.common.constants.model_constants import get_best_default_llm_manager_short_context
from tgen.common.objects.artifact import Artifact
from tgen.common.objects.trace import Trace
from tgen.common.util.enum_util import EnumDict
from tgen.contradictions.requirements_converter import RequirementsConverter
from tgen.contradictions.with_decision_tree.contradiction_decision_nodes import SupportedContradictionDecisionNodes
from tgen.contradictions.with_decision_tree.contradictions_tree_builder import ContradictionsTreeBuilder
from tgen.contradictions.with_decision_tree.requirement import Requirement
from tgen.core.trainers.llm_trainer import LLMTrainer
from tgen.core.trainers.llm_trainer_state import LLMTrainerState
from tgen.data.keys.structure_keys import TraceKeys, ArtifactKeys
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.decision_tree.nodes.llm_node import LLMNode
from tgen.decision_tree.path import Path
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager
from tgen.prompts.prompt_builder import PromptBuilder


class ContradictionsDetectorWithTree:
    TREE = ContradictionsTreeBuilder().build_tree()

    def __init__(self, trace_dataset: TraceDataset, export_path: str = None, llm_manager: AbstractLLMManager = None):
        """
        Handles detecting contradictions in requirements.
        :param trace_dataset: Contains the requirements.
        :param export_path: Where to export responses to.
        :param llm_manager: The LLM manager to use to make decisions.
        """
        self.trace_dataset = trace_dataset
        self.export_path = export_path
        self.llm_manager = get_best_default_llm_manager_short_context() if not llm_manager else llm_manager

    def detect_all(self) -> Dict[str, List[int]]:
        """
        Traverses a decision tree for each requirement pair to determine if a contradiction exists.
        :return: A dictionary mapping type of contradiction to the id of all links identified as having that type of contradiction.
        """
        id2requirement = self.create_requirements([a for _, a in self.trace_dataset.artifact_df.itertuples()], self.export_path)
        contradictions = {contradiction.value.description: [] for contradiction in SupportedContradictionDecisionNodes
                          if contradiction != SupportedContradictionDecisionNodes.NONE}

        links = self.trace_dataset.trace_df.get_links()

        link2path: Dict[int, Path] = {}
        links_with_decisions: Set[int] = set()
        choices = []
        while len(links_with_decisions) != len(links):
            choices = iter(choices)
            prompt_builders = []
            for link in links:
                link_id = link[TraceKeys.LINK_ID]
                if link_id in links_with_decisions:
                    continue

                current_path = link2path.get(link_id)
                last_choice = next(choices, None)
                if last_choice:
                    current_path.add_decision(last_choice)
                input_ = self._create_input_for_tree(link, id2requirement)
                if not input_:
                    links_with_decisions.add(link_id)
                    continue

                prompt_builder, path = self.TREE.next_step(input_, current_path)
                link2path[link_id] = path

                decision = path.get_final_decision()
                if decision:
                    links_with_decisions.add(link_id)
                    if decision in contradictions:
                        contradictions[decision].append(link_id)
                else:
                    prompt_builders.append(prompt_builder)
            choices = self._get_llm_choices(prompt_builders)
        return contradictions

    @staticmethod
    def detect_single_pair(artifact1: Artifact, artifact2: Artifact) -> Path:
        """
        Runs the detection for a single pair of artifacts..
        :param artifact1: The first artifact.
        :param artifact2: The second artifact.
        :return: The path taken when traversing the tree.
        """
        id2requirement = ContradictionsDetectorWithTree.create_requirements([artifact1, artifact2])
        if any([req.is_empty() for req in id2requirement.values()]):
            raise Exception("Failed to convert artifact to requirement - bad response.")
        link = Trace(source=artifact1[ArtifactKeys.ID], target=artifact2[ArtifactKeys.ID])
        input_ = ContradictionsDetectorWithTree._create_input_for_tree(link, id2requirement)
        path = ContradictionsDetectorWithTree.TREE.traverse(input_)
        return path

    @staticmethod
    def create_requirements(artifacts: List[Artifact], export_path: str = None) -> Dict[int, Requirement]:
        """
        Creates requirements from the artifacts.
        :param artifacts: The artifacts to convert to requirements.
        :param export_path: Path to save the LLM output to.
        :return: Map of requirement id to the requirement.
        """
        requirements = RequirementsConverter(export_path=export_path).convert_artifacts(artifacts)
        id2requirement = {req.id: req for req in requirements}
        return id2requirement

    @staticmethod
    def _create_input_for_tree(link: EnumDict, id2requirement: Dict[int, Requirement]) -> Optional[Tuple[Requirement, Requirement]]:
        """
        Creates the input for the decision tree.
        :param link: The current link to be examined.
        :param id2requirement: Maps requirement ids to their content.
        :return: The input for the decision tree.
        """
        r_id1, r_id2 = link[TraceKeys.child_label()], link[TraceKeys.parent_label()]
        req1, req2 = id2requirement[r_id1], id2requirement[r_id2]
        if req1.is_empty() or req2.is_empty():
            return
        input_ = (req1, req2)
        return input_

    def _get_llm_choices(self, prompt_builders: List[PromptBuilder]) -> List[str]:
        """
        Gets the LLM's next round of choices for each node.
        :param prompt_builders: List of prompt builders for each node.
        :return: The next round of choices for each node.
        """
        if len(prompt_builders) == 0:
            return []
        trainer = LLMTrainer(LLMTrainerState(prompt_builders=prompt_builders, llm_manager=self.llm_manager))
        res = trainer.perform_prediction()
        choices = [LLMNode.parse_response(r) for r in res.predictions]
        return choices
