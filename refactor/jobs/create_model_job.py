from typing import Dict

from jobs.abstract_job import AbstractJob
from jobs.responses.base_response import BaseResponse


class CreateModelJob(AbstractJob):

    def _run(self) -> Dict:
        """
        Creates a new model
        :return: the model path
        """
        model_generator = self.get_model_generator()
        model = model_generator.get_model()
        model.save_pretrained(self.output_dir)
        tokenizer = model_generator.get_tokenizer()
        tokenizer.save_pretrained(self.output_dir)
        return {BaseResponse.MODEL_PATH: self.output_dir}
