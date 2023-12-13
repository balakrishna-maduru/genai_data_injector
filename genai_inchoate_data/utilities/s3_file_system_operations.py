import os
import boto3
from botocore.exceptions import NoCredentialsError
from boto3.s3.transfer import TransferConfig

class S3FileSystemOperations:
    
    def __init__(self, access_key, secret_key, bucket_name, endpoint_url=None):
        self.access_key = access_key
        self.secret_key = secret_key
        self.bucket_name = bucket_name
        self.endpoint_url = endpoint_url
        self.s3 = boto3.client('s3', aws_access_key_id=self.access_key, aws_secret_access_key=self.secret_key, endpoint_url=self.endpoint_url)

    def create_bucket(self, new_bucket_name):
        try:
            self.s3.create_bucket(Bucket=new_bucket_name)
            print(f"Bucket '{new_bucket_name}' created.")
        except self.s3.exceptions.BucketAlreadyExists:
            print(f"Bucket '{new_bucket_name}' already exists.")
        except NoCredentialsError:
            print("Credentials not available.")

    def delete_bucket(self, bucket_to_delete):
        try:
            self.s3.delete_bucket(Bucket=bucket_to_delete)
            print(f"Bucket '{bucket_to_delete}' deleted.")
        except self.s3.exceptions.NoSuchBucket:
            print(f"Bucket '{bucket_to_delete}' does not exist.")
        except self.s3.exceptions.BucketNotEmpty:
            print(f"Bucket '{bucket_to_delete}' is not empty. Delete objects first.")
        except NoCredentialsError:
            print("Credentials not available.")

    def upload_file(self, local_file_path, s3_key):
        try:
            self.s3.upload_file(local_file_path, self.bucket_name, s3_key)
            print(f"File {local_file_path} uploaded to {self.bucket_name}/{s3_key}")
        except FileNotFoundError:
            print(f"The file {local_file_path} was not found.")
        except NoCredentialsError:
            print("Credentials not available.")

    def download_file(self, s3_key, local_file_path):
        try:
            self.s3.download_file(self.bucket_name, s3_key, local_file_path)
            print(f"File downloaded from {self.bucket_name}/{s3_key} to {local_file_path}")
        except FileNotFoundError:
            print(f"The file {self.bucket_name}/{s3_key} was not found.")
        except NoCredentialsError:
            print("Credentials not available.")

    def upload_folder(self, local_folder_path, s3_prefix=''):
        try:
            transfer_config = TransferConfig(use_threads=True)
            self.s3.upload_file(local_folder_path, self.bucket_name, s3_prefix,
                                config=transfer_config, extra_args={'ACL': 'public-read'})
            print(f"Folder {local_folder_path} uploaded to {self.bucket_name}/{s3_prefix}")
        except FileNotFoundError:
            print(f"The folder {local_folder_path} was not found.")
        except NoCredentialsError:
            print("Credentials not available.")

    def download_folder(self, s3_prefix, local_folder_path):
        try:
            transfer_config = TransferConfig(use_threads=True)
            self.s3.download_file(self.bucket_name, s3_prefix, local_folder_path,
                                  config=transfer_config)
            print(f"Folder downloaded from {self.bucket_name}/{s3_prefix} to {local_folder_path}")
        except FileNotFoundError:
            print(f"The folder {self.bucket_name}/{s3_prefix} was not found.")
        except NoCredentialsError:
            print("Credentials not available.")

    def list_keys(self, prefix=None):
        try:
            params = {'Bucket': self.bucket_name}
            if prefix:
                params['Prefix'] = prefix

            response = self.s3.list_objects_v2(**params)
            keys = [obj['Key'] for obj in response.get('Contents', [])]
            
            if keys:
                print(f"Keys in {self.bucket_name} with prefix '{prefix}': {keys}")
            else:
                print(f"No keys found in {self.bucket_name} with prefix '{prefix}'")
                
            return keys
        except NoCredentialsError:
            print("Credentials not available.")

    def key_exists(self, s3_key):
        try:
            response = self.s3.head_object(Bucket=self.bucket_name, Key=s3_key)
            return True
        except self.s3.exceptions.NoSuchKey:
            return False
        except NoCredentialsError:
            print("Credentials not available.")

    def delete_object(self, s3_key):
        try:
            self.s3.delete_object(Bucket=self.bucket_name, Key=s3_key)
            print(f"Object {s3_key} deleted from {self.bucket_name}")
        except self.s3.exceptions.NoSuchKey:
            print(f"The object {s3_key} does not exist in {self.bucket_name}")
        except NoCredentialsError:
            print("Credentials not available.")

    def bucket_exists(self, bucket_name=None):
        try:
            response = self.s3.list_buckets()
            buckets = [bucket['Name'] for bucket in response['Buckets']]
            if bucket_name:
                return bucket_name in buckets
            else:
                return self.bucket_name in buckets
        except NoCredentialsError:
            print("Credentials not available.")

