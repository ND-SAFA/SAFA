from tgen.common.logging.logger_manager import logger
from tgen.data.keys.structure_keys import TraceKeys
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.hgen.common.hgen_dataset_exporter import HGenDatasetBuilder
from tgen.hgen.hgen_args import HGenArgs
from tgen.hgen.hgen_state import HGenState
from tgen.pipeline.abstract_pipeline_step import AbstractPipelineStep


class CreateHGenDatasetStep(AbstractPipelineStep[HGenArgs, HGenState]):

    def _run(self, args: HGenArgs, state: HGenState) -> None:
        """
        Creates a dataset containing original artifacts, generated upper level artifacts, and trace links between them.
        :param state: The current state of hgen at this point in time
        :param args: The arguments and current state of HGEN.
        :return: None
        """
        trace_dataset = HGenDatasetBuilder.build(args, state)
        targets_without_children = trace_dataset.trace_df.find_orphans(
            trace_dataset.trace_df.get_links(true_link_threshold=args.link_selection_threshold),
            all_artifact_ids=set(state.new_artifact_dataset.artifact_df.index),
            artifact_role=TraceKeys.parent_label())
        if targets_without_children:
            logger.warning(f"REMOVING {len(targets_without_children)} {args.target_type.upper()} BECAUSE THEY HAD NO CHILDREN. ")
            trace_dataset.artifact_df.remove_rows(targets_without_children)
        dataset = PromptDataset(trace_dataset=trace_dataset, project_summary=args.dataset.project_summary)
        state.final_dataset = dataset
