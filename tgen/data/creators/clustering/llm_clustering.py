import random

import bs4
from bs4 import BeautifulSoup
from typing import List, Tuple, Optional

from tgen.constants.deliminator_constants import NEW_LINE, COMMA, EMPTY_STRING
from tgen.data.creators.clustering.iclustering import Clusters, iClustering
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame, ArtifactKeys
from tgen.data.keys.prompt_keys import PromptKeys
from tgen.data.prompts.generation_prompt_creator import GenerationPromptCreator
from tgen.data.prompts.supported_prompts import SupportedPrompts
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager
from tgen.models.llm.anthropic_manager import AnthropicManager
from tgen.models.llm.llm_responses import GenerationResponse
from tgen.models.llm.llm_task import LLMCompletionType
from tgen.models.llm.token_limits import TokenLimitCalculator, ModelTokenLimits
from tgen.train.trainers.trainer_task import TrainerTask


class LLMClustering(iClustering):
    CLUSTER_TAG = 'group'
    CLUSTER_id_TAG = 'summary'
    CLUSTER_ARTIFACTS_TAG = 'artifacts'
    ARTIFACT_CONTENT_FORMAT = "{}) {}" + NEW_LINE
    DEFAULT_LLM_MANAGER = AnthropicManager

    @staticmethod
    def cluster(trace_dataset: TraceDataset, llm_manager: AbstractLLMManager = None, **kwargs) -> Clusters:
        """
        Performs clustering by using the model to predict artifact groups
        :param llm_manager: The LLM manager to use for the prediction
        :param trace_dataset: The dataset containing artifacts to cluster
        :return: The mapping of cluster names to list of artifacts in the cluster
        """
        artifact_df = trace_dataset.artifact_df
        llm_manager = LLMClustering.DEFAULT_LLM_MANAGER() if llm_manager is None else llm_manager
        contents = [LLMClustering.format_artifact_content(i, content) for i, content in enumerate(artifact_df[ArtifactKeys.CONTENT])]

        prompt_creator = GenerationPromptCreator(llm_manager.prompt_args, SupportedPrompts.CLUSTERING)
        prompt = prompt_creator.create(NEW_LINE.join(contents))[PromptKeys.PROMPT]

        # TODO handle this case in the future
        error_msg = "LLM Clustering is currently only supported for models with token limits greater than the combined " \
                    "artifact content and max tokens length."
        n_tokens = TokenLimitCalculator.estimate_num_tokens(prompt, llm_manager.llm_args.model) + llm_manager.llm_args.get_max_tokens()
        assert n_tokens <= ModelTokenLimits.get_token_limit_for_model(llm_manager.llm_args.model), error_msg

        params = llm_manager.llm_args.to_params(TrainerTask.PREDICT, LLMCompletionType.GENERATION)
        res = llm_manager.make_completion_request(completion_type=LLMCompletionType.GENERATION, prompt=prompt, **params)

        return LLMClustering._get_clusters_from_response(res, artifact_df)

    @staticmethod
    def _get_clusters_from_response(res: GenerationResponse, artifact_df: ArtifactDataFrame) -> Clusters:
        """
        Gets the clusters from the LLM response
        :param res: The response from the LLM
        :param artifact_df: The dataframe of all artifacts
        :return: Mapping of cluster name to the list of artifacts in the cluster
        """
        groups = BeautifulSoup(res.batch_responses[0], features="lxml").findAll(LLMClustering.CLUSTER_TAG)
        artifact_ids = list(artifact_df.index)
        clusters = {}
        for group in groups:
            name, artifacts = LLMClustering._get_cluster_name_and_artifacts(group, artifact_ids)
            if name and artifacts:
                clusters[name] = artifacts
        return clusters

    @staticmethod
    def _get_cluster_name_and_artifacts(group: bs4.Tag, artifact_ids: List[str]) -> Tuple[str, List[str]]:
        """
        Gets the name of the cluster and the artifacts associated with it
        :param group: The group tag containing cluster information
        :param artifact_ids: The ordered list of artifact ids mapping to the artifact numbers
        :return: The name of the cluster and the artifacts associated with it
        """
        name, artifacts = '', []  # defaults
        for child in group.children:
            if isinstance(child, bs4.Tag) and child.contents is not None and len(child.contents) > 0:
                if child.name == LLMClustering.CLUSTER_id_TAG:
                    name = child.contents[0]
                if child.name == LLMClustering.CLUSTER_ARTIFACTS_TAG:
                    artifacts = [LLMClustering._get_artifact_id_by_num(num, artifact_ids) for num in child.contents[0].split(COMMA)]
        return name.strip(), [artifact for artifact in artifacts if artifact is not None]

    @staticmethod
    def format_artifact_content(num: int, content: str) -> str:
        """
        Formats the artifact content to be used for the prompt
        :param num: The number of the artifact
        :param content: The content of the artifact
        :return: The formatted content
        """
        content = content.replace(NEW_LINE, EMPTY_STRING)
        return LLMClustering.ARTIFACT_CONTENT_FORMAT.format(num, content)

    @staticmethod
    def _get_artifact_id_by_num(num: str, ordered_ids: List[str]) -> Optional[str]:
        """
        Gets the artifact id by its number if it exists
        :param num: The number of the artifact as a string
        :param ordered_ids: The ordered list of artifact ids mapping to the artifact numbers
        :return: The artifact id if it exists
        """
        try:
            return ordered_ids[int(num)]
        except (IndexError, ValueError):
            return None
