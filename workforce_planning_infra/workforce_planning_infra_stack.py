from constructs import Construct
import os
import subprocess
from aws_cdk.aws_lambda import Architecture
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    aws_s3 as s3,
    aws_s3_deployment as s3_deployment,
    aws_lambda_python_alpha as lambda_python,
)


class WorkforcePlanningInfraStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        entrypoint_name = "lambda"

        handler = lambda_python.PythonFunction(
            self,
            "WorkforcePlanningInfraFunction",
            entry="./lambda",
            runtime=_lambda.Runtime.PYTHON_3_12,
            index="lambda_handler.py",
            handler="handler",
            architecture=Architecture.X86_64,
        )

        # handler = _lambda.Function(
        #     self,
        #     "WorkforcePlanningInfraFunction",
        #     runtime=_lambda.Runtime.PYTHON_3_9,
        #     code=_lambda.Code.from_asset("lambda"),
        #     handler="lambda_handler.handler",
        #     layers=[self.create_dependencies_layer(self.stack_name, entrypoint_name)],
        # )

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
            disable_execute_api_endpoint=False,  # remove when ready to test
        )

        bucket = s3.Bucket(
            self,
            "WorkforcePlanningInfraBucket",
            bucket_name="workforce-planning-infra-bucket",
            # public_read_access=True,
            # block_public_access=s3.BlockPublicAccess(
            #     block_public_acls=False,
            #     block_public_policy=False,
            #     ignore_public_acls=False,
            #     restrict_public_buckets=False,
            # ),
            access_control=s3.BucketAccessControl.BUCKET_OWNER_FULL_CONTROL,
            website_index_document="index.html",
        )

        s3_deployment.BucketDeployment(
            self,
            "StaticWebsite",
            sources=[s3_deployment.Source.asset("./react-ts/dist")],
            destination_bucket=bucket,
        )

    def create_dependencies_layer(
        self, project_name, function_name: str
    ) -> _lambda.LayerVersion:
        requirements_file = "./lambda/requirements.txt"
        # output_dir = f"./.build/{function_name}/python/lib/python3.9/site-packages"
        output_dir = f"./.build/{function_name}/python"

        if not os.environ.get("SKIP_PIP"):
            subprocess.check_call(
                f"pip install -r {requirements_file} -t {output_dir}".split()
            )

        layer_id = f"{project_name}-{function_name}-dependencies"
        layer_code = _lambda.Code.from_asset(output_dir)

        return _lambda.LayerVersion(self, layer_id, code=layer_code)
