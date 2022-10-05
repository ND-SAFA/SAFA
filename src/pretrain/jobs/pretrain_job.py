from typing import Dict

from pretrain.jobs.abstract_pretrain_job import AbstractPreTrainJob


class PretrainJob(AbstractPreTrainJob):

    def _run(self) -> Dict:
        """
        Runs the pretraining
        :return: the results of the pretraining
        """
        self.pretrainer.build()
        return None  # TODO
