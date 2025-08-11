from typing import Any
import boto3

from src.config import settings
from botocore.exceptions import ClientError


class ImageUploader:
    def __init__(self):
        self.bucket_name = settings.FILE_SERVER_BUCKET_NAME
        self.s3_client = boto3.client(
            "s3",
            endpoint_url=settings.FILE_SERVER_ENDPOINT,
            aws_access_key_id=settings.FILE_SERVER_ACCESS_KEY,
            aws_secret_access_key=settings.FILE_SERVER_SECRET_KEY,
            region_name="us-east-1",
        )

    def ensure_bucket(self) -> bool:
        """
        Checks if the S3 bucket exists.

        :return: True if the bucket exists, False otherwise.
        """
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
            return True
        except ClientError as e:
            self.s3_client.create_bucket(Bucket=self.bucket_name)
            return True

    def upload_image(self, object_data: Any, object_name: str = None) -> str:
        """
        Uploads an image to the S3 bucket.

        :param object_data: The data of the object to upload.
        :param object_name: S3 object name. If not specified, a unique name will be generated.
        :return: URL of the uploaded image.
        """
        self.ensure_bucket()
        try:
            self.s3.upload_fileobj(object_data, self.bucket_name, object_name)
        except ClientError as e:
            raise RuntimeError(f"Failed to upload image: {e}")
        return self.get_image_url(object_name)

    def get_image_url(self, object_name: str) -> str:
        """
        Gets the public URL of an image stored in the S3 bucket.

        :param object_name: S3 object name.
        :return: URL of the image.
        """
        return f"{settings.FILE_SERVER_ENDPOINT}/{self.bucket_name}/{object_name}"


image_uploader = ImageUploader()
