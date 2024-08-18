from gen_common.data.keys.structure_keys import TraceKeys
from gen_common.data.tdatasets.prompt_dataset import PromptDataset
from gen_common.data.tdatasets.trace_dataset import TraceDataset
from gen_common.infra.t_logging.logger_manager import logger
from gen_common.pipeline.abstract_pipeline_step import AbstractPipelineStep

from gen.hgen.common.hgen_dataset_exporter import HGenDatasetBuilder
from gen.hgen.hgen_args import HGenArgs
from gen.hgen.hgen_state import HGenState


class CreateHGenDatasetStep(AbstractPipelineStep[HGenArgs, HGenState]):

    def _run(self, args: HGenArgs, state: HGenState) -> None:
        """
        Creates a dataset containing original artifacts, generated upper level artifacts, and trace links between them.
        :param state: The current state of hgen at this point in time
        :param args: The arguments and current state of HGEN.
        :return: None
        """
        trace_dataset = HGenDatasetBuilder.build(args, state)
        # self._remove_targets_without_children(args, state, trace_dataset)
        dataset = PromptDataset(trace_dataset=trace_dataset, project_summary=args.dataset.project_summary)
        state.final_dataset = dataset

    @staticmethod
    def _remove_targets_without_children(args: HGenArgs, state: HGenState, trace_dataset: TraceDataset) -> None:
        """
        Removes any target artifacts that don't have any children linked to them.
        :param state: The current state of hgen at this point in time
        :param args: The arguments and current state of HGEN.
        :param trace_dataset: The trace dataset created by HGEN.
        :return: None.
        """
        all_target_artifact_ids = {a_id for a_id in state.new_artifact_dataset.artifact_df.index if a_id in trace_dataset.artifact_df}
        targets_without_children = trace_dataset.trace_df.find_orphans(
            trace_dataset.trace_df.get_links(true_link_threshold=args.link_selection_threshold),
            all_artifact_ids=all_target_artifact_ids,
            artifact_role=TraceKeys.parent_label())
        if targets_without_children:
            logger.warning(f"REMOVING {len(targets_without_children)} {args.target_type.upper()} BECAUSE THEY HAD NO CHILDREN. ")
            trace_dataset.artifact_df.remove_rows(targets_without_children)
