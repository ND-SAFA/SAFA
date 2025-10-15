from typing import Dict, List

from gen_common.constants.symbol_constants import EMPTY_STRING, NEW_LINE
from gen_common.data.keys.prompt_keys import PromptKeys
from gen_common.data.keys.structure_keys import ArtifactKeys
from gen_common.data.objects.artifact import Artifact
from gen_common.infra.t_logging.logger_manager import logger
from gen_common.llm.prompts.context_prompt import ContextPrompt
from gen_common.llm.prompts.llm_prompt_build_args import LLMPromptBuildArgs
from gen_common.llm.prompts.prompt import Prompt
from gen_common.llm.prompts.prompt_args import PromptArgs
from gen_common.llm.prompts.prompt_builder import PromptBuilder
from gen_common.llm.response_managers.json_response_manager import JSONResponseManager
from gen_common.pipeline.abstract_pipeline_step import AbstractPipelineStep
from gen_common.util.file_util import FileUtil
from gen_common.util.llm_util import LLMUtil, PromptGeneratorReturnType, PromptGeneratorType
from langchain.text_splitter import NLTKTextSplitter
from pydantic.v1 import BaseModel, Field
from pypdf import PdfReader

from gen.health.concepts.extraction.concept_extraction_state import ConceptExtractionState
from gen.health.concepts.extraction.undefined_concept import UndefinedConcept
from gen.health.health_args import HealthArgs


class _DefineUndefinedConceptFormat(BaseModel):
    """
    Defines the definition for a term used in a project but has not yet been defined.
    """
    definition: str = Field(description="Definition for undefined term used in project.")


DEFINE_UNDEFINED_CONCEPT_SYSTEM_PROMPT = (
    "Based on the provided information, summarize what the following term means in the context of this project. "
)


