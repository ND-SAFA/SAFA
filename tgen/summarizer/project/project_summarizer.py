import uuid
from collections.abc import Generator
from copy import deepcopy
from typing import Dict, List, Tuple, Union

from common_resources.data.dataframes.artifact_dataframe import ArtifactDataFrame
from common_resources.data.keys.structure_keys import ArtifactKeys
from common_resources.data.tdatasets.prompt_dataset import PromptDataset
from common_resources.tools.constants.dataset_constants import PROJECT_SUMMARY_FILENAME
from common_resources.tools.constants.symbol_constants import EMPTY_STRING, NEW_LINE, UNDERSCORE

from tgen.common.constants.project_summary_constants import CUSTOM_TITLE_TAG, MULTI_LINE_ITEMS, PS_QUESTIONS_HEADER, \
    USE_PROJECT_SUMMARY_SECTIONS
from tgen.common.constants.ranking_constants import BODY_ARTIFACT_TITLE, BODY_VERSION_TITLE, DEFAULT_COMPLETION_TOKENS
from common_resources.tools.t_logging.logger_manager import logger
from common_resources.tools.util.base_object import BaseObject
from common_resources.tools.util.file_util import FileUtil
from common_resources.tools.util.prompt_util import PromptUtil
from common_resources.tools.util.unique_id_manager import DeterministicUniqueIDManager
from tgen.core.trainers.llm_trainer import LLMTrainer
from tgen.core.trainers.llm_trainer_state import LLMTrainerState
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from common_resources.llm.abstract_llm_manager import AbstractLLMManager
from tgen.prompts.artifact_prompt import ArtifactPrompt
from tgen.prompts.multi_artifact_prompt import MultiArtifactPrompt
from tgen.prompts.prompt import Prompt
from tgen.prompts.prompt_args import PromptArgs
from tgen.prompts.prompt_builder import PromptBuilder
from tgen.prompts.questionnaire_prompt import QuestionnairePrompt
from tgen.prompts.supported_prompts.supported_prompts import SupportedPrompts
from tgen.summarizer.project.supported_project_summary_sections import PROJECT_SUMMARY_MAP
from tgen.summarizer.summarizer_args import SummarizerArgs
from tgen.summarizer.summarizer_util import SummarizerUtil
from tgen.summarizer.summary import Summary


