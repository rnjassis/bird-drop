import json
import boto3

ssm = boto3.client('ssm', region_name='sa-east-1')
s3 = boto3.resource('s3')

def handler(event, context):
    bucketParam = ssm.get_parameter(Name="/bird-drop/s3", WithDecryption=False)
    bucketName = bucketParam["Parameter"]["Value"]
    s3Bucket = s3.Bucket(bucketName)
    for s3Object in s3Bucket.objects.all():
        print(s3Object)
    return ""
