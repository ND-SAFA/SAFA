from typing import Dict

from trace.jobs.abstract_trace_job import AbstractTraceJob


class PredictJob(AbstractTraceJob):

    def _run(self) -> Dict:
        """
        Performs predictions and (optionally) evaluation of model
        :return: results of the prediction including prediction values and associated ids
        """
        result = self.get_trainer().perform_prediction()
        return result
