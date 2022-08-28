from trace.jobs.abstract_trace_job import AbstractTraceJob


class TrainJob(AbstractTraceJob):

    def _run(self):
        """
        Runs the training and obtains results
        :return: results of the training including as loss and time
        """
        result = self.trainer.perform_training()
        return result
