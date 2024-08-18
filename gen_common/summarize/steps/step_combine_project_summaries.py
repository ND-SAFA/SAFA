from gen_common.pipeline.abstract_pipeline_step import AbstractPipelineStep
from gen_common.summarize.project.project_summarizer import ProjectSummarizer
from gen_common.summarize.summarizer_args import SummarizerArgs
from gen_common.summarize.summarizer_state import SummarizerState


class StepCombineProjectSummaries(AbstractPipelineStep[SummarizerArgs, SummarizerState]):

    def _run(self, args: SummarizerArgs, state: SummarizerState) -> None:
        """
        Combines all project summaries into a single one.
        :param args: Arguments to summarizer pipeline.
        :param state: Current state of the summarizer pipeline.
        :return: None
        """
        if len(state.project_summaries) == 1:
            state.final_project_summary = state.project_summaries[0]
        else:
            state.final_project_summary = ProjectSummarizer(args, project_summary_versions=state.project_summaries,
                                                            summarizer_id="Combined summaries").summarize()
