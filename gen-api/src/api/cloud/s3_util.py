import os

import boto3

from gen_common.infra.t_logging.logger_manager import logger


def upload_to_s3(input_file_path: str, cloud_path: str) -> None:
    """
    Uploads file to S3 bucket.
    :param input_file_path: Path to file to upload.
    :param cloud_path: Path in bucket to upload to.
    :return: None
    """
    logger.warning("S3 is not longer available.")
