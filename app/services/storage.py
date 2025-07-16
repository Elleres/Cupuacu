import os

import boto3
from botocore.config import Config


MINIO_URL = os.getenv('MINIO_URL')
MINIO_LOGIN = os.getenv('MINIO_LOGIN')
MINIO_PASSWORD = os.getenv('MINIO_PASSWORD')


s3_client = boto3.client(
    "s3",
    endpoint_url="http://minio:9000",
    aws_access_key_id=MINIO_LOGIN,
    aws_secret_access_key=MINIO_PASSWORD,
    config=Config(signature_version="s3v4"),
    region_name="us-east-1",
)

async def upload_object(bucket: str, key:str ,body: bytes, content_type: str):
    s3_client.put_object(Bucket=bucket, Key=key, Body=body, ContentType=content_type)


async def delete_object(bucket: str, key: str):
        s3_client.delete_object(Bucket=bucket, Key=key)
