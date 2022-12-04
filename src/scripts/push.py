import argparse
import os
import sys

from transformers import AutoModel

parser = argparse.ArgumentParser(description='Runs regular bert model.')
parser.add_argument('model')
parser.add_argument('export')
parser.add_argument('-commit', default="FEATURE: Pushing model from tgen.")
parser.add_argument('-root', default='~/tgen/src')
args = parser.parse_args()

args.root = os.path.expanduser(args.root)

os.environ["DJANGO_SETTINGS_MODULE"] = "server.settings"
assert os.path.exists(args.root), args.root
sys.path.append(args.root)
from models.base_models.supported_base_model import SupportedBaseModel
from models.model_manager import ModelManager
from train.trainer_args import TrainerArgs
from train.trace_trainer import TraceTrainer

if __name__ == "__main__":
    local_model_generator = ModelManager(args.model)
    local_model_generator.auto_class = AutoModel
    output_dir = os.path.join(args.root, "output", args.export)
    local_trace_args = TrainerArgs(None, None)
    trace_trainer = TraceTrainer(local_trace_args, model_manager=local_model_generator)
    trace_trainer.push_to_hub(args.commit)
