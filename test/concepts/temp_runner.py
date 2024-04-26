from test.concepts.utils import create_concept_args, create_concept_test_entities
from tgen.concepts.concept_pipeline import ConceptPipeline
from tgen.concepts.concept_state import ConceptState
from tgen.concepts.steps.entity_matching import EntityMatching


def run2():
    args = create_concept_args()
    state = ConceptState()
    state.entity_df = create_concept_test_entities()

    step = EntityMatching()
    step.run(args, state)

    predicted_links = state.predicted_matches


def run():
    args = create_concept_args()

    # Execution
    pipeline = ConceptPipeline(args)
    pipeline.run()
    res = pipeline.state.response
    print("hi")


if __name__ == '__main__':
    run()
