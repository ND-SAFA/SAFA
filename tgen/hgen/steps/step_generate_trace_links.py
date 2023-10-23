import os
from typing import Dict, Set
from typing import List

from tgen.common.constants.deliminator_constants import EMPTY_STRING
from tgen.common.constants.hgen_constants import WEIGHT_OF_PRED_RELATED_CHILDREN, DEFAULT_LINK_THRESHOLD, RELATED_CHILDREN_SCORE
from tgen.common.util.enum_util import EnumDict
from tgen.common.util.logging.logger_manager import logger
from tgen.common.util.math_util import MathUtil
from tgen.common.util.status import Status
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.keys.structure_keys import TraceKeys
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.hgen.hgen_args import HGenArgs
from tgen.hgen.hgen_state import HGenState
from tgen.hgen.hgen_util import HGenUtil
from tgen.jobs.tracing_jobs.ranking_job import RankingJob
from tgen.state.pipeline.abstract_pipeline import AbstractPipelineStep
from tgen.tracing.ranking.common.ranking_util import RankingUtil
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
        tracing_job = RankingJob(dataset=state.all_artifacts_dataset,
                                 layer_ids=(args.target_type, args.source_layer_id),  # parent, child
                                 export_dir=self._get_ranking_dir(state.export_dir),
                                 load_dir=self._get_ranking_dir(args.load_dir),
                                 link_threshold=0.3,  # Only filter out really low links so that related artifacts can factor in
                                 ranking_pipeline=SupportedRankingPipelines.EMBEDDING)
        result = tracing_job.run()
        if result.status != Status.SUCCESS:
            raise Exception(f"Trace link generation failed: {result.body}")

        trace_predictions: List[EnumDict] = result.body.prediction_entries
        self._weight_scores_with_related_children_predictions(trace_predictions, id_to_related_children)
        state.trace_predictions = trace_predictions

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
                                                         id_to_related_children: Dict[str, Set]) -> None:
        """
        Adjusts the score to reflect that an artifact was predicted to be related (through clustering or artifact gen step)
        :param trace_predictions: The list of trace predictions from ranking job
        :param id_to_related_children: A dictionary mapping the generated content id to the list of predicted relationships
        :return: None
        """
        for trace in trace_predictions:
            child = trace[TraceKeys.child_label()]
            parent = trace[TraceKeys.parent_label()]
            if parent in id_to_related_children and child in id_to_related_children[parent]:
                alpha = WEIGHT_OF_PRED_RELATED_CHILDREN
                trace[TraceKeys.SCORE] = MathUtil.calculate_weighted_score(RELATED_CHILDREN_SCORE, trace[TraceKeys.SCORE], alpha)
        SelectByThreshold.select(trace_predictions, DEFAULT_LINK_THRESHOLD)

    @staticmethod
    def _get_ranking_dir(directory: str) -> str:
        """
        Get the directory for ranking job
        :param directory: The main directory used by hgen
        :return: The full path
        """
        return os.path.join(directory, "ranking") if directory else EMPTY_STRING
