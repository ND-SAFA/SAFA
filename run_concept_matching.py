import os.path
from typing import Literal, Type, Union

from gen_common.data.creators.prompt_dataset_creator import PromptDatasetCreator
from gen_common.data.creators.trace_dataset_creator import TraceDatasetCreator
from gen_common.data.readers.structured_project_reader import StructuredProjectReader

from gen.health.concepts.concept_args import ConceptArgs
from gen.health.concepts.extraction.concept_extraction_pipeline import ConceptExtractionPipeline
from gen.health.concepts.extraction.concept_extraction_state import ConceptExtractionState
from gen.health.concepts.matching.concept_matching_pipeline import ConceptMatchingPipeline
from gen.health.concepts.matching.concept_matching_state import ConceptMatchingState

SupportedPipelineNames = Literal["concept-matching", "concept-extraction"]
SupportedPipelines = Union[ConceptMatchingPipeline, ConceptExtractionPipeline]


def pipeline_factory(pipeline_name: SupportedPipelineNames) -> Type[SupportedPipelines]:
    if pipeline_name == "concept-matching":
        return ConceptMatchingPipeline
    elif pipeline_name == "concept-extraction":
        return ConceptExtractionPipeline
    else:
        raise Exception(f"Unknown pipeline name: {pipeline_name}")


def print_pipeline_results(state: Union[ConceptMatchingState, ConceptExtractionState]):
    if isinstance(state, ConceptMatchingState):
        print("Direct Matches")
        for d in state.direct_matches:
            print(d)
        print("Predicted Matches:")
        for p in state.predicted_matches:
            print(p)

    elif isinstance(state, ConceptExtractionState):
        print("Undefined Concepts")
        for c in state.undefined_concepts:
            print(c)

    else:
        raise Exception(f"Unknown state type: {type(state)}")


def main():
    project_path = os.path.expanduser("~/desktop/safa/datasets/goes-r/2.0")
    prompt_dataset_creator = PromptDatasetCreator(
        trace_dataset_creator=TraceDatasetCreator(
            project_reader=StructuredProjectReader(project_path=project_path),
            should_generate_negative_links=False
        )
    )
    args = ConceptArgs(
        dataset_creator=prompt_dataset_creator,
        query_ids=[
            "FPS/GSFPS-1693",
            "FPS/GSFPS-2237",
            "FPS/GSFPS-2435",
            "FPS/GSFPS-2541",
            "FPS/GSFPS-2849"
        ]
    )
    pipeline = pipeline_factory("concept-matching")(args)
    pipeline.run()
    print_pipeline_results(pipeline.state)


if __name__ == '__main__':
    main()
