from typing import Dict, Any

from server.serializers.experiment_serializer import ExperimentSerializer
from variables.definition_variable import DefinitionVariable


class DefinitionCreator:

    @staticmethod
    def create(definition_class, definition, **kwargs) -> Any:
        """
        Creates a object from its definition
        :param definition_class: The class of object to create
        :param definition: The definition containing parameters for initialization
        :param kwargs: Any additional arguments used to create the object
        :return: The object
        """
        data = definition
        data.update(kwargs)
        definition_variable = DefinitionCreator.create_definition_variable(data)
        return definition_class.initialize_from_definition(definition_variable)

    @staticmethod
    def create_definition_variable(data: Dict) -> DefinitionVariable:
        """
        Creates a definition variable from a dictionary
        :param data: The data as a dictionary
        :return: The data as a definition var
        """
        definition = {ExperimentSerializer.KEY: data}
        experiment_serializer = ExperimentSerializer(data=definition)
        assert experiment_serializer.is_valid(), experiment_serializer.errors
        return experiment_serializer.save()
