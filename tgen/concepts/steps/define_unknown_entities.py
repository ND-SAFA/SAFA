from typing import List, Dict, Tuple

from langchain.text_splitter import NLTKTextSplitter
from pypdf import PdfReader

from tgen.common.constants.deliminator_constants import NEW_LINE, EMPTY_STRING
from tgen.common.objects.artifact import Artifact
from tgen.common.util.file_util import FileUtil
from tgen.common.util.llm_response_util import LLMResponseUtil
from tgen.concepts.concept_args import ConceptArgs
from tgen.concepts.concept_state import ConceptState
from tgen.concepts.types.undefined_concept import UndefinedConcept
from tgen.core.trainers.llm_trainer import LLMTrainer
from tgen.core.trainers.llm_trainer_state import LLMTrainerState
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.data.tdatasets.dataset_role import DatasetRole
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager
from tgen.pipeline.abstract_pipeline_step import AbstractPipelineStep
from tgen.prompts.artifact_prompt import ArtifactPrompt
from tgen.prompts.context_prompt import ContextPrompt
from tgen.prompts.prompt_args import PromptArgs
from tgen.prompts.prompt_builder import PromptBuilder
from tgen.prompts.response_managers.xml_response_manager import XMLResponseManager


class DefineUnknownEntitiesStep(AbstractPipelineStep):
    def _run(self, args: ConceptArgs, state: ConceptState) -> None:
        """
        Gives the model a chance to define any unknown concepts using provided documentation.
        :param args: Contains the optional path to the context document.
        :param state: Used to retrieve intermediate and store final result.
        :return: None
        """
        if not args.context_doc_path:
            return

        original_content = self._read_context_document(args.context_doc_path)

        undefined_entities = state.response["undefined_entities"]
        context, undefined_entity_artifacts = self._identify_context_for_entities(original_content, args.artifacts,
                                                                                  undefined_entities)

        entity_id_to_definition = self._predict_entity_definitions(context, undefined_entity_artifacts, args.llm_manager)
        for entity in undefined_entities:
            entity["concept_definition"] = entity_id_to_definition.get(entity["concept_id"], EMPTY_STRING)

    @staticmethod
    def _predict_entity_definitions(artifact2context: Dict[str, List[Artifact]], undefined_entities: List[Artifact],
                                    llm_manager: AbstractLLMManager) -> Dict[str, List]:
        """
        Predicts the definition of an entity based on the domain specific context.
        :param artifact2context: Dictionary mapping entity id to a list of related artifacts or document content.
        :param undefined_entities: List of entities to get the definition of.
        :param llm_manager: Manages the llm used for creating the predictions.
        :return: Maps entity id to its definition response.
        """
        context_prompt = ContextPrompt(artifact2context, prompt_args=PromptArgs(system_prompt=True))
        instruction_prompt = ArtifactPrompt(prompt_args=PromptArgs(title="Tasks"),
                                            prompt_start="Based on the provided information, summarize what the following "
                                                         "term means in the context of this project. ",
                                            include_id=False, response_manager=XMLResponseManager(response_tag="definition"))
        prompt_builder = PromptBuilder([context_prompt, instruction_prompt])
        dataset = PromptDataset(artifact_df=ArtifactDataFrame(undefined_entities))
        dataset_manager = TrainerDatasetManager.create_from_datasets({DatasetRole.EVAL: dataset})
        trainer_state = LLMTrainerState(trainer_dataset_manager=dataset_manager, prompt_builders=[prompt_builder],
                                        llm_manager=llm_manager)
        llm_trainer = LLMTrainer(trainer_state)
        res = llm_trainer.perform_prediction()
        predictions = LLMResponseUtil.extract_predictions_from_response(res.predictions, instruction_prompt.args.prompt_id,
                                                                        instruction_prompt.get_all_response_tags()[0],
                                                                        return_first=True)
        entity_id_to_definition = {e_id: pred for e_id, pred in zip(dataset.artifact_df.index, predictions)}
        return entity_id_to_definition

    def _identify_context_for_entities(self, context_doc_content: str, artifacts: List[Artifact],
                                       undefined_entities: List[UndefinedConcept]) -> Tuple[Dict[str, List[Artifact]], List[Artifact]]:
        """
        Identifies relevant context for each undefined entity.
        :param context_doc_content: The content from the context document.
        :param artifacts: Contains all project artifacts.
        :param undefined_entities: List of undefined concepts.
        :return: Mapping of entity id to related artifacts for context and a list of corresponding undefined entity as artifacts.
        """
        id2artifacts = {a["id"]: a for a in artifacts}
        chunks = NLTKTextSplitter().split_text(context_doc_content)
        context, undefined_entity_artifacts = {}, []
        for entity in undefined_entities:
            entity_id = entity["concept_id"]
            found_chunks = self._find_chunks_related_to_entity(entity_id, chunks)

            related_artifacts = [id2artifacts[a_id] for a_id in entity["artifact_ids"]]
            entity_context = related_artifacts + found_chunks
            if len(entity_context) > 1:
                context[entity_id] = entity_context
                undefined_entity_artifacts.append(Artifact(id=entity_id, content=entity_id, layer_id="undefined"))
        return context, undefined_entity_artifacts

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
            raise Exception(f"Unsupported file format {FileUtil.get_file_ext(args.context_doc_path)}")
        return original_content
