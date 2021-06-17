#  Author : Avinash Dalvi
#
# This script allows you to create tar file creation.
#
# Reference question : https://stackoverflow.com/questions/64341192/how-to-create-a-tar-file-containing-all-the-files-in-a-directory/64341789#64341789

import boto3
import tarfile
import os.path

s3Client = boto3.client("s3")
s3object = boto3.resource("s3")


def lambda_handler(event, context):
    agtBucket = "angularbuildbucket"
    key = ""
    tar = tarfile.open("/tmp/example.tar", "w")
    source_dir = "/tmp/"
    for fname in get_matching_s3_keys(bucket=agtBucket, prefix=key, suffix=".js"):
        print(fname)
        # file_obj = s3object.Object(agtBucket, fname)
        # file_content = file_obj.get()['Body'].read()
        # tar.add(file_content)
        s3object.Bucket(agtBucket).download_file(fname, "/tmp/" + fname)
        tar.add(source_dir, arcname=os.path.basename(source_dir))
    tar.close()
    s3object.meta.client.upload_file(
        source_dir + "example.tar", agtBucket, "example.tar"
    )


def get_matching_s3_keys(bucket, prefix="", suffix=""):
    """
    Generate the keys in an S3 bucket.

    :param bucket: Name of the S3 bucket.
    :param prefix: Only fetch keys that start with this prefix (optional).
    :param suffix: Only fetch keys that end with this suffix (optional).
    """
    kwargs = {"Bucket": bucket, "Prefix": prefix}
    while True:
        resp = s3Client.list_objects_v2(**kwargs)
        for obj in resp["Contents"]:
            key = obj["Key"]
            if key.endswith(suffix):
                yield key

        try:
            kwargs["ContinuationToken"] = resp["NextContinuationToken"]
        except KeyError:
            break


if __name__ == "__main__":
    lambda_handler({"invokingEvent": '{"messageType":"ScheduledNotification"}'}, None)
