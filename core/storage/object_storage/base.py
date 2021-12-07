from abc import abstractmethod, ABC


class BaseS3Client(ABC):
    @abstractmethod
    async def __aenter__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError


class BaseS3Manager(ABC):
    @abstractmethod
    async def list_buckets(self):
        raise NotImplementedError

    @abstractmethod
    async def list_objects(self, bucket_name: str):
        raise NotImplementedError

    @abstractmethod
    async def put_object(self, bucket_name: str, object_name: str, bytes_object: bytes):
        raise NotImplementedError

    @abstractmethod
    async def get_object(self, bucket_name: str, object_name: str):
        raise NotImplementedError

    @abstractmethod
    async def create_bucket(self, bucket_name: str):
        raise NotImplementedError

    @abstractmethod
    async def delete_bucket(self, bucket_name: str, recursive: bool = False):
        raise NotImplementedError
