from copy import deepcopy

from langchain.text_splitter import NLTKTextSplitter
from pypdf import PdfReader

from tgen.common.constants.deliminator_constants import NEW_LINE, EMPTY_STRING
from tgen.common.objects.artifact import Artifact
from tgen.common.util.file_util import FileUtil
from tgen.common.util.str_util import StrUtil
from tgen.concepts.concept_args import ConceptArgs
from tgen.concepts.concept_state import ConceptState
from tgen.core.trainers.llm_trainer import LLMTrainer
from tgen.core.trainers.llm_trainer_state import LLMTrainerState
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.data.tdatasets.dataset_role import DatasetRole
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.pipeline.abstract_pipeline_step import AbstractPipelineStep
from tgen.prompts.artifact_prompt import ArtifactPrompt
from tgen.prompts.context_prompt import ContextPrompt
from tgen.prompts.prompt_args import PromptArgs
from tgen.prompts.prompt_builder import PromptBuilder


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

        if args.context_doc_path.endswith(FileUtil.TEXT_EXT):
            original_content = FileUtil.read_file(args.context_doc_path)
        elif args.context_doc_path.endswith(FileUtil.PDF_EXT):
            expanded_path = FileUtil.expand_paths(args.context_doc_path)
            reader = PdfReader(expanded_path)
            pages = [p.extract_text() for p in reader.pages]
            original_content = NEW_LINE.join(pages)

        else:
            raise Exception(f"Unsupported file format {FileUtil.get_file_ext(args.context_doc_path)}")

        text_splitter = NLTKTextSplitter()
        chunks = text_splitter.split_text(original_content)

        context = {}
        undefined_entities = []
        for entity in state.response["undefined_entities"]:
            entity_id = entity["concept_id"]
            processed_entity_name = StrUtil.remove_stop_words(entity_id)
            candidates = deepcopy(chunks)
            for term in [entity_id] + processed_entity_name.split():
                if len(term) < 2:
                    continue
                found = [chunk for chunk in candidates if f"{term}" in chunk]
                if len(found) < 1:
                    found = [chunk for chunk in candidates if f"{term.lower()}" in chunk]
                if found:
                    if len(found) < 5 or term == entity_id:
                        break
                    candidates = found
                elif not found and term != entity_id:
                    break
            if len(found) > 10:
                check = 1
            artifacts = args.dataset.artifact_df.filter_by_index(entity["artifact_ids"]).to_artifacts()
            found_chunks = [Artifact(id=f"{i}", content=chunk) for i, chunk in enumerate(found)]
            if len(artifacts) + len(found_chunks) > 1:
                context[entity_id] = artifacts + found_chunks
                undefined_entities.append(Artifact(id=entity_id, content=entity_id, layer_id="undefined"))

        context_prompt = ContextPrompt(context, prompt_args=PromptArgs(system_prompt=True))
        instruction_prompt = ArtifactPrompt(prompt_args=PromptArgs(title="Tasks"),
                                            prompt_start="Based on the provided information, summarize what the following "
                                                         "term means in the context of this project. ",
                                            include_id=False)
        prompt_builder = PromptBuilder([context_prompt, instruction_prompt])
        dataset = PromptDataset(artifact_df=ArtifactDataFrame(undefined_entities))
        dataset_manager = TrainerDatasetManager.create_from_datasets({DatasetRole.EVAL: dataset})
        trainer_state = LLMTrainerState(trainer_dataset_manager=dataset_manager, prompt_builders=[prompt_builder],
                                        llm_manager=args.llm_manager)
        llm_trainer = LLMTrainer(trainer_state)
        res = llm_trainer.perform_prediction()
        entity_id_to_definition = {e_id: pred for e_id, pred in zip(dataset.artifact_df.index, res.predictions)}
        for entity in state.response["undefined_entities"]:
            entity["concept_definition"] = entity_id_to_definition.get(entity["concept_id"], EMPTY_STRING)
