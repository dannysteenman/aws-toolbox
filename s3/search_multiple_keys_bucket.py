#  https://github.com/dannysteenman/aws-toolbox
#
#  License: MIT
#
# This script searches for multiple keys/objects in an S3 bucket and let's you know wether it exists or not
#
# Usage: python search_multiple_keys_bucket.py

import boto3


def check_keys_exist(bucket, keys_to_check):
    s3 = boto3.client("s3")
    response = s3.list_objects_v2(Bucket=bucket)

    if "Contents" in response:
        existing_keys = {item["Key"] for item in response["Contents"]}
        return {key: key in existing_keys for key in keys_to_check}
    else:
        return {key: False for key in keys_to_check}


bucket = "my-bucket"
keys_to_check = ["path/to/file1.txt", "path/to/file2.txt", "path/to/file3.txt"]

result = check_keys_exist(bucket, keys_to_check)

for key, exists in result.items():
    print(f"Key {key} exists: {exists}")
