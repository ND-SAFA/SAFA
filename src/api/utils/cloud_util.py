import json
import os

import boto3

from tgen.util.json_util import NpEncoder
from tgen.util.logging.logger_manager import logger


class CloudUtility:
    """
    Contains utility methods for dealing with cloud storage.
    """

    @staticmethod
    def save_json(content_dict: dict, file_path: str):
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
