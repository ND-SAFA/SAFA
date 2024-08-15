import os.path
import subprocess
from typing import Any, List

import boto3
from common_resources.tools.cli.confirm import confirm
from common_resources.tools.util.file_util import FileUtil

from tgen.scripts.constants import DATA_PATH, DEFAULT_CONFIG_PATH, DEFAULT_DATA_BUCKET, IGNORE_FILES

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


def upload_folder(folder_path: str, bucket_path: str = None, bucket_name: str = DEFAULT_DATA_BUCKET,
                  show_files: bool = True):
    """
    Uploads folder to bucket.
    :param folder_path: Path to folder to upload.
    :param bucket_path: The name of the folder to store data in bucket. Default uses input folder name.
    :param bucket_name: The bucket to upload to.
    :param show_files: Whether to display files before copying to bucket.
    :return: None
    """
    folder_path = os.path.expanduser(folder_path)
    if bucket_path is None:
        bucket_path = os.path.basename(folder_path)
    if not os.path.isdir(folder_path):
        print(f"Cannot find folder at path: {folder_path}")
        return

    files_to_upload = get_copyable_files(folder_path)
    confirm_message = f"Copy {len(files_to_upload)} files to {bucket_path}?"
    if show_files:
        display_items(files_to_upload, "Files")
    if not confirm(confirm_message):
        return

    for file_path in files_to_upload:
        relative_path = os.path.relpath(file_path, start=folder_path)
        command = f"aws s3 cp {file_path} s3://{bucket_name}/{bucket_path}/{relative_path}"
        cmd(command)


def ls_bucket_files(bucket_name: str = DEFAULT_DATA_BUCKET, starting_path: str = ""):
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
    dir_path = os.path.dirname(folder_path)


def download_folder(s3_folder: str, store_path: str = DATA_PATH, bucket_name: str = DEFAULT_DATA_BUCKET):
    """
    Download the contents of a folder directory.
    :param s3_folder: The folder path in the s3 bucket.
    :param store_path: Path to store data on local machine.
    :param bucket_name: The name of the s3 bucket.
    :return: None
    """
    store_path = os.path.expanduser(store_path)
    bucket = s3.Bucket(bucket_name)

    saved_files = []
    for obj in bucket.objects.filter(Prefix=s3_folder):
        target = os.path.join(store_path, obj.key)
        if not os.path.exists(os.path.dirname(target)):
            os.makedirs(os.path.dirname(target))
        if obj.key[-1] == '/':  # checks if folder
            continue
        bucket.download_file(obj.key, target)
        saved_files.append(target)
    display_items(saved_files, "Files Downloaded")


"""
Private methods.
"""


def cmd(command: str):
    """
    Runs command.
    :param command: The string representing command to run.
    :return: Output of subprocess.
    """
    command_words = command.split()
    return subprocess.run(command_words)


def display_items(items: List[Any], header: str, relative_path: str = None, print_message: bool = True):
    """
    Displays the items in the list.
    :param items: The items to display.
    :param header: The header to display items under.
    :param relative_path: The path to display items from.
    :param print_message: Whether to print message.
    :return: The message containing all items.
    """
    HEADER_BAR = "-" * 25
    header_message = " ".join([HEADER_BAR, header, HEADER_BAR])
    messages = []
    for item in items:
        if relative_path:
            item_message = os.path.relpath(item, start=relative_path)
        else:
            item_message = repr(item)
        messages.append(item_message)

    if len(items) == 0:
        messages.append("No items to show.")

    message = "\n".join([header_message] + messages)
    if print_message:
        print(message)
    return message


def get_copyable_files(folder_path: str):
    """
    Gets list of file paths valid for copying to S3 bucket.
    :param folder_path: Path to folder to list files for.
    :return: List of copyable files.
    """
    files_to_upload = []
    for file_path in FileUtil.get_all_paths(folder_path):
        file_name = os.path.basename(file_path)
        if file_name[0] == "." or file_name in IGNORE_FILES or os.path.isdir(file_path):
            continue
        files_to_upload.append(file_path)
    return files_to_upload


S3_TOOLS = [upload_folder, download_folder, ls_bucket_files, delete_folder, ls_buckets, configure]
