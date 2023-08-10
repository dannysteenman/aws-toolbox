#  https://github.com/dannysteenman/aws-toolbox
#
#  License: MIT
#
# This script searches for a single keys/object in an S3 bucket and let's you know wether it exists or not
#
# Usage: python search_key_bucket.py

import boto3
import botocore


def key_exists(bucket, key):
    s3 = boto3.client("s3")
    try:
        s3.head_object(Bucket=bucket, Key=key)
        print(f"Key: '{key}' found!")
    except botocore.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "404":
            print(f"Key: '{key}' does not exist!")
        else:
            print("Something else went wrong")
            raise


bucket = "my-bucket"
key = "path/to/my-file.txt"

key_exists(bucket, key)
