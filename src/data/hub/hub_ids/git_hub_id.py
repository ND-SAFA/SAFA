from data.hub.hub_ids.multi_task_hub_id import MultiStageHubId


class GitHubId(MultiStageHubId):
    """
    Identifies the dataset containing slice of git links from Jinfeng's crawl.
    """

    def get_url(self) -> str:
        """
        :return: Returns URL to hub dataset.
        """
        return "https://safa-datasets-open.s3.amazonaws.com/datasets/open-source/git.zip"
