import os
import boto3
from io import BytesIO

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_REGION_NAME = os.environ.get("AWS_REGION_NAME")
AWS_BUCKET_NAME = os.environ.get("AWS_BUCKET_NAME")


def upload(bytes_file, s3_file_name):
    bucket_name = AWS_BUCKET_NAME
    bytes_stream = BytesIO(bytes_file)
    try:
        s3 = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_REGION_NAME
        )
        s3.upload_fileobj(bytes_stream, bucket_name, s3_file_name)
        print(f"File uploaded successfully to {bucket_name}/{s3_file_name}")
        url = f"https://{bucket_name}.s3.amazonaws.com/{s3_file_name}"
        return url
    except Exception as e:
        print(f"An error occurred: {e}")
