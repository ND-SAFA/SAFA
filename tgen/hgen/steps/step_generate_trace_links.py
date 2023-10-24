import os
from typing import Dict, Set
from typing import List

from tgen.common.constants.deliminator_constants import EMPTY_STRING
from tgen.common.constants.hgen_constants import WEIGHT_OF_PRED_RELATED_CHILDREN, DEFAULT_LINK_THRESHOLD, RELATED_CHILDREN_SCORE
from tgen.common.util.enum_util import EnumDict
from tgen.common.util.logging.logger_manager import logger
from tgen.common.util.math_util import MathUtil
from tgen.common.util.status import Status
from tgen.common.util.thread_util import ThreadUtil
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.keys.structure_keys import TraceKeys, ArtifactKeys
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.hgen.hgen_args import HGenArgs
from tgen.hgen.hgen_state import HGenState
from tgen.hgen.hgen_util import HGenUtil
from tgen.jobs.tracing_jobs.ranking_job import RankingJob
from tgen.state.pipeline.abstract_pipeline import AbstractPipelineStep
from tgen.tracing.ranking.common.ranking_args import RankingArgs
from tgen.tracing.ranking.common.ranking_util import RankingUtil
from tgen.tracing.ranking.embedding_ranking_pipeline import EmbeddingRankingPipeline
from tgen.tracing.ranking.selectors.select_by_threshold import SelectByThreshold
from tgen.tracing.ranking.supported_ranking_pipelines import SupportedRankingPipelines


