"""Class to handle Minio integration."""
from io import BytesIO

import boto3
import botocore

from src.conf.constants import MINIO_BUCKET_NAME, MINIO_ENDPOINT
from src.conf.core.basic_integration import DataIntegration
from src.conf.secrets import return_minio_secrets


class MinioIntegration(DataIntegration):
    """A class containing configuration for Minio related operations."""

    def __init__(self):
        super().__init__()
        self.__minio_secrets = return_minio_secrets()

        self.bucket_name = MINIO_BUCKET_NAME
        self.minio_client = boto3.client(
            "s3",
            endpoint_url=MINIO_ENDPOINT,
            aws_access_key_id=self.__minio_secrets["aws_access_key_id"],
            aws_secret_access_key=self.__minio_secrets["aws_secret_access_key"],
        )
        try:
            self.minio_client.head_bucket(Bucket=self.bucket_name)
        except botocore.exceptions.ClientError:
            self.minio_client.create_bucket(Bucket=self.bucket_name)

    def fetch_new_files(self) -> list:
        """Fetch the new files from Minio."""
        response = self.minio_client.list_objects_v2(Bucket=self.bucket_name)
        return [content["Key"] for content in response.get("Contents", [])]

    def read(self, file_key: str) -> str:
        """Read the data from Minio."""
        obj = self.minio_client.get_object(Bucket=self.bucket_name, Key=file_key)
        return obj["Body"].read().decode("utf-8")

    def write(self, csv_buffer: BytesIO, file_name: str) -> None:
        """Write the data to Minio."""
        self.minio_client.upload_fileobj(csv_buffer, self.bucket_name, file_name)
