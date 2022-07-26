from jobs.job_args import PretrainArgs
from jobs.base_job import BasePretrainJob


class BuildDataJob(BasePretrainJob):

    def __init__(self, args: PretrainArgs):
        super().__init__(args)

    def __start(self):
        self.pretrain.build_pretraining_data()
