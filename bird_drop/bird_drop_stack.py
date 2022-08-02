from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_lambda as lambda_,
    aws_iam as iam,
    aws_ssm as ssm
)
from constructs import Construct

class BirdDropStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Bucket
        bucket = s3.Bucket(self, "BucketFromCDK-rnjassis")

        # Bucket name as param on Parameter Store
        paramS3 = ssm.StringParameter(self,
                "bucket-s3", 
                parameter_name="/bird-drop/s3",
                string_value=bucket.bucket_arn
                )

        s3Policy = iam.PolicyStatement(
                actions=["s3:GetObject", "s3:PutObject"],
                resources=[bucket.bucket_arn]
                )

        stsPolicy = iam.PolicyStatement(
                actions=["ssm:GetParametersByPath","ssm:GetParameters"],
                resources=[paramS3.parameter_arn]
                )

        lambdaFunction = lambda_.Function(self, "BirdDropFunction",
                runtime=lambda_.Runtime.PYTHON_3_8,
                code=lambda_.Code.from_asset('src'),
                handler='code.handler',
                initial_policy=[s3Policy, stsPolicy]
                )
