from tgen.data.creators.prompt_dataset_creator import PromptDatasetCreator
from tgen.data.readers.artifact_project_reader import ArtifactProjectReader
from tgen.hgen.hgen_args import HGenArgs
from tgen.testres.paths.paths import TEST_HGEN_PATH


def get_test_hgen_args():
    return HGenArgs(source_layer_id="C++ Code",
                    target_type="Test User Story",
                    dataset_creator_for_sources=PromptDatasetCreator(ArtifactProjectReader(project_path=TEST_HGEN_PATH)))
