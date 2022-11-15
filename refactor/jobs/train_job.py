from jobs.abstract_trace_job import AbstractTraceJob


class TrainJob(AbstractTraceJob):

    def _run(self, **kwargs):
        """
        Runs the training and obtains results
        :return: results of the training including as loss and time
        """
        trainer = self.get_trainer()
        result = trainer.perform_training()
        trainer.save_model(self.output_dir)
        return result
