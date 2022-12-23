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
