from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.hgen.common.hgen_dataset_exporter import HGenDatasetExporter
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
        trace_dataset = HGenDatasetExporter.export(args, state)
        dataset = PromptDataset(trace_dataset=trace_dataset, project_summary=args.dataset.project_summary)
        state.final_dataset = dataset
