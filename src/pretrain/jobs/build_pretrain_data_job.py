from typing import Dict

from pretrain.jobs.abstract_pretrain_job import AbstractPreTrainJob


class BuildPretrainDataJob(AbstractPreTrainJob):

    def _run(self) -> Dict:
        """
        Runs the dataset building for pretraining
        :return: the results of the data build
        """
        self.pretrainer.build_pretraining_data()
        return None  # TODO
