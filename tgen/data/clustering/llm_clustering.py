from copy import deepcopy
from typing import List, Tuple, Optional, Union

import bs4
from bs4.element import Tag

from tgen.constants.deliminator_constants import NEW_LINE, COMMA, EMPTY_STRING
from tgen.constants.open_ai_constants import MAX_TOKENS_BUFFER
from tgen.data.clustering.iclustering import Clusters, iClustering
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame, ArtifactKeys
from tgen.data.keys.prompt_keys import PromptKeys
from tgen.data.prompts.generation_prompt_creator import GenerationPromptCreator
from tgen.data.prompts.prompt import Prompt
from tgen.data.prompts.supported_prompts import SupportedPrompts
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager
from tgen.models.llm.anthropic_manager import AnthropicManager
from tgen.models.llm.llm_task import LLMCompletionType
from tgen.models.llm.token_limits import TokenLimitCalculator, ModelTokenLimits
from tgen.train.args.anthropic_args import AnthropicArgs
from tgen.train.trainers.trainer_task import TrainerTask
from tgen.util.llm_response_util import LLMResponseUtil
from tgen.util.logging.logger_manager import logger


class LLMClustering(iClustering):
    CLUSTER_TAG = 'group'
    FUNCTIONALITY_TAG = 'feature'
    CLUSTER_ARTIFACTS_TAG = 'artifacts'
    ARTIFACT_CONTENT_FORMAT = "{}) {} {}"
    DEFAULT_LLM_MANAGER = AnthropicManager
    RES_TOKENS_MIN = 500
    PERC_TOKENS_FOR_RES = 0.1
    CLUSTER_MAX = 10
    CLUSTER_MIN = 1

    @staticmethod
    def cluster(trace_dataset: TraceDataset, target_artifact_type: str, llm_manager: AbstractLLMManager = None, **kwargs) -> Clusters:
        """
        Performs clustering by using the model to predict artifact groups
        :param llm_manager: The LLM manager to use for the prediction
        :param trace_dataset: The dataset containing artifacts to cluster
        :param target_artifact_type: The goal artifact to get feature for
        :return: The mapping of cluster names to list of artifacts in the cluster
        """
        artifact_df = trace_dataset.artifact_df
        llm_manager = AnthropicManager(AnthropicArgs()) if llm_manager is None else llm_manager
        artifact_ids, artifact_content = list(artifact_df.index), artifact_df[ArtifactKeys.CONTENT]
        features = LLMClustering._get_features(artifact_ids, artifact_content, target_artifact_type, llm_manager)
        logger.info(f"\nCreating clusters for {len(features)} features")
        clusters = LLMClustering._get_clusters(artifact_ids, artifact_content, target_artifact_type, llm_manager, features)
        clusters = LLMClustering._recluster_large_groups(artifact_df, clusters, target_artifact_type, llm_manager)
        clusters = LLMClustering._recluster_small_groups(artifact_df, clusters, target_artifact_type, llm_manager)
        return clusters

    @staticmethod
    def _get_features(artifact_ids: List[str], artifact_content: List[str], target_artifact_type: str,
                      llm_manager: AbstractLLMManager) -> List[str]:
        """
        Gets feature across artifacts
        :param artifact_ids: The ids of the artifacts to get feature for
        :param artifact_content: The content of the artifacts to get feature for
        :param target_artifact_type: The goal artifact to get feature for
        :param llm_manager: The LLM to get feature from
        :return: The list of feature
        """
        logger.info(f"Getting features for clusters.")
        prompt = SupportedPrompts.FUNCTIONALITIES.value.format(target_artifact_type=target_artifact_type)
        res = LLMClustering._get_response(artifact_ids, artifact_content, llm_manager, prompt)
        features: List[Tag] = LLMResponseUtil.parse(res, LLMClustering.FUNCTIONALITY_TAG, is_nested=True)
        return [str(functionality.contents[0]) for functionality in features]

    @staticmethod
    def _get_clusters(artifact_ids: List[str], artifact_content: List[str], target_artifact_type: str,
                      llm_manager: AbstractLLMManager, features: Union[List[str], str],
                      base_prompt: Union[SupportedPrompts, Prompt] = SupportedPrompts.CLUSTER_FROM_FEATURES) -> Clusters:
        """
        Gets clusters of the given artifacts using the llm manager
        :param artifact_ids: Ids of all artifacts to cluster
        :param artifact_content: Content of all artifacts to cluster
        :param target_artifact_type: The goal artifact to get feature for
        :param llm_manager: LLM to use to create clusters
        :param features: Functionalities to cluster by
        :return: The clusters
        """
        if isinstance(base_prompt, SupportedPrompts):
            base_prompt = base_prompt.value
        prompt = base_prompt.format(features=features, target_artifact_type=target_artifact_type)
        res = LLMClustering._get_response(artifact_ids, artifact_content, llm_manager, prompt)
        clusters = LLMClustering._get_clusters_from_response(res, artifact_ids)
        return clusters

    @staticmethod
    def _recluster_large_groups(artifact_df: ArtifactDataFrame, clusters: Clusters, target_artifact_type: str,
                                llm_manager: AbstractLLMManager) -> Clusters:
        """
        Re-clusters groups of artifacts above the threshold
        :param artifact_df: Contains the original artifacts
        :param clusters: The clusters
        :param target_artifact_type: The goal artifact to get feature for
        :param llm_manager: LLM to use to create clusters
        :return: The updated clusters with large groups re-clustered
        """
        for cluster_name, artifacts in deepcopy(clusters).items():
            if len(artifacts) > LLMClustering.CLUSTER_MAX:
                logger.info(f"\nRe-clustering a group with more than {LLMClustering.CLUSTER_MAX} artifacts")
                artifact2cluster = clusters.pop(cluster_name)
                artifact_content = [artifact_df.get_artifact(id_)[ArtifactKeys.CONTENT] for id_ in artifact2cluster]
                prompt = SupportedPrompts.RE_CLUSTER_FEATURE.value.format(feature=cluster_name)
                clusters.update(LLMClustering._get_clusters(artifact2cluster, artifact_content, target_artifact_type,
                                                            llm_manager, features=list(clusters.keys()),
                                                            base_prompt=prompt))
        return clusters

    @staticmethod
    def _recluster_small_groups(artifact_df: ArtifactDataFrame, clusters: Clusters, target_artifact_type: str,
                                llm_manager: AbstractLLMManager) -> Clusters:
        """
        Re-clusters groups of artifacts below the threshold
        :param artifact_df: Contains the original artifacts
        :param clusters: The clusters
        :param target_artifact_type: The goal artifact to get feature for
        :param llm_manager: LLM to use to create clusters
        :return: The updated clusters with small groups re-clustered
        """
        okay_clusters = {name: artifacts for name, artifacts in clusters.items() if len(artifacts) > LLMClustering.CLUSTER_MIN}
        clustered_artifacts = {a for artifacts in okay_clusters.values() for a in artifacts}
        artifact2cluster = [artifact for artifact in artifact_df.index.values if artifact not in clustered_artifacts]
        if len(artifact2cluster) < 0:
            return clusters
        logger.info(f"\nRe-clustering groups with less than {LLMClustering.CLUSTER_MIN} artifacts")
        artifact_content = [artifact_df.get_artifact(id_)[ArtifactKeys.CONTENT] for id_ in artifact2cluster]
        new_clusters = LLMClustering._get_clusters(artifact2cluster, artifact_content, target_artifact_type, llm_manager,
                                                   features=list(clusters.keys()))
        for name, artifacts in new_clusters.items():
            if name in okay_clusters:
                okay_clusters[name].extend(artifacts)
            else:
                okay_clusters[name] = artifacts
        return okay_clusters

    @staticmethod
    def _get_response(artifact_ids: List[str], artifact_content: List[str], llm_manager: AbstractLLMManager,
                      prompt: Union[SupportedPrompts, str]) -> str:
        """
        Gets the response for a given prompt from the LLM
        :param artifact_ids: List of artifact ids to use in prompt
        :param artifact_content: List of artifact content to use in prompt
        :param llm_manager: The LLM to use for response
        :param prompt: The base prompt to use
        :return: The response from the LLM
        """
        contents = [LLMClustering.format_artifact_content(i, artifact_ids[i], content) for i, content in enumerate(artifact_content)]
        prompt_creator = GenerationPromptCreator(llm_manager.prompt_args, prompt)
        prompt = prompt_creator.create(NEW_LINE.join(contents))[PromptKeys.PROMPT]
        LLMClustering._set_max_tokens(llm_manager, prompt)
        params = llm_manager.llm_args.to_params(TrainerTask.PREDICT, LLMCompletionType.GENERATION)
        res = llm_manager.make_completion_request(completion_type=LLMCompletionType.GENERATION, prompt=prompt, **params)
        return res.batch_responses[0]

    @staticmethod
    def _get_clusters_from_response(res: str, artifact_ids: List[str]) -> Clusters:
        """
        Gets the clusters from the LLM response
        :param res: The response from the LLM
        :param artifact_ids: The ids of all artifacts
        :return: Mapping of cluster name to the list of artifacts in the cluster
        """
        groups = LLMResponseUtil.parse(res, LLMClustering.CLUSTER_TAG, is_nested=True)
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
                if child.name == LLMClustering.FUNCTIONALITY_TAG:
                    name = child.contents[0]
                if child.name == LLMClustering.CLUSTER_ARTIFACTS_TAG:
                    artifacts = [LLMClustering._get_artifact_id_by_num(num, artifact_ids) for num in child.contents[0].split(COMMA)]
        return name.strip(), [artifact for artifact in artifacts if artifact is not None]

    @staticmethod
    def _set_max_tokens(llm_manager: AbstractLLMManager, prompt: str) -> int:
        """
        Tries to find the optimal number of tokens to set for the model's response
        :param llm_manager: The LLM Manager being used for the clustering
        :param prompt: The prompt being used for the clustering
        :return: The max tokens that the model was set to
        """
        n_tokens = TokenLimitCalculator.estimate_num_tokens(prompt, llm_manager.llm_args.model)
        model_token_limit = ModelTokenLimits.get_token_limit_for_model(llm_manager.llm_args.model)
        tokens_available = model_token_limit - n_tokens - MAX_TOKENS_BUFFER
        max_tokens = max(LLMClustering.RES_TOKENS_MIN, min(tokens_available, model_token_limit * LLMClustering.PERC_TOKENS_FOR_RES))
        # TODO handle this case in the future
        error_msg = "LLM Clustering is currently only supported for models with token limits greater than the combined " \
                    "artifact content and max tokens length."
        assert tokens_available >= max_tokens, error_msg
        llm_manager.llm_args.set_max_tokens(max_tokens)
        return max_tokens

    @staticmethod
    def format_artifact_content(num: int, id_: str, content: str) -> str:
        """
        Formats the artifact content to be used for the prompt
        :param num: The number of the artifact
        :param id_: The id of the artifact
        :param content: The content of the artifact
        :return: The formatted content
        """
        content = content.replace(NEW_LINE, EMPTY_STRING)
        return LLMClustering.ARTIFACT_CONTENT_FORMAT.format(num, id_, content)

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
