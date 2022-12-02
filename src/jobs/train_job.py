from jobs.abstract_trace_job import AbstractTraceJob
from jobs.components.job_result import JobResult


class TrainJob(AbstractTraceJob):

    def _run(self, **kwargs) -> JobResult:
        """
        Runs the training and obtains results
        :return: results of the training including as loss and time
        """
        trainer = self.get_trainer(**kwargs)
        training_output = trainer.perform_training()
        trainer.save_model(self.output_dir)
        return JobResult.from_dict(training_output)
