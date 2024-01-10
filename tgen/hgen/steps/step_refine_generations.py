from tgen.hgen.common.content_refiner import ContentRefiner
from tgen.hgen.common.duplicate_detector import DuplicateType
from tgen.hgen.hgen_args import HGenArgs
from tgen.hgen.hgen_state import HGenState
from tgen.pipeline.abstract_pipeline_step import AbstractPipelineStep


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

        for duplicate_type in [DuplicateType.INTRA_CLUSTER, DuplicateType.INTER_CLUSTER]:
            refiner = ContentRefiner(args, state, duplicate_type)
            refined_state_vars = refiner.refine()
            if refined_state_vars:
                refined_generation2sources, refined_cluster2generations, refined_cluster2artifacts = refined_state_vars
                state.refined_generations2sources[duplicate_type.value] = refined_generation2sources
                state.refined_cluster2generation[duplicate_type.value] = refined_cluster2generations
                state.refined_cluster2artifacts[duplicate_type.value] = refined_cluster2artifacts
