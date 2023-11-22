from copy import deepcopy

from tgen.pipeline.abstract_pipeline_step import AbstractPipelineStep
from tgen.summarizer.summarizer_args import SummarizerArgs
from tgen.summarizer.summarizer_state import SummarizerState


class StepCreateSummarizedDataset(AbstractPipelineStep[SummarizerArgs, SummarizerState]):

    def _run(self, args: SummarizerArgs, state: SummarizerState) -> None:
        """
        Creates a new summarized version of the original dataset.
        :param args: Arguments to summarizer pipeline.
        :param state: Current state of the summarizer pipeline.
        :return: None
        """
        summarized_dataset = deepcopy(state.dataset)
        artifact_df = state.re_summarized_artifacts_dataset.artifact_df if state.re_summarized_artifacts_dataset \
            else state.dataset.artifact_df
        summarized_dataset.update_artifact_df(artifact_df)
        summarized_dataset.project_summary = state.final_project_summary
        state.summarized_dataset = summarized_dataset
