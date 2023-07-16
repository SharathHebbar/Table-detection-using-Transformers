from pathlib import Path
from minio import Minio
from minio.error import (ResponseError, BucketAlreadyOwnedByYou,
                         BucketAlreadyExists)
class MINIO():
    def __init__(self, HOST, ACCESS_KEY, MINIO_KEY, BUCKET_NAME, UID, op):
        self.minioClient = Minio(HOST,
                        access_key=ACCESS_KEY,
                        secret_key=MINIO_KEY,
                        secure=False)
        self.BUCKET_NAME = BUCKET_NAME
        self.UID = UID
        self.op = op
    
    def upload_to_minio(self):
        try:
            self.minioClient.make_bucket(self.BUCKET_NAME, location="us-east-1")
        except BucketAlreadyOwnedByYou as err:
            pass
        except BucketAlreadyExists as err:
            pass
        except ResponseError as err:
            raise

        # Put an object 'A' with contents from 'B'.
        try:
            self.minioClient.fput_object(self.BUCKET_NAME, str(self.UID) + '/' + Path(self.op).name, self.op)
        except ResponseError as err:
            print(err)
    

    def download_from_minio(self):
        val = self.minioClient.fget_object(self.BUCKET_NAME, Path(self.op).name, str(self.UID) + '/' + Path(self.op).name)
        return val.object_name


