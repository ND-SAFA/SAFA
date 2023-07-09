import os
import uuid

from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.hgen.hgen_args import HGenArgs
from tgen.hgen.steps.step_create_dataset import create_hgen_dataset
from tgen.hgen.steps.step_generate_artifact_content import generate_artifact_content
from tgen.hgen.steps.step_initialize_dataset import initialize_datasets
from tgen.hgen.steps.step_refine_output import refine_artifact_content
from tgen.util.base_object import BaseObject


class HierarchyGenerator(BaseObject):
    """
    Responsible for generating higher-level artifacts from low-level artifacts
    """

    def __init__(self, args: HGenArgs):
        """
        Initializes the generator with necessary trainer information
        :param args: The arguments required for the hierarchy generation
        """
        self.args = args

    def run(self) -> TraceDataset:
        """
        Runs the hierarchy generator to create a new trace dataset containing generated higher-level artifacts
        :return: Path to exported dataset of generated artifacts
        """
        export_path = os.path.join(self.args.export_dir, str(uuid.uuid4())) if self.args.export_dir else None
        self.args.state.export_path = export_path

        pipeline = [initialize_datasets,
                    generate_artifact_content,
                    refine_artifact_content,
                    create_hgen_dataset]
        for step in pipeline:
            step(hgen_args=self.args)

        dataset = self.args.state.dataset
        assert dataset is not None, f"Final dataset is not set."
        return dataset
