from constructs import Construct
from aws_cdk import (
    Stack,
    aws_lambda as lambda_,
    aws_apigateway as apigateway,
    aws_s3 as s3,
    aws_s3_deployment as s3_deployment,
)


class WorkforcePlanningInfraStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        handler = lambda_.Function(
            self,
            "WorkforcePlanningInfraFunction",
            runtime=lambda_.Runtime.PYTHON_3_7,
            code=lambda_.Code.from_asset("lambda"),
            handler="lambda_handler.handler",
        )

        apigateway.LambdaRestApi(
            self,
            "WorkforcePlanningInfraApi",
            handler=handler,
            deploy=True,
            default_cors_preflight_options=apigateway.CorsOptions(
                allow_origins=apigateway.Cors.ALL_ORIGINS,
                allow_methods=apigateway.Cors.ALL_METHODS,
                allow_headers=["*"],
            ),
        )

        bucket = s3.Bucket(
            self,
            "WorkforcePlanningInfraBucket",
            bucket_name="workforce-planning-infra-bucket",
            public_read_access=True,
            block_public_access=s3.BlockPublicAccess(
                block_public_acls=False,
                block_public_policy=False,
                ignore_public_acls=False,
                restrict_public_buckets=False,
            ),
            access_control=s3.BucketAccessControl.BUCKET_OWNER_FULL_CONTROL,
            website_index_document="index.html",
        )

        s3_deployment.BucketDeployment(
            self,
            "StaticWebsite",
            sources=[s3_deployment.Source.asset("./react-ts/dist")],
            destination_bucket=bucket,
        )
