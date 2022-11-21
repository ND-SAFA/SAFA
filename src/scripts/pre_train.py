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
parser.add_argument('-model', help="The model to pre-train", default="roberta-base-uncased")
parser.add_argument('-root', default='~/projects/safa/tgen/src')

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
from jobs.mlm_pre_train_job import MLMPreTrainJob
from server.serializers.job_factory.pre_training_request_serializer import PreTrainingRequestSerializer
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
#
# Script Initialization
#

model = args.model
data_path = args.data
output_path = args.output

if __name__ == "__main__":
    job_definition = {
        "baseModel": SupportedBaseModel.BERT_FOR_MASKED_LM,
        "modelPath": "roberta-base",
        "trainingDataDir": data_path,
        "outputDir": output_path,
        "saveJobOutput": True
    }
    pre_training_serializer = PreTrainingRequestSerializer(data=job_definition)
    assert pre_training_serializer.is_valid(), pre_training_serializer.errors
    job_factory: JobFactory = pre_training_serializer.save()
    pre_training_job = job_factory.build(MLMPreTrainJob)
    pre_training_job.run()
