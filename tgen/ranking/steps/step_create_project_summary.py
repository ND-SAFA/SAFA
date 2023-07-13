import os

from tgen.ranking.common.completion_util import complete_prompts
from tgen.ranking.common.ranking_prompt_builder import RankingPromptBuilder
from tgen.ranking.ranking_args import RankingArgs
from tgen.ranking.ranking_state import RankingState
from tgen.state.pipeline.abstract_pipeline import AbstractPipelineStep
from tgen.util.file_util import FileUtil
from tgen.util.llm_response_util import LLMResponseUtil
from tgen.util.logging.logger_manager import logger

GOAL = "# Task\nBelow is the set of software artifacts of a software system. " \
       "Read through each artifact and reasoning about what the system is doing."
INSTRUCTIONS_GOAL = "# Instructions\nPlease follow the instructions below to create brief software specification document " \
                    "describing the behavior of the system. " \
                    "Exclude details that are generally applicable across systems " \
                    "and focus only on details that are truly specific to the design and behavior of this particular system. " \
                    "Write the document in markdown and start the document with the header '# Software Specification'." \
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


class CreateProjectSummary(AbstractPipelineStep[RankingArgs, RankingState]):
    def run(self, args: RankingArgs, state: RankingState) -> None:
        summary_path = os.path.join(args.export_dir, "project_summary.txt")
        if os.path.exists(summary_path):
            logger.info(f"Reloading project summary from: {summary_path}")
            summary = FileUtil.read_file(summary_path)
        else:
            prompt_builder = RankingPromptBuilder(goal=GOAL,
                                                  instructions=INSTRUCTIONS,
                                                  body_title="# Software Artifacts")
            artifact_ids = args.artifact_map.keys()
            for target_artifact_name in artifact_ids:
                prompt_builder.with_artifact(target_artifact_name, args.artifact_map[target_artifact_name])
            prompt = prompt_builder.get()
            generation_response = complete_prompts([prompt], max_tokens=args.n_summary_tokens)
            response = generation_response.batch_responses[0]
            summary = LLMResponseUtil.parse(response, "summary")[0].strip()
            FileUtil.write(summary, summary_path)
            logger.info(f"Saving project summary to: {summary_path}")

        state.project_summary = summary
