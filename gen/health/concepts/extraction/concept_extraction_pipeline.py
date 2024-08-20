from typing import Type

from gen_common.pipeline.abstract_pipeline import AbstractPipeline
from gen_common.pipeline.state import State

from gen.health.concepts.concept_args import ConceptArgs
from gen.health.concepts.extraction.state import ConceptExtractionState
from gen.health.concepts.extraction.steps.define_undefined_concepts import DefineUndefinedConceptsStep
from gen.health.concepts.extraction.steps.extract_undefined_concepts_step import ExtractUndefinedConceptsStep


class ConceptExtractionPipeline(AbstractPipeline):
    steps = [
        ExtractUndefinedConceptsStep,
        DefineUndefinedConceptsStep
    ]

    def __init__(self, args: ConceptArgs):
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
