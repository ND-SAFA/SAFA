import os.path

from gen_common.data.creators.prompt_dataset_creator import PromptDatasetCreator
from gen_common.data.creators.trace_dataset_creator import TraceDatasetCreator
from gen_common.data.readers.structured_project_reader import StructuredProjectReader

from gen.health.concepts.concept_args import ConceptArgs
from gen.health.concepts.matching.concept_matching_pipeline import ConceptMatchingPipeline


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
    pipeline = ConceptMatchingPipeline(args)

    pipeline.run()
    print("Response:", pipeline.state)


if __name__ == '__main__':
    main()
