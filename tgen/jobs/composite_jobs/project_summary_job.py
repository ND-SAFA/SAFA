from typing import Dict, TypedDict

from tgen.constants.tgen_constants import DEFAULT_SUMMARY_TOKENS, SUMMARY_TITLE
from tgen.jobs.abstract_job import AbstractJob
from tgen.ranking.common.completion_util import complete_prompts
from tgen.ranking.common.ranking_prompt_builder import RankingPromptBuilder
from tgen.util.llm_response_util import LLMResponseUtil
from tgen.util.logging.logger_manager import logger

GOAL = "# Task\nBelow is the set of software artifacts of a software system. " \
       "Read through each artifact and reasoning about what the system is doing."
INSTRUCTIONS_GOAL = "# Instructions\nPlease follow the instructions below to create brief software specification document " \
                    "describing the behavior of the system. " \
                    "Exclude details that are generally applicable across systems " \
                    "and focus only on details that are truly specific to the design and behavior of this particular system. " \
                    f"Write the document in markdown and start the document with the header '{SUMMARY_TITLE}'." \
                    "\nInstructions: "
TASKS_DEFINITIONS = [
    "Create a sub-section called `Overview`. Provide a paragraph describing the main functionality of the system.",
    "Create a sub-sections for each major components in the system. ",
    "For each component, provide a paragraph describing its responsibilities and its contribution(s) to the system.",
    "Create a sub-section called `Data Flow` and describe the dependencies between components and how do they interact.",
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
    def __init__(self, artifact_map: Dict[str, str], n_tokens: int = DEFAULT_SUMMARY_TOKENS):
        """
        Generates a system specification document for containing all artifacts.
        :param artifact_map:
        :param n_tokens:
        """
        super().__init__()
        self.artifact_map = artifact_map
        self.n_tokens = n_tokens

    def _run(self) -> ProjectSummaryResponse:
        """
        Creates specification document and runs.
        :return: System summary.
        """
        logger.log_title("Creating project specification.")
        prompt_builder = RankingPromptBuilder(goal=GOAL,
                                              instructions=INSTRUCTIONS,
                                              body_title="# Software Artifacts")
        artifact_ids = self.artifact_map.keys()
        for target_artifact_name in artifact_ids:
            prompt_builder.with_artifact(target_artifact_name, self.artifact_map[target_artifact_name])
        prompt = prompt_builder.get()
        generation_response = complete_prompts([prompt], max_tokens=self.n_tokens, temperature=0)
        response = generation_response.batch_responses[0]
        summary = LLMResponseUtil.parse(response, "summary")[0].strip()
        return ProjectSummaryResponse(summary=summary)
