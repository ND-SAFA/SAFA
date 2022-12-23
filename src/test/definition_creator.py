from server.serializers.experiment_serializer import ExperimentSerializer


class DefinitionCreator:

    @staticmethod
    def create(definition_class, definition, **kwargs):
        data = definition
        data.update(kwargs)
        definition = {ExperimentSerializer.KEY: data}
        experiment_serializer = ExperimentSerializer(data=definition)
        assert experiment_serializer.is_valid(), experiment_serializer.errors
        definition_variable = experiment_serializer.save()
        return definition_class.initialize_from_definition(definition_variable)

# model_manager_definition_creator = DefinitionCreator(ModelManager, {
#     "model_path": "path"
# })
#
# job_args_definition_creator = DefinitionCreator(JobArgs, {
#     "output_dir": TEST_OUTPUT_DIR
# })
#
# trainer_args_definition_creator = DefinitionCreator(TrainerArgs, {
#     "output_dir": TEST_OUTPUT_DIR
# })
#
# trainer_dataset_manager_definition_creator = DefinitionCreator(TrainerDatasetManager, {
#     "train": {
#         "objectType": "SAFADatasetCreator",
#         "project_path": os.path.join(TEST_DATA_DIR, "safa")
#     }
# })