class DefineUndefinedConceptsStep(AbstractPipelineStep):
    def _run(self, args: HealthArgs, state: ConceptExtractionState) -> None:
        """
        Gives the model a chance to define any unknown concepts using provided documentation.
        :param args: Contains the optional path to the context document.
        :param state: Used to retrieve intermediate and store final result.
        :return: None
        """
        context_doc_content = self._read_context_document(args.context_doc_path) if args.context_doc_path else None

        if len(state.undefined_concepts) == 0:
            state.undefined_concepts = []
            logger.info("Skipping concept definition generation, no undefined concepts.")
            return

        context = self._identify_context_for_entities(
            args=args,
            undefined_concepts=state.undefined_concepts,
            context_doc_content=context_doc_content
        )

        predictions = LLMUtil.complete_iterable_prompts(
            items=state.undefined_concepts,
            prompt_generator=self._create_prompt_generator(
                format_args=args.llm_manager.prompt_args,
                artifact2context=context
            ),
            llm_manager=args.llm_manager
        )

        for undefined_concept, prediction in predictions:
            definition = prediction.get("definition", [EMPTY_STRING])[0]
            undefined_concept.definition = definition

    @staticmethod
    def _create_prompt_generator(format_args: LLMPromptBuildArgs,
                                 artifact2context: Dict[str, List[Artifact]]) -> PromptGeneratorType:
        """
        Creates a prompt generator for defining undefined concepts.
        :param format_args: LLM provider format arguments.
        :param artifact2context: Mapping of artifact id to list of related artifacts to use in context.
        :return: PromptGenerator callable.
        """

        def generator(undefined_concept: UndefinedConcept) -> PromptGeneratorReturnType:
            """
            Generates prompt for an undefined concept.
            :param undefined_concept: The undefined whose prompt is created for.
            :return: Prompt builder and built prompt for undefined concept.
            """
            builder = PromptBuilder(prompts=[
                ContextPrompt(artifact2context, prompt_args=PromptArgs(system_prompt=False)),
                Prompt(f"# Undefined Concept\n{undefined_concept.concept_id}"),
                Prompt(
                    response_manager=JSONResponseManager.from_langgraph_model(
                        _DefineUndefinedConceptFormat
                    )
                )
            ])
            undefined_concept_artifact = Artifact(id=undefined_concept.concept_id, content=EMPTY_STRING)
            prompt = builder.build(format_args, artifact=undefined_concept_artifact)
            prompt[PromptKeys.SYSTEM] = DEFINE_UNDEFINED_CONCEPT_SYSTEM_PROMPT
            return builder, prompt

        return generator

    def _identify_context_for_entities(self,
                                       args: HealthArgs,
                                       undefined_concepts: List[UndefinedConcept],
                                       context_doc_content: str = None) -> Dict[str, List[Artifact]]:
        """
        Identifies relevant context for each undefined entity.
        :param args: Concept arguments containing artifacts referencing undefined concepts.
        :param undefined_concepts: List of undefined concepts.
        :param context_doc_content: The content from the context document.
        :return: Mapping of entity id to related artifacts for context and a list of corresponding undefined entity as artifacts.
        """
        id2artifacts = {a[ArtifactKeys.ID]: a for a in args.get_query_artifacts()}
        context = {}
        chunks = None

        if context_doc_content:
            chunks = NLTKTextSplitter().split_text(context_doc_content)

        for u_concept in undefined_concepts:
            concept_id = u_concept.concept_id

            related_artifacts = [id2artifacts[a_id] for a_id in u_concept.artifact_ids]
            entity_context = related_artifacts

            if chunks:
                found_chunks = self._find_chunks_related_to_entity(concept_id, chunks)
                entity_context += found_chunks

            context[concept_id] = entity_context

        return context

    def _find_chunks_related_to_entity(self, entity_id: str, chunks: List[str]) -> List[Artifact]:
        """
        Finds all chunks that are related to the entity and returns them as artifacts.
        :param entity_id: The id of the entity to search for.
        :param chunks: List of candidate chunks to search in.
        :return: List of all chunks related to the entity as artifacts.
        """
        candidates = chunks
        found = []

        terms: List[str] = entity_id.split()
        if len(terms) > 1:
            terms = [entity_id] + terms

        for term in terms:
            if len(term) <= 1:  # single letters or numbers tend not to be terribly helpful
                continue
            found = self._find_term_in_document(candidates, term)
            if not found and not term.isupper():  # try lower case of term if not an acronym
                found = self._find_term_in_document(candidates, term.lower())

            end_search = self._should_end_search(found, is_original_id=term == entity_id)

            if end_search:
                break
            elif found:
                candidates = found

        found_chunks = [Artifact(id=str(i), content=chunk) for i, chunk in enumerate(found)]
        return found_chunks

    @staticmethod
    def _find_term_in_document(candidates: List[str], term: str) -> List[str]:
        """
        Identifies each chunk that contains the search term.
        :param candidates: List of document chunks.
        :param term: The term to search for.
        :return: List of chunks that contains the search term.
        """
        found = [chunk for chunk in candidates if f"{term}" in chunk]
        return found

    @staticmethod
    def _should_end_search(found: List[str], is_original_id: bool) -> bool:
        """
        Determines whether the search should continue or not.
        :param found:
        :param is_original_id:
        :return: True if the search should be ended.
        """
        if found:
            if len(found) < 5 or is_original_id:
                # If only a few results or the original id was found, then good to proceed
                return True
        elif not (found or is_original_id):
            # If not found and is not the original ID, then give up (expects all parts to be present in some capacity)
            return True
        return False

    @staticmethod
    def _read_context_document(context_doc_path: str) -> str:
        """
        Reads in the context document.
        :param context_doc_path: The path to the context document.
        :return: The content extracted from the context document.
        """
        if context_doc_path.endswith(FileUtil.TEXT_EXT):
            original_content = FileUtil.read_file(context_doc_path)
        elif context_doc_path.endswith(FileUtil.PDF_EXT):
            expanded_path = FileUtil.expand_paths(context_doc_path)
            reader = PdfReader(expanded_path)
            pages = [p.extract_text() for p in reader.pages]
            original_content = NEW_LINE.join(pages)

        else:
            raise Exception(f"Unsupported file format {FileUtil.get_file_ext(context_doc_path)}")
        return original_content
