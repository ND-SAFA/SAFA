import os.path
from typing import List

from tgen.common.constants.deliminator_constants import EMPTY_STRING
from tgen.common.util.dataclass_util import DataclassUtil
from tgen.common.util.dict_util import DictUtil
from tgen.common.util.param_specs import ParamSpecs
from tgen.common.util.status import Status
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.hgen.hgen_args import HGenArgs
from tgen.hgen.hgen_state import HGenState
from tgen.jobs.abstract_job import AbstractJob
from tgen.jobs.components.args.job_args import JobArgs
from tgen.jobs.hgen_jobs.base_hgen_job import BaseHGenJob


class MultiLayerHGenJob(AbstractJob):

    def __init__(self, starting_hgen_job: BaseHGenJob, target_types: List[str] = None, job_args: JobArgs = None):
        """
        Initializes the job with args needed for hierarchy generator
        :param starting_hgen_job: The initial hgen job to run to get the first layer of artifacts
        :param target_types: The list of target types going up the hierarchy
        :param job_args: The arguments need for the job
        """
        if target_types is None:
            target_types = []
        self.starting_hgen_job = starting_hgen_job
        if len(target_types) > 0 and self.starting_hgen_job.get_hgen_args().target_type == target_types[0]:
            # target types should not include start target type
            target_types.pop(0)
        self.target_types = target_types
        super().__init__(job_args)

    def _run(self) -> TraceDataset:
        """
        Runs all the hgen jobs, slowly progressing up the hierarchy
        :return: The final dataset created by the top level hgen job
        """
        current_hgen_job = self.starting_hgen_job
        current_hgen_job.result.experimental_vars = {"target_type": current_hgen_job.get_hgen_args().target_type}

        last_index = len(self.target_types) - 1
        add_seeds_as_artifacts = self.starting_hgen_job.hgen_args.add_seeds_as_artifacts
        for i, next_target_type in enumerate(self.target_types):
            if i == last_index:
                current_hgen_job.hgen_args.add_seeds_as_artifacts = add_seeds_as_artifacts
            else:
                current_hgen_job.hgen_args.add_seeds_as_artifacts = False
            res = current_hgen_job.run()
            if res.status != Status.SUCCESS:
                raise Exception(res.body)
            current_hgen_job = self.get_next_hgen_job(current_hgen_job, next_target_type)
        return current_hgen_job.run().body

    @staticmethod
    def get_next_hgen_job(current_hgen_job: BaseHGenJob, next_target_type: str) -> BaseHGenJob:
        """
        Gets the next hgen job to progress up the hierarchy
        :param current_hgen_job: The last hgen job that run
        :param next_target_type: The next target type to create with the new hgen job
        :return: The next hgen job
        """
        current_args = current_hgen_job.get_hgen_args()
        current_state: HGenState = current_hgen_job.hgen.state
        generated_dataset = current_state.final_dataset
        project_summary = generated_dataset.project_summary
        if project_summary:
            project_summary.combine_summaries(current_state.all_artifacts_dataset.project_summary)
        export_dir = os.path.dirname(current_state.export_dir)
        new_params = DataclassUtil.convert_to_dict(current_args,
                                                   source_layer_ids=current_args.target_type,
                                                   export_dir=export_dir,
                                                   source_type=current_args.target_type,
                                                   target_type=next_target_type,
                                                   dataset=generated_dataset,
                                                   dataset_creator=None,
                                                   optimize_with_reruns=False,
                                                   load_dir=EMPTY_STRING)
        DictUtil.get_kwarg_values(new_params, reduction_percentage=None, pop=True)
        init_params = ParamSpecs.create_from_method(HGenArgs.__init__).param_names
        new_params = {name: new_params[name] for name in init_params if name in new_params}
        next_job = BaseHGenJob(HGenArgs(**new_params), current_hgen_job.job_args)
        next_job.result.experimental_vars = {"target_type": next_target_type}
        return next_job
