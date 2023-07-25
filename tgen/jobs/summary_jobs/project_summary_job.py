from typing import Dict, TypedDict

from tgen.common.util.file_util import FileUtil
from tgen.common.util.llm_response_util import LLMResponseUtil
from tgen.common.util.logging.logger_manager import logger
from tgen.constants.tgen_constants import BODY_ARTIFACT_TITLE, DEFAULT_SUMMARY_TOKENS, SUMMARY_TITLE
from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
from tgen.data.readers.artifact_project_reader import ArtifactProjectReader
from tgen.data.summarizer.summarizer import Summarizer
from tgen.jobs.abstract_job import AbstractJob
from tgen.ranking.common.completion_util import complete_prompts
from tgen.ranking.common.ranking_prompt_builder import RankingPromptBuilder

GOAL = "# Task\nBelow is the set of software artifacts of a software system. " \
       "Read through each artifact and reason about what the system is doing."
INSTRUCTIONS_GOAL = "# Instructions\nPlease follow the instructions below to create brief software specification document " \
                    "describing the behavior of the system. " \
                    "Exclude details that are generally applicable across systems " \
                    "and focus only on details that are truly specific to the design and behavior of this particular system. " \
                    f"Write the document in markdown and start the document with the header '{SUMMARY_TITLE}'." \
                    "\nInstructions: "
TASKS_DEFINITIONS = [
    "Create a sub-section called `Overview`. Provide a paragraph describing the main functionality of the system.",
    "Create a sub-section called `Entities`. Enumerate and define each of the major entities in the system. "
    "Also include a paragraph describing how the entities interact with each other.",
    "Create a sub-section called `Features`. Outline the major features of the software system. ",
    "Create a sub-section called `Major Components`. Within it, create a sub-section for each sub-system. "
    "For each sub-system, provide a paragraph describing its unique role in the overall system. "
    "List system artifacts that are directly linked to that component. All child artifacts should have at least one parent. "
    "Most children artifact should have a single parent and few will have many.",
    "Create a sub-section called `Data Flow` and describe the dependencies between major sub-systems and components. "
    "Highlight how they interact to accomplish the listed features.",
]
FORMAT = "\n\n" \
         "Enclose your response in <summary></summary>."
TASKS = "".join([f"\n- {t}" for t in TASKS_DEFINITIONS])
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
            artifact_map = ProjectSummaryJob.create_artifact_map(artifact_reader)
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
            prompt_builder.with_artifact(target_artifact_name, self.artifact_map[target_artifact_name])
        prompt = prompt_builder.get()
        generation_response = complete_prompts([prompt], max_tokens=self.n_tokens, temperature=0)
        response = generation_response.batch_responses[0]
        summary = LLMResponseUtil.parse(response, "summary")[0].strip()
        if self.export_path:
            FileUtil.write(summary, self.export_path)
        return ProjectSummaryResponse(summary=summary)

    @staticmethod
    def create_artifact_map(reader: ArtifactProjectReader) -> Dict[str, str]:
        artifact_map: Dict[str, str] = {}
        artifact_df = reader.read_project()
        for artifact_id, artifact_row in artifact_df.itertuples():
            artifact_map[artifact_id] = artifact_row[ArtifactKeys.CONTENT]
        return artifact_map
