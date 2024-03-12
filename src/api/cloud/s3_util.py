import os

import boto3

from tgen.common.logging.logger_manager import logger


def upload_to_s3(input_file_path: str, cloud_path: str) -> None:
    """
    Uploads file to S3 bucket.
    :param input_file_path: Path to file to upload.
    :param cloud_path: Path in bucket to upload to.
    :return: None
    """
    aws_access_key_id = os.environ["BACKEND_ACCESS_ID"]
    aws_secret_access_key = os.environ["BACKEND_SECRET_KEY"]
    s3_bucket_name = os.environ["BACKEND_BUCKET_NAME"]

    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )
    s3 = session.client('s3')
    s3.upload_file(input_file_path, s3_bucket_name, cloud_path)
    logger.info(f"Successfully uploaded file to: {cloud_path}")
