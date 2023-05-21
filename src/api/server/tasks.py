from typing import Dict

from tgen.jobs.supported_job_type import SupportedJobType
from tgen.testres.definition_creator import DefinitionCreator


def predict_task(predict_job_definition: Dict) -> Dict:
    """
    Performs trace link prediction.
    :param predict_job_definition: The experiment definition wraping a prediction job.
    :return:
    """
    job_type_name = predict_job_definition.pop("object_type")
    job_type = SupportedJobType.get_value(job_type_name)

    job = DefinitionCreator.create(job_type, predict_job_definition)
    job.run()
    return job.result.to_json(as_dict=True)
