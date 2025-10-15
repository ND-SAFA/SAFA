from gen.hgen.common.content_refiner import ContentRefiner
from gen.hgen.common.duplicate_detector import DuplicateType
from gen.hgen.common.hgen_util import HGenUtil
from gen.hgen.hgen_args import HGenArgs
from gen.hgen.hgen_state import HGenState
from gen_common.pipeline.abstract_pipeline_step import AbstractPipelineStep


class RefineGenerationsStep(AbstractPipelineStep[HGenArgs, HGenState]):

    def _run(self, args: HGenArgs, state: HGenState) -> None:
        """
        Re-runs hgen on cluster of duplicate artifacts to condense them.
        :param args: The arguments to Hierarchy Generator.
        :param state: The current state for the generator.
        :return: None.
        """
        if not args.run_refinement or not args.perform_clustering:
            return

        duplicate_types = [DuplicateType.ALL]

        for duplicate_type in duplicate_types:

            generated_artifacts_df, _ = HGenUtil.create_artifact_df_from_generated_artifacts(args,
                                                                                             state.get_generations2sources(),
                                                                                             args.target_type,
                                                                                             generate_names=True,
                                                                                             generation_id=duplicate_type.name.lower())
            refiner = ContentRefiner(args, state, duplicate_type)
            refined_state_vars = refiner.refine(generated_artifacts_df)
            if refined_state_vars:
                refined_generation2sources, refined_cluster2generations, refined_cluster2artifacts = refined_state_vars
                state.refined_generations2sources[duplicate_type.value] = refined_generation2sources
                state.refined_cluster2generation[duplicate_type.value] = refined_cluster2generations
                state.refined_cluster2artifacts[duplicate_type.value] = refined_cluster2artifacts
