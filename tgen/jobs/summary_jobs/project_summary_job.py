from typing import Dict, TypedDict

from tgen.common.util.file_util import FileUtil
from tgen.common.util.llm_response_util import LLMResponseUtil
from tgen.common.util.logging.logger_manager import logger
from tgen.constants.ranking_constants import BODY_ARTIFACT_TITLE, DEFAULT_SUMMARY_TOKENS, PROJECT_SUMMARY_HEADER
from tgen.data.readers.artifact_project_reader import ArtifactProjectReader
from tgen.data.summarizer.summarizer import Summarizer
from tgen.jobs.abstract_job import AbstractJob
from tgen.ranking.common.completion_util import complete_prompts
from tgen.ranking.common.ranking_prompt_builder import RankingPromptBuilder

GOAL = (
    "# Goal\nBelow is the set of software artifacts of a software system. "
    f"The goal is to read through all the artifacts and create a thorough document "
    f"providing all the necessary details to hand off the project to another company."
)
INSTRUCTIONS_GOAL = (
    f"# Task\n"
    f"Below are instructions for creating the document. "
    "Include as much detail as you can. Ignore details that are generally applicable across systems. "
    f"Write the document in markdown and start the document with the header '# {PROJECT_SUMMARY_HEADER}'."
    "\n\nInstructions: "
)
OVERVIEW = "Create a sub-section called `Overview` describing the main purpose of the system."
ENTITIES = "Create a sub-section called `Entities`. Define all the major entities in the system."
FEATURES = "Create a sub-section called `Features` outlining the major features of the system. "
MAJOR_COMPONENTS = (
    "Create a sub-section called `Modules`. "
    "In this high level section enumerate all the major modules in the system and give a brief descriptions of what they do for the system."
)
COMPONENTS = (
    "Under `Modules`, create sub-sections for each module in the system. "
    "For each module, create a detailed report that describes:"
    "\n    - The functionality the module."
    "\n    - The value of the module to the overall system."
    "\n    - The software artifacts that work to implement the functionality of the module"
    "\n    - The differences to other similar modules in the system."
)
DATA_FLOW = (
    "Create a sub-section called `Summary` and write a paragraph describing how "
    "the system fulfills all of its features (outlined in `Features`) using its components. "
    "Describe the interactions between modules and how data flows between them."
)
TASKS_DEFINITIONS = [OVERVIEW, ENTITIES, FEATURES, MAJOR_COMPONENTS, COMPONENTS, DATA_FLOW]
FORMAT = "\n\nEnclose your response in <summary></summary>."
TASKS = "".join([f"\n{i + 1}. {t}" for i, t in enumerate(TASKS_DEFINITIONS)])
INSTRUCTIONS = INSTRUCTIONS_GOAL + TASKS + FORMAT


class ProjectSummaryResponse(TypedDict):
    """
    The response for a project summary request.
    """
    summary: str


class ProjectSummaryJob(AbstractJob):
    def __init__(self, artifact_map: Dict[str, str] = None,
                 artifact_reader: ArtifactProjectReader = None,
                 n_tokens: int = DEFAULT_SUMMARY_TOKENS, export_path: str = None):
        """
        Generates a system specification document for containing all artifacts.
        :param artifact_map:
        :param n_tokens:
        """
        assert artifact_map is not None or artifact_reader is not None, "Please define artifact map or project reader."
        super().__init__()
        if artifact_reader:
            summarizer = Summarizer()
            artifact_reader.set_summarizer(summarizer)
            artifact_map = artifact_reader.read_project().to_map()
        self.artifact_map = artifact_map
        self.n_tokens = n_tokens
        self.export_path = export_path

    def _run(self) -> ProjectSummaryResponse:
        """
        Creates specification document and runs.
        :return: System summary.
        """
        logger.log_title("Creating project specification.")
        prompt_builder = RankingPromptBuilder(goal=GOAL,
                                              instructions=INSTRUCTIONS,
                                              body_title=BODY_ARTIFACT_TITLE)
        artifact_ids = self.artifact_map.keys()
        for target_artifact_name in artifact_ids:
            artifact_content = self.artifact_map[target_artifact_name]
            prompt_builder.with_artifact(target_artifact_name, artifact_content, separator="\n")
        prompt = prompt_builder.get()
        generation_response = complete_prompts([prompt], max_tokens=self.n_tokens, temperature=0)
        summary_response = generation_response.batch_responses[0]
        summary_tag_query = LLMResponseUtil.parse(summary_response, "summary")
        if len(summary_tag_query) == 0:
            summary = summary_response
        else:
            summary = summary_tag_query[0].strip()
        if self.export_path:
            FileUtil.write(summary, self.export_path)
        return ProjectSummaryResponse(summary=summary)
