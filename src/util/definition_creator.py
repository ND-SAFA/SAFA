from typing import Dict

from server.serializers.experiment_serializer import ExperimentSerializer


class DefinitionCreator:

    @staticmethod
    def create(definition_class, definition, **kwargs):
        data = definition
        data.update(kwargs)
        definition_variable = DefinitionCreator.create_definition_variable(data)
        return definition_class.initialize_from_definition(definition_variable)

    @staticmethod
    def create_definition_variable(data: Dict):
        definition = {ExperimentSerializer.KEY: data}
        experiment_serializer = ExperimentSerializer(data=definition)
        assert experiment_serializer.is_valid(), experiment_serializer.errors
        return experiment_serializer.save()