class GenerateTraceLinksStep(AbstractPipelineStep[HGenArgs, HGenState]):

    def _run(self, args: HGenArgs, state: HGenState) -> None:
        """
        Generates trace links between the new generated artifacts and the source artifacts
        :param state: The current state of hgen at this point in time
        :param args: The arguments and current state of HGEN.
        :return: None
        """
        new_artifact_df, id_to_related_children = HGenUtil.create_artifact_df_from_generated_artifacts(args,
                                                                                                       state.refined_content,
                                                                                                       args.target_type)
        all_artifact_df = ArtifactDataFrame.concat(state.original_dataset.artifact_df, new_artifact_df)
        state.all_artifacts_dataset = PromptDataset(artifact_df=all_artifact_df, project_summary=args.dataset.project_summary)

        if not args.generate_trace_links:
            state.trace_predictions = self._create_traces_from_generation_predictions(id_to_related_children)
            return

        logger.info(f"Predicting links between {args.target_type} and {args.source_layer_id}\n")

        if args.perform_clustering:
            trace_predictions = self._trace_artifacts_in_cluster_to_generated_parents(args, state, new_artifact_df)
        else:
            trace_predictions = self._run_tracing_job_on_all_artifacts(args, state)
        trace_predictions = self._weight_scores_with_related_children_predictions(trace_predictions, id_to_related_children)
        state.trace_predictions = trace_predictions

    def _run_tracing_job_on_all_artifacts(self, args: HGenArgs, state: HGenState) -> List[EnumDict]:
        """
        Runs a ranking job for all candidate links between the children and generated parents
        :param args: The arguments to HGen
        :param state: The current state of HGen
        :return: The trace predictions for all candidates (that were not filtered)
        """
        tracing_job = RankingJob(dataset=state.all_artifacts_dataset,
                                 layer_ids=(args.target_type, args.source_layer_id),  # parent, child
                                 export_dir=self._get_ranking_dir(state.export_dir),
                                 load_dir=self._get_ranking_dir(args.load_dir),
                                 ranking_pipeline=SupportedRankingPipelines.EMBEDDING,
                                 link_threshold=0.3)  # Only filter out really low links so that related artifacts can factor in
        result = tracing_job.run()
        if result.status != Status.SUCCESS:
            raise Exception(f"Trace link generation failed: {result.body}")
        trace_predictions: List[EnumDict] = result.body.prediction_entries
        return trace_predictions

    def _trace_artifacts_in_cluster_to_generated_parents(self, args: HGenArgs, state: HGenState,
                                                         generated_parents_df: ArtifactDataFrame,
                                                         max_threads: int = 10) -> List[EnumDict]:
        """
        Generates links between the artifacts in a cluster and the parent artifact generated from the cluster artifacts
        :param args: The arguments to HGen
        :param state: The current state of HGen
        :param generated_parents_df: Contains the parent content that aws generated generated
        :param max_threads: The maximum number of threads to run
        :return: The trace predictions for the clusters
        """

        def generate_for_cluster(cluster_id: str) -> List[EnumDict]:
            """
            Runs the generation for a given cluster id
            :param cluster_id: The id of the cluster to generate links for
            :return: The list of link predictions for that cluster
            """
            generations = state.cluster2generation.get(cluster_id)
            parent_ids = [generation2id[generation] for generation in generations]
            children_ids = [a[ArtifactKeys.ID] for a in state.id_to_cluster_artifacts[cluster_id]]
            pipeline_args = RankingArgs(run_name=f"Cluster{cluster_id}: " + RankingJob.get_run_name(args.source_type, children_ids,
                                                                                                    args.target_type, parent_ids),
                                        dataset=state.all_artifacts_dataset,
                                        parent_ids=parent_ids,
                                        children_ids=children_ids,
                                        export_dir=os.path.join(self._get_ranking_dir(state.export_dir), str(cluster_id)),
                                        types_to_trace=(args.source_type, args.target_type),
                                        selection_method=None)
            pipeline = EmbeddingRankingPipeline(pipeline_args, embedding_manager=state.embedding_manager)
            pipeline.run()
            return pipeline.state.selected_entries

        cluster_ids = list(state.cluster_dataset.artifact_df.index)
        generation2id = {content: a_id for a_id, content in generated_parents_df.to_map().items()}
        pipeline_args = RankingArgs(dataset=state.all_artifacts_dataset, parent_ids=[], children_ids=[],
                                    export_dir=self._get_ranking_dir(state.export_dir), types_to_trace=('', ''))
        state.all_artifacts_dataset.project_summary = EmbeddingRankingPipeline(pipeline_args).run_summarizations()
        trace_predictions = ThreadUtil.multi_thread_process(
            title="Generating trace links between artifacts in cluster and generated parents",
            iterable=cluster_ids, thread_work=generate_for_cluster, n_threads=min(len(cluster_ids), max_threads),
            collect_results=True)
        return trace_predictions

    @staticmethod
    def _create_traces_from_generation_predictions(id_to_related_children) -> List[EnumDict]:
        """
        Creates traces using the related sources from the previous step
        :param id_to_related_children: Dictionary mapping new artifact id to a list of related children
        :return: List of traces created from the related sources from the previous step
        """
        trace_predictions = []
        for p_id, related_children in id_to_related_children.items():
            for artifact in related_children:
                trace_predictions.append(RankingUtil.create_entry(parent=p_id, child=artifact, score=RELATED_CHILDREN_SCORE))
        return trace_predictions

    @staticmethod
    def _weight_scores_with_related_children_predictions(trace_predictions: List[EnumDict],
                                                         id_to_related_children: Dict[str, Set]) -> List[EnumDict]:
        """
        Adjusts the score to reflect that an artifact was predicted to be related (through clustering or artifact gen step)
        :param trace_predictions: The list of trace predictions from ranking job
        :param id_to_related_children: A dictionary mapping the generated content id to the list of predicted relationships
        :return: The adjusted trace predictions
        """
        for trace in trace_predictions:
            child = trace[TraceKeys.child_label()]
            parent = trace[TraceKeys.parent_label()]
            if parent in id_to_related_children and child in id_to_related_children[parent]:
                alpha = WEIGHT_OF_PRED_RELATED_CHILDREN
                trace[TraceKeys.SCORE] = MathUtil.calculate_weighted_score(RELATED_CHILDREN_SCORE, trace[TraceKeys.SCORE], alpha)
        return SelectByThreshold.select(trace_predictions, DEFAULT_LINK_THRESHOLD)

    @staticmethod
    def _get_ranking_dir(directory: str) -> str:
        """
        Get the directory for ranking job
        :param directory: The main directory used by hgen
        :return: The full path
        """
        return os.path.join(directory, "ranking") if directory else EMPTY_STRING
