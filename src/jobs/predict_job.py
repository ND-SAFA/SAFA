from typing import Dict

from jobs.abstract_trace_job import AbstractTraceJob
from jobs.components.job_result import JobResult


class PredictJob(AbstractTraceJob):

    def _run(self) -> JobResult:
        """
        Performs predictions and (optionally) evaluation of model
        :return: results of the prediction including prediction values and associated ids
        """
        prediction_output = self.get_trainer().perform_prediction()
        return self._result_from_prediction_output(prediction_output)

    @staticmethod
    def _result_from_prediction_output(trainer_output: Dict) -> JobResult:
        """
        Creates a TraceJobResult from a dictionary
        :return: a new TraceJobResult
        """
        scores = trainer_output.pop(JobResult.PREDICTIONS)
        pred_id_pairs = trainer_output.pop(JobResult.SOURCE_TARGET_PAIRS)
        predictions = []
        for pred_ids, pred_scores in zip(pred_id_pairs, scores):
            entry = {
                JobResult.SOURCE: pred_ids[0],
                JobResult.TARGET: pred_ids[1],
                JobResult.SCORE: float(pred_scores)
            }
            predictions.append(entry)
        trainer_output[JobResult.PREDICTIONS] = predictions
        return JobResult.from_dict(trainer_output)
