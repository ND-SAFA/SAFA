import os
import os.path

from api.endpoints.gen.serializers import ArtifactSerializer
from apiTests.base_test import BaseTest
from tgen.common.logging.logger_manager import logger
from tgen.common.util.json_util import JsonUtil


class ProjectTest(BaseTest):
    def test_project(self):
        run(os.path.expanduser("~/desktop/linux/Code.json"))


def to_artifact(artifact_json):
    return {
        "id": artifact_json["name"],
        "content": artifact_json["body"],
        "summary": artifact_json["summary"],
        "layer_id": "Code"
    }


def run(artifact_file: str):
    artifact_file_content = JsonUtil.read_json_file(artifact_file)
    artifacts = artifact_file_content["artifacts"]
    for artifact_json in artifacts:
        artifact = to_artifact(artifact_json)
        serializer = ArtifactSerializer(data=artifact)
        serializer.is_valid(raise_exception=False)
        if len(serializer.errors) > 0:
            logger.info(f"Failed to parse {artifact_json['name']}")
            for error in serializer.errors:
                logger.info(error)
            return