class ProjectSummarizer(BaseObject):

    def __init__(self, summarizer_args: SummarizerArgs, dataset: PromptDataset = None,
                 project_summary_versions: List[Summary] = None,
                 reload_existing: bool = True, n_tokens: int = DEFAULT_COMPLETION_TOKENS,
                 summarizer_id: str = str(uuid.uuid4())):
        """
        Generates a system specification document for containing all artifacts.
        :param summarizer_args: The args necessary for the summary
        :param dataset: The dataset to create the summary for
        :param project_summary_versions: A list of different versions of the project summary from unique subsets.
        :param reload_existing: If True, reloads an existing project summary if it exists
        :param n_tokens: The token limit for the LLM
        :param summarizer_id: Id assigned to this summarizer
        """
        super().__init__()
        self.args = summarizer_args
        self.project_summary_versions = project_summary_versions
        self.dataset = dataset
        assert self.project_summary_versions or self.dataset, \
            "Must supply existing project summaries or artifacts to create one"

        self.llm_manager: AbstractLLMManager = summarizer_args.llm_manager_for_project_summary
        self.n_tokens = n_tokens
        self.export_dir = summarizer_args.export_dir
        self.save_progress = bool(self.export_dir)
        self.reload_existing = reload_existing
        self.project_summary = Summary() if not dataset or not dataset.project_summary else deepcopy(dataset.project_summary)
        self.all_project_sections = self._get_all_project_sections(self.args)
        self.section_display_order = self._get_section_display_order(self.args.section_display_order,
                                                                     self.all_project_sections)

        self.uuid_manager = DeterministicUniqueIDManager(summarizer_id)

    def summarize(self) -> Summary:
        """
        Creates the project summary from the project artifacts.
        :return: The summary of the project.
        """
        save_path = self.get_save_path(export_dir=self.export_dir)
        if FileUtil.safely_check_path_exists(save_path) and self.reload_existing:
            logger.info(f"Loading previous project summary from {save_path}")
            self.project_summary = Summary.load_from_file(save_path)

        if not self.args.project_summary_sections or not SummarizerUtil.needs_project_summary(self.project_summary, self.args):
            return self.project_summary

        self._create_sections(async_sections_only=True)  # create sections that can be created asynchronously
        self._create_sections(async_sections_only=False)  # create sections that require other sections to be included in the prompt
        self.project_summary.re_order_sections(self.section_display_order, remove_unordered_sections=True)
        self.uuid_manager.generate_new_id()
        return self.project_summary

    def get_generation_iterator(self, async_sections_only: bool = False) -> Generator:
        """
        Creates iterator for section titles and questions.
        :param async_sections_only: If true, iterators only through sections that can be generated asynchronously.
        :return: Iterator for each title and prompt.
        """
        for section_id in self.all_project_sections:
            if section_id not in self.project_summary and (not async_sections_only or self.can_be_generated_async(section_id)):
                section_prompt = self.get_section_prompt_by_id(section_id)
                yield section_id, section_prompt

    @staticmethod
    def can_be_generated_async(section_id: str) -> bool:
        """
        Returns whether the section can be generated async or requires earlier sections to be generated first.
        :param section_id: The section id to check if it can be generated async.
        :return: Whether the section can be generated async or requires earlier sections to be generated first.
        """
        return section_id not in USE_PROJECT_SUMMARY_SECTIONS

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

    @staticmethod
    def get_save_path(export_dir: str, as_json: bool = True) -> str:
        """
        Gets the path to save the summary at
        :param export_dir: The directory to save the summary to
        :param as_json: If True, saves it as a json, else as a txt
        :return: The save path
        """
        if not export_dir:
            return export_dir
        path = FileUtil.safely_join_paths(export_dir, PROJECT_SUMMARY_FILENAME)
        ext = FileUtil.JSON_EXT if as_json else FileUtil.TEXT_EXT
        return FileUtil.add_ext(path, ext)

    def _create_sections(self, async_sections_only: bool = False) -> None:
        """
        Handles creating each section of the project summary.
        :param async_sections_only: If true, iterators only through sections that can be generated asynchronously.
        :return: None
        """
        sections_being_created = [s for s in SummarizerUtil.missing_project_summary_sections(self.project_summary, self.args)
                                  if not async_sections_only or self.can_be_generated_async(s)]
        if len(sections_being_created) == 0:
            return
        logger.log_title(f"Creating project specification: {sections_being_created}")
        prompt_builders = {section_id: self._create_prompt_builder(section_id, section_prompt)
                           for section_id, section_prompt in self.get_generation_iterator(async_sections_only=async_sections_only)}
        dataset = [self._create_dataset_from_project_summaries(self.project_summary_versions, section_id)
                   for section_id, section_prompt in self.get_generation_iterator(async_sections_only=async_sections_only)] \
            if not self.dataset else [self.dataset]
        generated_section_responses = self._generate_sections(prompt_builders, dataset)
        for i, (section_id, section_prompt) in enumerate(self.get_generation_iterator(async_sections_only=async_sections_only)):
            if isinstance(generated_section_responses[i], Exception):
                logger.warning(f"Generating {section_id} failed due to {generated_section_responses[i]}")
                continue

            self._create_section(generated_section_responses[i], section_id, section_prompt)

    def _create_section(self, section_response: Dict, section_id: str, section_prompt: QuestionnairePrompt) -> bool:
        """
        Creates the project section from the LLM response.
        :param section_response: The response for the section from the LLM.
        :param section_id: The id of the section being created.
        :param section_prompt: The prompt used to create the section.
        :return: Whether the creation was successful.
        """
        try:
            task_tag = section_prompt.get_response_tags_for_prompt(-1)
            task_tag = task_tag[0] if isinstance(task_tag, list) else task_tag
            section_body, section_title = self._parse_section(response=section_response,
                                                              task_tag=task_tag, multi_line_items=section_id in MULTI_LINE_ITEMS)
            if not section_title:
                section_title = section_id
            self.project_summary.add_section(section_id=section_id, section_title=section_title, body=section_body)
            if self.save_progress:
                self.project_summary.save(self.get_save_path(export_dir=self.export_dir))
            return True
        except Exception:
            logger.exception(f"Unable to create project section {section_id}")
            return False

    def _generate_sections(self, prompt_builders: Dict[str, PromptBuilder],
                           dataset: Union[PromptDataset, List[PromptDataset]]) -> List[Dict]:
        """
        Has the LLM generate the section corresponding using the prompt builder
        :param prompt_builders: Contains prompts necessary for generating sections
        :param dataset: The dataset that will be provided to the model when generating
        :return: Responses for all sections
        """
        self.llm_manager.llm_args.set_max_tokens(self.n_tokens)
        self.llm_manager.llm_args.temperature = 0

        trainer_dataset_manager = TrainerDatasetManager.create_from_datasets(eval=dataset)
        trainer = LLMTrainer(LLMTrainerState(llm_manager=self.llm_manager,
                                             prompt_builders=list(prompt_builders.values()),
                                             trainer_dataset_manager=trainer_dataset_manager))
        save_and_load_path = self._get_responses_save_and_load_path(list(prompt_builders.keys()))
        res = trainer.perform_prediction(raise_exception=False, save_and_load_path=save_and_load_path)
        failures = {i for i, r in enumerate(res.original_response) if isinstance(r, Exception)}
        parsed_responses = [(res.predictions[i][prompt_builder.get_prompt(-1).args.prompt_id]
                             if i not in failures else res.original_response[i])
                            for i, prompt_builder in enumerate(prompt_builders.values())]
        return parsed_responses

    def _create_prompt_builder(self, section_id: str, section_prompt: QuestionnairePrompt) -> PromptBuilder:
        """
        Creates a prompt builder for a given section prompt
        :param section_id: The id of the section
        :param section_prompt: The prompt used to create the section
        :return: The prompt builder for creating the section
        """
        assert isinstance(section_prompt, QuestionnairePrompt), f"Expected section {section_id} prompt " \
                                                                f"to be a {QuestionnairePrompt.__class__.__name__}"
        content_prompt = SupportedPrompts.PROJECT_SUMMARY_CONTEXT_ARTIFACTS.value if self.dataset \
            else SupportedPrompts.PROJECT_SUMMARY_CONTEXT_VERSIONS.value
        prompt_start = BODY_ARTIFACT_TITLE if self.dataset else BODY_VERSION_TITLE
        artifacts_prompt = MultiArtifactPrompt(prompt_start=prompt_start,
                                               build_method=MultiArtifactPrompt.BuildMethod.XML,
                                               xml_tags=ArtifactPrompt.DEFAULT_XML_TAGS
                                               if self.dataset else {"versions": ["id", "body"]},
                                               include_ids=self.dataset is not None)
        section_prompt.set_instructions(f"{PS_QUESTIONS_HEADER}{NEW_LINE}"
                                        f"*Importantly, ONLY answer the {len(section_prompt.child_prompts)} questions below "
                                        f"and ensure the ALL tags {section_prompt.get_all_response_tags()} "
                                        f"are included in your answer*")
        prompt_builder = PromptBuilder(prompts=[content_prompt,
                                                artifacts_prompt,
                                                section_prompt])
        if self.project_summary and section_id in USE_PROJECT_SUMMARY_SECTIONS:
            current_summary = self.project_summary.to_string()
            prompt_builder.add_prompt(Prompt(f"# Current Document\n\n{current_summary}",
                                             prompt_args=PromptArgs(allow_formatting=False)), 1)
        return prompt_builder

    @staticmethod
    def _parse_section(response: Dict, task_tag: str, multi_line_items: bool = False) -> Tuple[str, str]:
        """
        Extracts the necessary information for creating the section from its response.
        :param response: The section response.
        :param task_tag: The tag used to retrieve the generations from the parsed response.
        :param multi_line_items: If True, expects each item in the body to span multiple lines.
        :return: The section body and section title (if one was generated).
        """
        body_res = response[task_tag]
        body_res = [PromptUtil.strip_new_lines_and_extra_space(r, remove_all_new_lines=len(
            body_res) > 1 and not multi_line_items)
                    for r in body_res]
        task_title = response[CUSTOM_TITLE_TAG][0] if response.get(CUSTOM_TITLE_TAG) else None
        deliminator = NEW_LINE if not multi_line_items else f"{NEW_LINE}{PromptUtil.as_markdown_header(EMPTY_STRING, level=2)}"
        task_body = body_res[0] if len(body_res) == 1 else deliminator.join(body_res)
        return deliminator + task_body, task_title

    @staticmethod
    def _get_section_display_order(section_order: List[str], all_project_sections: List[str]) -> List[str]:
        """
        Gets the order in which the sections should appear
        :param section_order: The order the sections should be displayed in. Can be subset of full sections to display.
        :param all_project_sections: List of all sections to include.
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

    @staticmethod
    def _create_dataset_from_project_summaries(project_summaries: List[Summary], curr_section: str) -> PromptDataset:
        """
        Creates a dataset using the project summaries' sections as artifacts
        :param project_summaries: The versions of the project summary
        :param curr_section: The section currently being built
        :return: A dataset using the project summaries' sections as artifacts
        """
        versions = [summary.to_string([curr_section]) for summary in project_summaries]
        artifact_df = ArtifactDataFrame({ArtifactKeys.ID: [i for i in range(len(versions))],
                                         ArtifactKeys.CONTENT: versions,
                                         ArtifactKeys.LAYER_ID: ["summary_version" for _ in versions]})
        return PromptDataset(artifact_df=artifact_df)

    def _get_responses_save_and_load_path(self, section_names: List[str]) -> str:
        """
        Gets the save and load path for responses.
        :param section_names: The sections being generated.
        :return: The save and load path for responses.
        """
        sections = UNDERSCORE.join(section_names)
        return FileUtil.safely_join_paths(self.args.export_dir,
                                          FileUtil.add_ext(f"ps_{sections}{self.uuid_manager.get_uuid()}", FileUtil.YAML_EXT)
                                          )
