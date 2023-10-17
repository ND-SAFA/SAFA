import os
from collections.abc import Generator
from copy import deepcopy
from typing import Tuple, List

from tgen.common.constants.dataset_constants import PROJECT_SUMMARY_FILENAME, PROJECT_SUMMARY_STATE_FILENAME
from tgen.common.constants.deliminator_constants import NEW_LINE, EMPTY_STRING
from tgen.common.constants.project_summary_constants import PS_QUESTIONS_HEADER, CUSTOM_TITLE_TAG, MULTI_LINE_ITEMS
from tgen.common.constants.ranking_constants import BODY_ARTIFACT_TITLE, DEFAULT_SUMMARY_TOKENS
from tgen.common.util.base_object import BaseObject
from tgen.common.util.logging.logger_manager import logger
from tgen.common.util.prompt_util import PromptUtil
from tgen.core.trainers.llm_trainer import LLMTrainer
from tgen.core.trainers.llm_trainer_state import LLMTrainerState
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.data.tdatasets.dataset_role import DatasetRole
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager
from tgen.prompts.multi_artifact_prompt import MultiArtifactPrompt
from tgen.prompts.prompt import Prompt
from tgen.prompts.prompt_builder import PromptBuilder
from tgen.prompts.questionnaire_prompt import QuestionnairePrompt
from tgen.prompts.supported_prompts.supported_prompts import SupportedPrompts
from tgen.summarizer.artifact.artifacts_summarizer import ArtifactsSummarizer
from tgen.summarizer.project.supported_project_summary_sections import PROJECT_SUMMARY_MAP
from tgen.summarizer.summarizer_args import SummarizerArgs
from tgen.summarizer.summary import Summary


