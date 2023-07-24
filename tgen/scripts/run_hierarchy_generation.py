import os

from dotenv import load_dotenv

from tgen.core.args.open_ai_args import OpenAIArgs
from tgen.core.trainers.llm_trainer_state import LLMTrainerState
from tgen.data.prompts.prompt_builder import PromptBuilder
from tgen.models.llm.llm_task import LLMCompletionType
from tgen.models.llm.open_ai_manager import OpenAIManager

load_dotenv()

os.environ["DEPLOYMENT"] = "development"

from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.data.readers.dataframe_project_reader import DataFrameProjectReader
from tgen.data.creators.prompt_dataset_creator import PromptDatasetCreator
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.data.readers.artifact_project_reader import ArtifactProjectReader
from tgen.data.summarizer.summarizer import Summarizer
from tgen.hgen.hgen_args import HGenArgs
from tgen.jobs.hgen_jobs.hgen_job import HGenJob
from tgen.core.trainers.llm_trainer import LLMTrainer

DO_SUMMARIZE = True
USE_DATASET_CREATOR_FOR_SOURCES = False

if __name__ == "__main__":
    data_path = os.getenv("DATA_PATH")
    output_path = os.getenv("OUTPUT_PATH")

    project_path = os.path.join(data_path, "dr_onboard_autonomy") if DO_SUMMARIZE else \
        os.path.join(data_path, "dr_onboard_autonomy_summarizations")
    hgen_llm_manager = OpenAIManager(OpenAIArgs())
    tgen_llm_manager = OpenAIManager(OpenAIArgs())
    summarizer = Summarizer(hgen_llm_manager) if DO_SUMMARIZE else None
    export_path = os.path.join(output_path, "hgen", "dr_onboard_autonomy")

    if USE_DATASET_CREATOR_FOR_SOURCES:
        tgen_trainer = None
        dataset_creator_for_sources = TraceDatasetCreator(
            DataFrameProjectReader(project_path=os.path.join(data_path, "dr_onboard_autonomy_trace_dataset"),
                                   overrides={
                                       "allowed_orphans": -1,
                                       "allowed_missing_sources": 1000,
                                       "allowed_missing_targets": 1000
                                   }))
    else:
        dataset_creator_for_sources = None
        trainer_dataset_manager = TrainerDatasetManager(eval_dataset_creator=PromptDatasetCreator(
            project_reader=ArtifactProjectReader(project_path=project_path), summarizer=summarizer))
        tgen_trainer = LLMTrainer(LLMTrainerState(trainer_dataset_manager=trainer_dataset_manager, prompt_builder=PromptBuilder(),
                                                  # TODO make prompts
                                                  llm_manager=tgen_llm_manager, completion_type=LLMCompletionType.CLASSIFICATION))

    args = HGenArgs(
        source_layer_id="Code", tgen_trainer=tgen_trainer,
        dataset_creator_for_sources=dataset_creator_for_sources)
    job = HGenJob(hgen_args=args, llm_manager=hgen_llm_manager, export_path=export_path)
    job_result = job.run()
