import os

from dotenv import load_dotenv

from tgen.train.args.open_ai_args import OpenAiArgs

load_dotenv()

os.environ["DEPLOYMENT"] = "development"

from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.data.readers.dataframe_project_reader import DataFrameProjectReader
from tgen.constants import GENERATION_MODEL_DEFAULT
from tgen.data.creators.prompt_dataset_creator import PromptDatasetCreator
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.data.prompts.generation_prompt_creator import GenerationPromptCreator
from tgen.data.readers.artifact_project_reader import ArtifactProjectReader
from tgen.data.summarizer.summarizer import Summarizer
from tgen.hgen.hgen_args import HGenArgs
from tgen.jobs.hgen_jobs.hgen_job import HGenJob
from tgen.train.trainers.llm_trainer import LLMTrainer
from tgen.train.trainers.supported_trainer import SupportedTrainer

DO_SUMMARIZE = False
USE_DATASET_CREATOR_FOR_SOURCES = False

if __name__ == "__main__":
    data_path = os.getenv("DATA_PATH")
    output_path = os.getenv("OUTPUT_PATH")

    project_path = os.path.join(data_path, "dr_onboard_autonomy") if DO_SUMMARIZE else \
        os.path.join(data_path, "dr_onboard_autonomy_summarizations")
    summarizer = Summarizer() if DO_SUMMARIZE else None
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
        tgen_trainer = LLMTrainer(trainer_dataset_manager=trainer_dataset_manager)

    args = HGenArgs(hgen_trainer_type=SupportedTrainer.OPEN_AI,
                    hgen_trainer_args=OpenAiArgs(prompt_creator=GenerationPromptCreator()),
                    hgen_base_model=GENERATION_MODEL_DEFAULT,
                    source_layer_id="Code", tgen_trainer=tgen_trainer, dataset_creator_for_sources=dataset_creator_for_sources)
    job = HGenJob(hgen_args=args, export_path=export_path, save_dataset_checkpoints=True)
    job_result = job.run()
