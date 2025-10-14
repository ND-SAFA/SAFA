from gen_common.data.dataframes.artifact_dataframe import ArtifactDataFrame
from gen_common.data.keys.structure_keys import ArtifactKeys
from gen_common.data.tdatasets.prompt_dataset import PromptDataset
from gen_common.pipeline.abstract_pipeline_step import AbstractPipelineStep
from gen_common.summarize.artifact.artifacts_summarizer import ArtifactsSummarizer
from gen_common.summarize.summarizer_args import SummarizerArgs
from gen_common.summarize.summarizer_state import SummarizerState
from gen_common.summarize.summarizer_util import SummarizerUtil


class StepResummarizeArtifacts(AbstractPipelineStep[SummarizerArgs, SummarizerState]):

    def _run(self, args: SummarizerArgs, state: SummarizerState) -> None:
        """
        Re-summarizes the artifacts with the project summary.
        :param args: Arguments to summarizer pipeline.
        :param state: Current state of the summarizer pipeline.
        :return: None
        """
        if args.do_resummarize_artifacts and not args.no_project_summary:
            orig_artifact_df = state.dataset.artifact_df
            artifact_df = ArtifactDataFrame({ArtifactKeys.ID: orig_artifact_df.index,
                                             ArtifactKeys.CONTENT: orig_artifact_df[ArtifactKeys.CONTENT],
                                             ArtifactKeys.LAYER_ID: orig_artifact_df[ArtifactKeys.LAYER_ID]})
            params = SummarizerUtil.get_params_for_artifact_summarizer(args)
            summarizer = ArtifactsSummarizer(**params, project_summary=state.final_project_summary, summarizer_id="Second Summary")
            artifact_df.summarize_content(summarizer, re_summarize=True)
            state.re_summarized_artifacts_dataset = PromptDataset(artifact_df=artifact_df)