class ProjectSummarizer(BaseObject):

    def __init__(self, summarizer_args: SummarizerArgs, dataset: PromptDataset, n_tokens: int = DEFAULT_SUMMARY_TOKENS):
        """
        Generates a system specification document for containing all artifacts.
        :param summarizer_args: The args necessary for the summary
        :param n_tokens: The token limit for the LLM
        """
        super().__init__()
        self.artifact_df = dataset.artifact_df
        self.llm_manager: AbstractLLMManager = summarizer_args.llm_manager_for_project_summary
        self.n_tokens = n_tokens
        self.export_dir = summarizer_args.export_dir
        self.save_progress = bool(self.export_dir)
        self.args = summarizer_args
        self.dataset = dataset
        self.project_summary = Summary() if not dataset.project_summary else deepcopy(dataset.project_summary)
        self.all_project_sections = self._get_all_project_sections(self.args)
        self.section_display_order = self._get_section_display_order(self.args.section_display_order, self.all_project_sections)

    def summarize(self) -> Summary:
        """
        Creates the project summary from the project artifacts.
        :return: The summary of the project.
        """
        logger.log_title("Creating project specification.")
        self.artifact_df.summarize_content(ArtifactsSummarizer(self.args, project_summary=self.project_summary))
        if not self.project_summary and os.path.exists(self.get_save_path()):
            logger.info(f"Loading previous project summary from {self.get_save_path()}")
            self.project_summary = Summary.load_from_file(self.get_save_path())

        for section_id, section_prompt in self.get_generation_iterator():
            logger.log_step(f"Creating section: `{section_id}`")
            prompt_builder = self._create_prompt_builder(section_id, section_prompt)
            task_tag = section_prompt.get_response_tags_for_question(-1)
            section_body, section_title = self._generate_section(prompt_builder, task_tag,
                                                                 multi_line_items=section_id in MULTI_LINE_ITEMS)
            if not section_title:
                section_title = section_id

            self.project_summary.add_section(section_id=section_id, section_title=section_title, body=section_body)
            if self.save_progress:
                self.project_summary.save(self.get_save_path())
        self.project_summary.re_order_sections(self.section_display_order, remove_unordered_sections=True)
        return self.project_summary

    def _create_prompt_builder(self, section_id: str, section_prompt: QuestionnairePrompt) -> PromptBuilder:
        """
        Creates a prompt builder for a given section prompt
        :param section_id: The id of the section
        :param section_prompt: The prompt used to create the section
        :return: The prompt builder for creating the section
        """
        assert isinstance(section_prompt, QuestionnairePrompt), f"Expected section {section_id} prompt " \
                                                                f"to be a {QuestionnairePrompt.__class__.__name__}"
        artifacts_prompt = MultiArtifactPrompt(prompt_prefix=BODY_ARTIFACT_TITLE,
                                               build_method=MultiArtifactPrompt.BuildMethod.XML,
                                               include_ids=True)
        prompt_builder = PromptBuilder(prompts=[SupportedPrompts.PROJECT_SUMMARY_CONTEXT.value,
                                                artifacts_prompt,
                                                section_prompt])
        if self.project_summary:
            current_summary = self.project_summary.to_string()
            prompt_builder.add_prompt(Prompt(f"# Current Document\n\n{current_summary}", allow_formatting=False), 1)
        section_prompt.set_instructions(PS_QUESTIONS_HEADER)
        return prompt_builder

    def _generate_section(self, prompt_builder: PromptBuilder, task_tag: str, multi_line_items: bool = False) -> Tuple[str, str]:
        """
        Has the LLM generate the section corresponding using the prompt builder
        :param prompt_builder: Contains prompts necessary for generating section
        :param task_tag: The tag used to retrieve the generations from the parsed response
        :param multi_line_items: If True, expects each item in the body to span multiple lines
        :return: The section body and section title (if one was generated)
        """
        self.llm_manager.llm_args.set_max_tokens(self.n_tokens)
        self.llm_manager.llm_args.temperature = 0
        trainer_dataset_manager = TrainerDatasetManager.create_from_datasets({DatasetRole.EVAL:
                                                                                  PromptDataset(artifact_df=self.artifact_df)})
        trainer = LLMTrainer(LLMTrainerState(llm_manager=self.llm_manager,
                                             prompt_builder=prompt_builder, trainer_dataset_manager=trainer_dataset_manager))
        predictions = trainer.perform_prediction().predictions[0]
        parsed_responses = predictions[prompt_builder.get_prompt(-1).id]
        body_res = parsed_responses[task_tag]
        body_res = [PromptUtil.strip_new_lines_and_extra_space(r, remove_all_new_lines=len(body_res) > 1) for r in body_res]
        task_title = parsed_responses[CUSTOM_TITLE_TAG][0] if parsed_responses.get(CUSTOM_TITLE_TAG) else None
        deliminator = NEW_LINE if not multi_line_items else f"{NEW_LINE}{PromptUtil.as_markdown_header(EMPTY_STRING, level=2)}"
        task_body = body_res[0] if len(body_res) == 1 else deliminator.join(body_res)
        return deliminator + task_body, task_title

    def get_generation_iterator(self) -> Generator:
        """
        Creates iterator for section titles and questions.
        :return: Iterator for each title and prompt.
        """
        for section_id in self.all_project_sections:
            if section_id not in self.project_summary:
                section_prompt = self.get_section_prompt_by_id(section_id)
                yield section_id, section_prompt

    def get_section_prompt_by_id(self, section_id: str) -> QuestionnairePrompt:
        """
        Gets the prompt for creating the section by its title
        :param section_id: The title of the section
        :return: The prompt for creating the section
        """
        section_prompt = PROJECT_SUMMARY_MAP.get(section_id, None)
        if not section_prompt:
            assert section_id in self.args.new_sections, f"Must provide the prompt to use for creating the section: {section_id}"
            section_prompt = self.args.new_sections[section_id]
        else:
            section_prompt = section_prompt.value
        return section_prompt

    def get_summary(self, raise_exception_on_not_found: bool = False) -> str:
        """
        Creates summary in the order of the headers given.
        :param raise_exception_on_not_found: Whether to raise an error if a header if not in the map.
        :return: String representing project summary.
        """
        return self.project_summary.to_string(self.section_display_order, raise_exception_on_not_found)

    def get_save_path(self) -> str:
        """
        Gets the path to save the summary at
        :return: The save path
        """
        if not self.export_dir:
            return EMPTY_STRING
        return os.path.join(self.export_dir, PROJECT_SUMMARY_STATE_FILENAME)

    @staticmethod
    def _get_section_display_order(section_order: List[str], all_project_sections: List[str]) -> List[str]:
        """
        Gets the order in which the sections should appear
        :param args: The arguments for the project summarizer
        :return: The section ids in the order in which the sections should appear
        """
        ordered_sections = set(section_order)
        unorder_sections = [section for section in all_project_sections if section not in ordered_sections]
        project_sections = set(all_project_sections)
        section_order = [sec for sec in section_order + unorder_sections if sec in project_sections]
        return section_order

    @staticmethod
    def _get_all_project_sections(args: SummarizerArgs) -> List[str]:
        """
        Gets all sections in the order in which they should be created
        :param args: The arguments for the project summarizer
        :return: All section ids in the order in which they should be created
        """
        current_sections = set(args.project_summary_sections)
        sections_to_add = set(args.new_sections.keys()).difference(current_sections)
        return args.project_summary_sections + list(sections_to_add)
