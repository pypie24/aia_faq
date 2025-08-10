from abc import ABC, abstractmethod

from minio import Minio

from src.config import get_settings


class FileClient(ABC):
    @abstractmethod
    def upload_file(self, file_path: str, bucket_name: str, object_name: str):
        pass

    @abstractmethod
    def download_file(self, bucket_name: str, object_name: str, file_path: str):
        raise NotImplementedError("This method should be implemented by subclasses.")

    @abstractmethod
    def remove_file(self, bucket_name: str, object_name: str):
        raise NotImplementedError("This method should be implemented by subclasses.")

    @abstractmethod
    def list_files(self, bucket_name: str):
        raise NotImplementedError("This method should be implemented by subclasses.")

    @abstractmethod
    def create_folder(self, folder_name: str):
        raise NotImplementedError("This method should be implemented by subclasses.")

    @abstractmethod
    def remove_folder(self, folder_name: str):
        raise NotImplementedError("This method should be implemented by subclasses.")

    @abstractmethod
    def is_folder_exists(self, folder_name: str):
        raise NotImplementedError("This method should be implemented by subclasses.")


class MinioClient(FileClient):
    def __init__(self):
        settings = get_settings()
        self.client = Minio(
            endpoint=settings.FILE_SERVER_ENDPOINT,
            access_key=settings.FILE_SERVER_ACCESS_KEY,
            secret_key=settings.FILE_SERVER_SECRET_KEY,
            secure=settings.FILE_SERVER_SECURE,
        )

    def upload_file(self, file_path: str, folder_name: str, object_name: str):
        if not self.is_folder_exists(folder_name):
            self.create_folder(folder_name)
        self.client.fput_object(folder_name, object_name, file_path)

    def download_file(self, folder_name: str, object_name: str, file_path: str):
        self.client.fget_object(folder_name, object_name, file_path)

    def remove_file(self, folder_name: str, object_name: str):
        self.client.remove_object(folder_name, object_name)

    def list_files(self, folder_name: str):
        return self.client.list_objects(folder_name)

    def create_folder(self, folder_name: str):
        self.client.make_bucket(folder_name)

    def remove_folder(self, folder_name: str):
        self.client.remove_bucket(folder_name)

    def is_folder_exists(self, folder_name: str):
        try:
            self.client.bucket_exists(bucket_name=folder_name)
            return True
        except Exception:
            return False


class FileService:
    def __init__(self, client: FileClient):
        self.client = client

    def save_image_to_bucket(self, bucket_name, object_name, image_data):
        self.client.upload_file(image_data, bucket_name, object_name)

    def get_image_from_bucket(self, bucket_name, object_name):
        return self.client.download_file(bucket_name, object_name)
