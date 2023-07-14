from tgen.constants.tgen_constants import SUMMARY_TITLE
from tgen.ranking.common.completion_util import complete_prompts
from tgen.ranking.common.ranking_prompt_builder import RankingPromptBuilder
from tgen.ranking.ranking_args import RankingArgs
from tgen.ranking.ranking_state import RankingState
from tgen.state.pipeline.abstract_pipeline import AbstractPipelineStep
from tgen.util.llm_response_util import LLMResponseUtil

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


class CreateProjectSummary(AbstractPipelineStep[RankingArgs, RankingState]):
    def run(self, args: RankingArgs, state: RankingState) -> None:
        """
        Sets the pipeline to either NO SUMMARY, MANUAL SUMMARY, or GENERATED SUMMARY.
        If NO SUMMARY, summary is set to None
        If MANUAL SUMMARY then summary is set to given
        If GENERATED SUMMARY then project summary is generated for all artifacts.
        :param args: The pipeline arguments.
        :param state: The state of the pipeline.
        :return: None
        """
        if args.project_summary is not None and len(args.project_summary) > 0:  # MANUAL SUMMARY
            summary = args.project_summary
        elif not args.generate_summary:  # NO SUMMARY
            summary = None
        else:  # GENERATED SUMMARY
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

        state.project_summary = summary
