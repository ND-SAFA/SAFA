import uuid
from unittest import mock

from tgen.data.creators.prompt_dataset_creator import PromptDatasetCreator
from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.data.prompts.base_prompt import BasePrompt
from tgen.data.prompts.creation_prompt_generator import CreationPromptGenerator
from tgen.data.tdatasets.dataset_role import DatasetRole
from tgen.hgen.hierarchy_generator import HierarchyGenerator
from tgen.testres.base_tests.base_test import BaseTest, fake_open_ai_completion
from tgen.testres.testprojects.artifact_test_project import ArtifactTestProject
from tgen.train.args.open_ai_args import OpenAiArgs
from tgen.train.trainers.open_ai_trainer import OpenAiTrainer


class TestHierarchyGeneration(BaseTest):

    @mock.patch("community.best_partition")
    @mock.patch("openai.Completion.create")
    def test_summarize(self, mock_completion: mock.MagicMock, mock_partition: mock.MagicMock):
        mock_completion.side_effect = fake_open_ai_completion
        reader = ArtifactTestProject().get_project_reader()
        mock_partition.return_value = {entry["id"]: i % 4 for i, entry in enumerate(ArtifactTestProject().get_artifact_entries())}
        trainer_dataset_manager = TrainerDatasetManager(summarize_dataset_creator=PromptDatasetCreator(project_reader=reader))
        layer_id = str(uuid.uuid4())
        layer_ids = [layer_id for _ in trainer_dataset_manager[DatasetRole.SUMMARIZE].artifact_df.index]
        trainer_dataset_manager[DatasetRole.SUMMARIZE].artifact_df[ArtifactKeys.LAYER_ID] = layer_ids
        tgen_trainer = OpenAiTrainer(trainer_dataset_manager=trainer_dataset_manager, trainer_args=OpenAiArgs(metrics=[]))
        hgen_trainer = OpenAiTrainer(trainer_dataset_manager=trainer_dataset_manager, trainer_args=OpenAiArgs(metrics=[]),
                                     prompt_generator=CreationPromptGenerator(base_prompt=BasePrompt.SHALL_REQUIREMENT_SUMMARY))
        hgen = HierarchyGenerator(tgen_trainer, hgen_trainer)
        dataset = hgen.run(layer_id)
        #dataset
