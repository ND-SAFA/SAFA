from typing import Type

from gen_common.pipeline.abstract_pipeline import AbstractPipeline
from gen_common.pipeline.state import State

from gen.health.concepts.extraction.concept_extraction_state import ConceptExtractionState
from gen.health.concepts.extraction.steps.condense_undefined_concepts import CondenseUndefinedConceptsStep
from gen.health.concepts.extraction.steps.define_undefined_concepts import DefineUndefinedConceptsStep
from gen.health.concepts.extraction.steps.extract_undefined_concepts_step import ExtractUndefinedConceptsStep
from gen.health.health_args import HealthArgs


class ConceptExtractionPipeline(AbstractPipeline):
    steps = [
        ExtractUndefinedConceptsStep,
        CondenseUndefinedConceptsStep,
        DefineUndefinedConceptsStep
    ]

    def __init__(self, args: HealthArgs):
        """
        Creates new pipeline with concept configuration.
        :param args: Args containing dataset, query ids, and concept type.
        """
        super().__init__(args, steps=self.steps, skip_summarization=True)

    def state_class(self) -> Type[State]:
        """
        :return: Returns pipeline state class for concept extraction pipeline.
        """
        return ConceptExtractionState
