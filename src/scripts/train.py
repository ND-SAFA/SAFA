import argparse
import os
import sys

os.environ["DJANGO_SETTINGS_MODULE"] = "server.settings"

#
# Argument Parsing
#
parser = argparse.ArgumentParser(
    prog='PreTrainer',
    description='Pre-trains a bert model on a directory of documents.')
parser.add_argument('data')  # positional argument
parser.add_argument('output')
parser.add_argument('-model', help="The model to pre-train", default="roberta-base")
parser.add_argument('-root', default='~/projects/safa/tgen/src')
parser.add_argument('-epochs', default=10)

args = parser.parse_args()

#
# Path Expansion
#
path_vars = ["root", "data", "output"]
for path_var in path_vars:
    path_value = getattr(args, path_var)
    path_value = os.path.expanduser(path_value)
    setattr(args, path_var, path_value)
    assert os.path.exists(path_value), path_value

sys.path.append(args.root)

#
# IMPORTS
#
from tracer.models.base_models.supported_base_model import SupportedBaseModel
from jobs.job_factory import JobFactory
from django.core.wsgi import get_wsgi_application
from jobs.train_job import TrainJob
from server.serializers.job_factory.training_request_serializer import TrainingRequestSerializer

application = get_wsgi_application()
#
# Script Initialization
#


if __name__ == "__main__":
    job_definition = {
        "baseModel": SupportedBaseModel.AUTO_MODEL,
        "modelPath": args.model,
        "outputDir": args.output,
        "saveJobOutput": True,
        "data": {
            "creator": "CSV",
            "params": {
                "data_file_path": args.data
            },
            "preProcessingSteps": []
        },
        "settings": {
            "trace_args_params": {
                "num_train_epochs": args.epochs
            }
        }
    }
    pre_training_serializer = TrainingRequestSerializer(data=job_definition)
    assert pre_training_serializer.is_valid(), pre_training_serializer.errors
    job_factory: JobFactory = pre_training_serializer.save()
    pre_training_job = job_factory.build(TrainJob)
    pre_training_job.run()
