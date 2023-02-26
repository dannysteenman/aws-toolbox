#  Author : Avinash Dalvi
#
# This script allows you to search subdirectory under nested folder structure.
#
# Reference question : https://stackoverflow.com/questions/62158664/search-in-each-of-the-s3-bucket-and-see-if-the-given-folder-exists/62160218#62160218


import boto3

client = boto3.client("s3")
bucket_name = "bucket_name"
prefix = ""

s3 = boto3.client("s3")

result = client.list_objects(Bucket=bucket_name, Delimiter="/")


def ListFiles(client, bucket_name, prefix):
    _BUCKET_NAME = bucket_name
    _PREFIX = prefix
    """List files in specific S3 URL"""
    response = client.list_objects(Bucket=_BUCKET_NAME, Prefix=_PREFIX)

    for content in response.get("Contents", []):
        # print(content)
        yield content.get("Key")


for obj in result.get("CommonPrefixes"):
    prefix = obj.get("Prefix")
    file_list = ListFiles(client, bucket_name, prefix)
    for file in file_list:
        if "processed/files" in file:
            print("Found", file)
