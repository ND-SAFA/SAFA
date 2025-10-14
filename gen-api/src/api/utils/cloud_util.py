import json
import os

import boto3

from gen_common.infra.t_logging.logger_manager import logger
from gen_common.util.json_util import NpEncoder


class CloudUtility:
    """
    Contains utility methods for dealing with cloud storage.
    """

    @staticmethod
    def save_json(content_dict: dict, file_path: str) -> None:
        """
        Saves JSON to file path.
        :param content_dict: The JSON content.
        :param file_path: Path in default bucket to save content to.
        :return: None.
        """
        AWS_ACCESS_KEY_ID = os.environ["BACKEND_ACCESS_ID"]
        AWS_SECRET_ACCESS_KEY = os.environ["BACKEND_SECRET_KEY"]
        BUCKET_NAME = os.environ["BACKEND_BUCKET_NAME"]
        session = boto3.Session(
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )
        s3 = session.client('s3')
        # Upload the string content to the specified file path in the bucket
        try:
            content = json.dumps(content_dict, indent=4, cls=NpEncoder)
            s3.put_object(Body=content, Bucket=BUCKET_NAME, Key=file_path)
            logger.info(f"Created file: {BUCKET_NAME}/{file_path}")
        except Exception as e:
            logger.info(f"An error occurred while saving the string content: {e}")
