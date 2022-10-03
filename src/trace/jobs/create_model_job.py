from typing import Dict

from common.jobs.abstract_job import AbstractJob
from common.api.responses import BaseResponse
from trace.jobs.trace_args_builder import TraceArgsBuilder


class CreateModelJob(AbstractJob):

    def __init__(self, args_builder: TraceArgsBuilder):
        super().__init__(args_builder, output_dir=args_builder.output_dir, save_output=False)

    def _run(self) -> Dict:
        """
        Creates a new model
        :return: the model path
        """
        model_generator = self.args.model_generator
        model = model_generator.get_model()
        model.save_pretrained(self.output_dir)
        tokenizer = model_generator.get_tokenizer()
        tokenizer.save_pretrained(self.output_dir)
        return {BaseResponse.MODEL_PATH: self.output_dir}
