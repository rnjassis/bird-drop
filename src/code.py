import json
import boto3

ssm = boto3.client('ssm', region_name='sa-east-1')
s3 = boto3.client('s3')

def handler(event, context):
    bucketName = ssm.get_parameters(Names=["bird-drop/s3"])
    with open('filename', 'wb') as data:
        s3.download_fileobj(bucketName, 'exemplo.txt', data)
    
    return ""
