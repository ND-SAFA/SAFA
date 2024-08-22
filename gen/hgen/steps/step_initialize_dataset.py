from typing import List

from gen_common.constants.symbol_constants import EMPTY_STRING, NEW_LINE
from gen_common.data.objects.artifact import Artifact
from gen_common.data.tdatasets.prompt_dataset import PromptDataset
from gen_common.pipeline.abstract_pipeline_step import AbstractPipelineStep
from gen_common.pipeline.util import PipelineUtil
from gen_common.summarize.summary import SummarySectionKeys

from gen.hgen.hgen_args import HGenArgs
from gen.hgen.hgen_state import HGenState


class InitializeDatasetStep(AbstractPipelineStep[HGenArgs, HGenState]):
    HGEN_SECTION_TITLE = "Hgen"

    def _run(self, args: HGenArgs, state: HGenState) -> None:
        """
        Gets the original source datasets used for the generation
        :param args: The arguments and current state of HGEN.
        :param state: The state of HGEN.
        :return: The original dataset and a dataset with only the source layer
        """
        original_dataset_complete = args.dataset
        args.dataset.artifact_df.drop_large_files()
        PipelineUtil.save_dataset_checkpoint(original_dataset_complete, state.export_dir, filename="initial_dataset_with_sources")

        seed_artifacts = self.get_seed_artifacts(args, state)
        original_dataset_complete.artifact_df.add_artifacts(seed_artifacts)

        artifact_types = set(original_dataset_complete.artifact_df.get_artifact_types())
        missing_types = [s for s in args.source_layer_ids if s not in artifact_types]
        assert len(missing_types) == 0, f"Unknown artifact types: {missing_types}. Should be one of {artifact_types}."

        source_artifact_df = original_dataset_complete.artifact_df.get_artifacts_by_type(args.source_layer_ids)
        source_layer_only_dataset = PromptDataset(artifact_df=source_artifact_df)

        state.source_dataset = source_layer_only_dataset
        state.original_dataset = original_dataset_complete

    def get_seed_artifacts(self, args: HGenArgs, state: HGenState) -> List[Artifact]:
        """
        Creates artifacts from seeds defined by HGEN configuration.
        :param args: Args defining where to find the seeds.
        :param state: State containing seed contents.
        :return: The seeds as artifacts.
        """
        if args.seed_project_summary_section:
            section_id = args.seed_project_summary_section
            assert section_id in args.dataset.project_summary, f"{section_id} not in {list(args.dataset.project_summary.keys())}"
            seed_contents = args.dataset.project_summary[section_id][SummarySectionKeys.CHUNKS]
            seed_artifact_type = section_id
        elif args.seed_layer_id:
            # Artifacts already present in data frame.
            return []
        else:
            return []

        seed_artifacts = [self.create_cluster_artifact(s, seed_artifact_type) for s in seed_contents]
        return seed_artifacts

    @staticmethod
    def create_cluster_artifact(seed_text: str, seed_layer_id: str) -> Artifact:
        """
        Creates artifact for cluster with given content and layer id.
        :param seed_text: The content of the seed.
        :param seed_layer_id: The layer to given the seed artifact.
        :return: Artifact.
        """
        if NEW_LINE in seed_text:
            curr_id = seed_text.splitlines()
            artifact_id = curr_id[0]
            artifact_content = NEW_LINE.join(curr_id[1:])
        else:
            artifact_id = seed_text
            artifact_content = seed_text
        new_artifact = Artifact(id=artifact_id, content=artifact_content, layer_id=seed_layer_id, summary=EMPTY_STRING)
        return new_artifact
