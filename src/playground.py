import os
import time
import uuid
from typing import Optional

from celery import shared_task
from celery.result import AsyncResult
from dotenv import load_dotenv

os.environ["DJANGO_SETTINGS_MODULE"] = "api.server.settings"

from api.endpoints.views.predict_serializer import TraceRequest
from api.endpoints.views.trace_view import create_predict_definition
from api.utils.view_util import ViewUtil
from tgen.server.api.api_definition import ApiDefinition
from tgen.testres.definition_creator import DefinitionCreator
from tgen.util.logging.logger_manager import logger


@shared_task
def predict_test(prediction_payload: TraceRequest):
    job_id = uuid.uuid4()
    logger.info(f"Storing result under job id: {job_id}")

    model = prediction_payload.get("model", "gpt")
    dataset_definition: ApiDefinition = prediction_payload["dataset"]
    prompt: Optional[str] = prediction_payload.get("prompt", None)
    dataset: ApiDefinition = DefinitionCreator.create(ApiDefinition, dataset_definition)

    api_id = uuid.uuid4()
    prediction_job = create_predict_definition(str(api_id), dataset, model, prompt)

    prediction_result = ViewUtil.run_job(prediction_job)

    return {"predictions": prediction_result.prediction_entries}


dataset = {
    "model": "GPT",
    "dataset": {
        "source_layers": [
            {
                "F1": "A UAV flies dangerously close to another object."
            }
        ],
        "target_layers": [
            {
                "F2": "A UAV flies too close to ground-based objects (e.g. ground trees buildings people).",
                "D10": "If the number of locked sattelites falls below a threshold the system shall automatically display a warning message notifying the RPIC. The position inaccuracy shall be displayed in the user interface e.g. by displaying a circle around the UAV showing its approx. estimated position."
            }
        ]
    }
}
if __name__ == "__main__":
    load_dotenv()
    task = predict_test.delay(dataset)
    print("Task ID:", task.id)
    task_result = AsyncResult(task.id)

    while not task_result.successful():
        time.sleep(1)
        print("sleeping...")
        if task_result.status == "FAILURE":
            raise Exception(task_result.traceback)
    task_result = task_result.get()
    print(type(task_result))
