from tgen.pipeline.abstract_pipeline_step import AbstractPipelineStep
from tgen.summarizer.artifact.artifacts_summarizer import ArtifactsSummarizer
from tgen.summarizer.summarizer_args import SummarizerArgs
from tgen.summarizer.summarizer_state import SummarizerState
from tgen.summarizer.summarizer_util import SummarizerUtil


class StepSummarizeArtifacts(AbstractPipelineStep[SummarizerArgs, SummarizerState]):

    def _run(self, args: SummarizerArgs, state: SummarizerState) -> None:
        """
        Summarizes the artifacts for initial run.
        :param args: Arguments to summarizer pipeline.
        :param state: Current state of the summarizer pipeline.
        :return: None
        """
        params = SummarizerUtil.get_params_for_artifact_summarizer(args)
        re_summarize = not SummarizerUtil.needs_project_summary(state.dataset.project_summary, args)
        project_summary = state.dataset.project_summary if re_summarize else None
        summarizer = ArtifactsSummarizer(**params, project_summary=project_summary)
        state.dataset.artifact_df.summarize_content(summarizer, re_summarize=re_summarize)
