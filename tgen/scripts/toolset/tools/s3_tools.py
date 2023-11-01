import os.path
import subprocess
from typing import Any, List

import boto3

from tgen.common.util.file_util import FileUtil
from tgen.common.util.list_util import ListUtil
from tgen.scripts.toolset.core.confirm import confirm
from tgen.scripts.toolset.core.constants import DEFAULT_CONFIG_PATH, DEFAULT_DATA_BUCKET, IGNORE_FILES

s3 = boto3.resource('s3')
N_PER_BATCH = 2


def configure():
    """
    Attempts to configure AWS for you.
    """
    if os.path.isfile(DEFAULT_CONFIG_PATH):
        print("AWS Configuration Found (file).")
    elif os.path.isdir(DEFAULT_CONFIG_PATH):
        print("AWS Configuration Found (dir).")
    else:
        print("Unable to find the aws configuration.")
        if confirm("Attempt to configure aws?"):
            a = "aws configure"
            cmd(a)
        else:
            print("Okay bye.")


def ls_buckets() -> None:
    """
    Prints out all bucket names.
    :return: None
    """
    bucket_names = [bucket.name for bucket in s3.buckets.all()]
    display_items(bucket_names, "Buckets")


def upload_folder(folder_path: str, bucket_name: str = DEFAULT_DATA_BUCKET, bucket_path: str = None, show_files: bool = True):
    """
    Uploads folder to bucket.
    :param folder_path: Path to folder to upload.
    :param bucket_name: The bucket to upload to.
    :param bucket_path: The name of the folder to store data in bucket. Default uses input folder name.
    :param show_files: Whether to display files before copying to bucket.
    :return: None
    """
    folder_path = os.path.expanduser(folder_path)
    if bucket_path is None:
        bucket_path = os.path.basename(folder_path)
    if not os.path.isdir(folder_path):
        print(f"Cannot find folder at path: {folder_path}")
        return
    files_to_upload = [f for f in FileUtil.ls_dir(folder_path) if f not in IGNORE_FILES]

    confirm_message = f"Copy {len(files_to_upload)} files?"
    if show_files:
        files_display = "\n".join(files_to_upload)
        confirm_message = files_display + confirm_message
    if not confirm(confirm_message):
        return

    for file_name in files_to_upload:
        file_path = os.path.join(folder_path, file_name)
        command = f"aws s3 cp {file_path} s3://{bucket_name}/{bucket_path}/{file_name}"
        cmd(command)


def ls_bucket(bucket_name: str = DEFAULT_DATA_BUCKET, starting_path: str = ""):
    """
    Lists all files in folder on bucket.
    :param bucket_name: The name of the bucket.
    :param starting_path: The path to list in bucket.
    :return: None
    """
    bucket = s3.Bucket(bucket_name)
    folder_items = [b.key for b in bucket.objects.filter(Prefix=starting_path)]
    display_items(folder_items, "Folder Items")


def delete_folder(folder_path: str, bucket_name: str = DEFAULT_DATA_BUCKET):
    """
    Deletes
    :param folder_path:
    :param bucket_name:
    :return:
    """
    bucket = s3.Bucket(bucket_name)
    bucket.objects.filter(Prefix=folder_path).delete()


def cmd(command: str):
    """
    Runs command.
    :param command: The string representing command to run.
    :return: Output of subprocess.
    """
    command_words = command.split()
    return subprocess.run(command_words)


def display_items(items: List[Any], header: str, n_per_batch: int = N_PER_BATCH):
    """
    Displays the items in the list.
    :param items: The items to display.
    :param header: The header to display items under.
    :param n_per_batch: The number of items per batch.
    :return: None
    """
    batches = ListUtil.batch(items, n_per_batch)
    HEADER_BAR = "-" * 25
    print(HEADER_BAR, header, HEADER_BAR)
    for batch in batches:
        print(repr(batch))


S3_TOOLS = [configure, ls_buckets, upload_folder, ls_bucket, delete_folder]
