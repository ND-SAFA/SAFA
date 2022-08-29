from google.cloud import storage


class GCPCloudStorage:
    @staticmethod
    def upload_file(content: str,
                    destination_blob_name,
                    bucket_name: str = "safa-tgen-models",
                    content_type: str = "application/json"):
        """
        Uploads file to bucket.
        :param content: Content of the file to write to.
        :param destination_blob_name: Path in storage to write to.
        :param bucket_name: Name of bucket storing file
        :param content_type: Type of content written to file.
        """
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_string(content, content_type=content_type)

        print(f"File uploaded to {destination_blob_name}.")
