from tgen.jobs.abstract_job import AbstractJob


class CreateModelJob(AbstractJob):

    def _run(self) -> str:
        """
        Creates a new model
        :return: the model path
        """
        model = self.model_manager.get_model()
        model.save_pretrained(self.model_manager.model_output_path)
        tokenizer = self.model_manager.get_tokenizer()
        tokenizer.save_pretrained(self.model_manager.model_output_path)
        return self.model_manager.model_output_path
