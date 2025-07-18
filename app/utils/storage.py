import boto3
from botocore.config import Config

from const.const import MINIO_LOGIN, MINIO_PASSWORD, MINIO_CONTAINER_URL

s3_client = boto3.client(
    "s3",
    endpoint_url=MINIO_CONTAINER_URL,
    aws_access_key_id=MINIO_LOGIN,
    aws_secret_access_key=MINIO_PASSWORD,
    config=Config(signature_version="s3v4"),
    region_name="us-east-1",
)

async def upload_object(bucket: str, key:str ,body: bytes, content_type: str):
    s3_client.put_object(Bucket=bucket, Key=key, Body=body, ContentType=content_type)


async def delete_object(bucket: str, key: str):
    try:
        s3_client.head_object(Bucket=bucket, Key=key)

        s3_client.delete_object(Bucket=bucket, Key=key)
        return {
            "success": True,
            "status": f"deleted",
        }
    except s3_client.exceptions.ClientError as _:
        return {
            "success": False,
            "status": f"not found"
        }

async def list_objects_with_prefix(bucket: str, prefix: str):
    response = s3_client.list_objects_v2(
        Bucket=bucket,
        Prefix=prefix
    )

    contents = response.get("Contents", [])
    return [obj["Key"] for obj in contents]