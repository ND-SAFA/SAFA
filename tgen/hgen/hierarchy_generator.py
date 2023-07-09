import os
import uuid

from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.hgen.hgen_args import HGenArgs, HGenState
from tgen.hgen.steps.step_create_dataset import CreateHGenDataset
from tgen.hgen.steps.step_generate_artifact_content import GenerateArtifactContent
from tgen.hgen.steps.step_initialize_dataset import InitializeDatasetStep
from tgen.hgen.steps.step_refine_output import RefineArtifactContent
from tgen.ranking.pipeline.ipipeline import iPipeline
from tgen.util.base_object import BaseObject


class HierarchyGenerator(iPipeline[HGenArgs, HGenState], BaseObject):
    """
    Responsible for generating higher-level artifacts from low-level artifacts
    """
    steps = [InitializeDatasetStep,
             GenerateArtifactContent,
             RefineArtifactContent,
             CreateHGenDataset]

    def __init__(self, args: HGenArgs):
        """
        Initializes the generator with necessary trainer information
        :param args: The arguments required for the hierarchy generation
        """
        super().__init__(args, HierarchyGenerator.steps)
        self.args = args

    def init_state(self) -> HGenState:
        """
        Initialized pipeline state.
        :return:
        """
        return HGenState()

    def run(self) -> TraceDataset:
        """
        Runs the hierarchy generator to create a new trace dataset containing generated higher-level artifacts
        :return: Path to exported dataset of generated artifacts
        """
        export_path = os.path.join(self.args.export_dir, str(uuid.uuid4())) if self.args.export_dir else None
        self.state.export_path = export_path

        super().run()

        dataset = self.state.dataset
        assert dataset is not None, f"Final dataset is not set."
        return dataset
