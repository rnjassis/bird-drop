import json
import boto3

ssm = boto3.client('ssm', region_name='sa-east-1')
s3Client = boto3.client("s3")

def handler(event, context):
    folderLocation = getFolderFromSQS(event["Records"])
    bucketParam = ssm.get_parameter(Name="/bird-drop/s3", WithDecryption=False)
    bucketName = bucketParam["Parameter"]["Value"]
    
    pagination = s3Client.get_paginator("list_objects_v2")
    print(pagination)
    for page in pagination.paginate(Bucket=bucketName):
        for object in page['Contents']:
            print(object['Key'])

def getFolderFromSQS(records):
    for record in records:
        body = json.loads(record["body"])
        return body["location"]

