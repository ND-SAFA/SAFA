import os

from dotenv import load_dotenv

from data.github.github_constants import ARTIFACT_PATH, CLONE_PATH, SAFA_PATH

load_dotenv()


class GithubConfiguration:
    """
    Represents configuration for scraping github projects.
    """

    def __init__(self):
        self.token = os.environ.get("GITHUB_KEY")
        self.data_path = CLONE_PATH
        self.output_path = ARTIFACT_PATH
        self.final_path = SAFA_PATH
        self.projects = ['Autonomous-Racing-PG/ar-tu-do', 'ndrplz/self-driving-car']

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(GithubConfiguration, cls).__new__(cls)
        return cls.instance
