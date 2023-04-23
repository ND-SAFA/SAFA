import os

from dotenv import load_dotenv

load_dotenv()

os.environ["DEPLOYMENT"] = "development"

from tgen.constants import GENERATION_MODEL_DEFAULT
from tgen.data.creators.prompt_dataset_creator import PromptDatasetCreator
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.data.prompts.generation_prompt_creator import GenerationPromptCreator
from tgen.data.readers.artifact_project_reader import ArtifactProjectReader
from tgen.data.summarizer.summarizer import Summarizer
from tgen.hgen.hgen_args import HGenArgs
from tgen.jobs.hgen_jobs.hgen_job import HGenJob
from tgen.train.args.open_ai_args import OpenAiArgs
from tgen.train.trainers.open_ai_trainer import OpenAiTrainer
from tgen.train.trainers.supported_trainer import SupportedTrainer

if __name__ == "__main__":
    project_path = os.path.join(os.getenv("DATA_PATH"), "dr_onboard_autonomy")
    trainer_dataset_manager = TrainerDatasetManager(eval_dataset_creator=PromptDatasetCreator(
        project_reader=ArtifactProjectReader(project_path=project_path), summarizer=Summarizer()))
    args = HGenArgs(hgen_trainer_type=SupportedTrainer.OPEN_AI, hgen_prompt_creator=GenerationPromptCreator(),
                    hgen_base_model=GENERATION_MODEL_DEFAULT, hgen_trainer_args=OpenAiArgs(metrics=[]),
                    source_layer_id="Code", tgen_trainer=OpenAiTrainer(trainer_dataset_manager=trainer_dataset_manager,
                                                                       trainer_args=OpenAiArgs(metrics=[])))
    export_path = os.path.join(os.getenv("OUTPUT_PATH"), "hgen", "dr_onboard_autonomy")
    job = HGenJob(hgen_args=args, export_path=export_path, save_dataset_checkpoints=True)
    job_result = job.run()
