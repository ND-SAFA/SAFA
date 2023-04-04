import os

from google.cloud import storage

from cloud.icloud_storage import ICloudStorage


class GcpCloudStorage(ICloudStorage):
    """
    Implements the storage solution for GCP.
    """

    @classmethod
    def exists(cls, path: str, bucket_name: str) -> bool:
        """
        Returns if path exists within bucket.
        :param path: The path to check if blob exists.
        :param bucket_name: The bucket to search within.
        :return: True if blob exists at path.
        """
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        return storage.Blob(bucket=bucket, name=path).exists(storage_client)

    @classmethod
    def copy(cls, src: str, dest: str, bucket_name: str = None) -> None:
        """
        Copies folder to destination.
        :param src: Path to source folder in bucket.
        :param dest: Path to local machine.
        :param bucket_name: The name of the bucket to search within.
        :return: None. Error thrown if failure occurs.
        """

        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name=bucket_name)
        source_blob = bucket.blob(src)
        blobs = source_blob.list_blobs()
        for blob in blobs:
            file_name = blob.name
            blob.download_to_filename(os.path.join(dest, file_name))
