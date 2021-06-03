#  Author : Avinash Dalvi
#
# This script allows you to search file in S3 bucket.

import boto3

client = boto3.client("s3")
bucket_name = "shreedattatechnosolutions"
prefix = ""

s3 = boto3.client("s3")
# all_objects = s3.list_objects(Bucket = bucket_name)
# print(all_objects)

# result = client.list_objects(Bucket=bucket_name, Delimiter='/')
# for obj in result.get('CommonPrefixes'):
prefix = obj.get("Prefix")
file_list = ListFiles(client, bucket_name, prefix)
for file in file_list:
    if "processed/files" in file:
        print("Found", file)

result = s3.list_objects(Bucket=bucket_name, Prefix="", Delimiter="")
contents = result.get("Contents")
for content in contents:
    if "processed/files/" in content.get("Key"):
        print("Do the process")


def ListFiles(client, bucket_name, prefix):
    _BUCKET_NAME = bucket_name
    _PREFIX = prefix
    """List files in specific S3 URL"""
    response = client.list_objects(Bucket=_BUCKET_NAME, Prefix=_PREFIX)

    for content in response.get("Contents", []):
        print(content)
        yield content.get("Key")
