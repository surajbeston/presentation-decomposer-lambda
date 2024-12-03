from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    aws_lambda as lambda_,
    aws_apigateway as apigw,
)


class PresentationDecomposerLambdaStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create Lambda function from Docker container
        decomposer_lambda = lambda_.DockerImageFunction(
            self, "PresentationDecomposerLambda",
            code=lambda_.DockerImageCode.from_image_asset("presentation_decomposer_lambda/decomposer"),
            timeout=Duration.minutes(5),
            memory_size=8000,
            environment={
                "S3_ACCESS_KEY": "bed6c1f5cc02c9fe3ea7be791865fcbd",
                "S3_SECRET_KEY": "257a4eb75fc508395084dd522335885e97dedeae82f083f5027a9e6034dc2137",
                "CLOUDFLARE_API_TOKEN": "0qNnxn5gAzH1x7qX9iTueqqLmRLQkfQz-3JGorRA",
                "S3_BUCKET_URL": "https://66f903215ee11cb820883e93cff8c6d6.r2.cloudflarestorage.com",
                "S3_BUCKET_NAME": "present-for-me",
                "PUBLIC_DOMAIN_URL": "https://pub-ae5a83dfee0146d886142453235c2605.r2.dev/"
            }
        )

        # Create API Gateway
        api = apigw.LambdaRestApi(
            self, "PresentationDecomposerAPI",
            handler=decomposer_lambda,
            default_cors_preflight_options={
                "allow_origins": apigw.Cors.ALL_ORIGINS,
                "allow_methods": apigw.Cors.ALL_METHODS,
                "allow_headers": ["Content-Type", "X-Amz-Date", "Authorization", "X-Api-Key"]
            }
        )
