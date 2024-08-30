from io import BytesIO
import hashlib
import os
import boto3
from good_guard import endpoint_url_bucket, region_bucket, access_key_bucket, secret_access_key_bucket, bucket_name
from botocore.client import Config

s3 = boto3.client(
  's3',
  endpoint_url=endpoint_url_bucket,
  region_name=region_bucket,
  aws_access_key_id=access_key_bucket,
  aws_secret_access_key=secret_access_key_bucket,
  config=Config(signature_version='s3v4')
)

async def upload_avatar(file_content: bytes, file_key: str) -> str:
    try:
      # Загрузка файла на S3
      file = BytesIO(file_content)
      s3.upload_fileobj(file, bucket_name, file_key)
    except Exception as e:
      print(e)
      raise
  
async def delete_avatar(file_key: str) -> None:
  try:
    s3.delete_object(Bucket=bucket_name, Key=file_key)
  except Exception as e:
    print(e)
    
def get_s3_file_etag(avatar_url: str) -> str:
  object_key = avatar_url.replace(f"{endpoint_url_bucket}/{bucket_name}/", "")
  response = s3.head_object(Bucket=bucket_name, Key=object_key)
  return response['ETag'].strip('"')