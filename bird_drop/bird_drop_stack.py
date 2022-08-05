from aws_cdk import (
    Stack,
    Duration,
    aws_s3 as s3,
    aws_lambda as lambda_,
    aws_iam as iam,
    aws_ssm as ssm,
    aws_sqs as sqs,
    aws_lambda_event_sources as eventSource
)
from constructs import Construct


class BirdDropStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Bucket
        bucket = s3.Bucket(self,
                           "s3FromCDK",
                           bucket_name="s3fromcdk")

        # Bucket name as param on Parameter Store
        paramS3 = ssm.StringParameter(self,
                                      "bucket-s3",
                                      parameter_name="/bird-drop/s3",
                                      string_value=bucket.bucket_name
                                      )

        # S3 access policies
        s3PolicyReadWrite = iam.PolicyStatement(
            actions=["s3:GetObject", "s3:PutObject"],
            resources=[bucket.bucket_arn + "/*"]
        )

        s3PolicyListObjects = iam.PolicyStatement(
            actions=["s3:ListBucket"],
            resources=[bucket.bucket_arn]
        )

        # SSM access policies
        ssmPolicy = iam.PolicyStatement(
            actions=["ssm:GetParametersByPath", "ssm:GetParameters", "ssm:GetParameter"],
            resources=[paramS3.parameter_arn]
        )

        lambdaFunction = lambda_.Function(self, "BirdDropFunction",
                                          runtime=lambda_.Runtime.PYTHON_3_8,
                                          code=lambda_.Code.from_asset('src'),
                                          handler='code.handler',
                                          initial_policy=[s3PolicyReadWrite, s3PolicyListObjects, ssmPolicy],
                                          timeout=Duration.seconds(10),
                                          function_name="BirdDropFunctionCDK"
                                          )

        # SQS
        sqsQueue = sqs.Queue(self, "sqsFromCDK", queue_name="sqsFromCDK")

        # Event Source
        eSource = eventSource.SqsEventSource(sqsQueue)
        lambdaFunction.add_event_source(eSource)
