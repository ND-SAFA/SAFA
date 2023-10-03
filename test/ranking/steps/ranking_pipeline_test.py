from typing import Dict, List

from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.testres.test_data_manager import TestDataManager
from tgen.tracing.ranking.ranking_args import RankingArgs
from tgen.tracing.ranking.ranking_state import RankingState


class RankingPipelineTest:
    @staticmethod
    def create_ranking_structures(parent_ids: List[str] = None, children_ids: List[str] = None, state_kwargs: Dict = None, **kwargs):
        """
        Creates the args and state of a ranking pipeline.
        :param parent_ids: The parent ids to perform ranking for.
        :param children_ids: The children to rank children against.
        :param kwargs: Custom keyword arguments to ranking args.
        :return: Ranking args and state.
        """
        if parent_ids is None:
            parent_ids = []
        if children_ids is None:
            children_ids = []
        if state_kwargs is None:
            state_kwargs = {}
        project_reader = TestDataManager.get_project_reader()
        artifact_df, _, _ = project_reader.read_project()
        project_summary = kwargs.pop("project_summary")  if "project_summary" in kwargs else None

        args = RankingArgs(dataset=PromptDataset(artifact_df=artifact_df, project_summary=project_summary),
                           parent_ids=parent_ids, children_ids=children_ids, **kwargs)
        state = RankingState(**state_kwargs)
        return args, state
