from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_lambda as lambda_,
    aws_iam as iam
)
import aws_cdk.aws_apigatewayv2_alpha as apigwv2
from aws_cdk.aws_apigatewayv2_integrations_alpha import HttpLambdaIntegration


class RafaelpomboChatbotStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        endpoint = "rafaelpombo_chatbot"
        http_api = apigwv2.HttpApi(
            self,
            "positions-backend-micro",
            cors_preflight=apigwv2.CorsPreflightOptions(
                allow_headers=["Authorization"],
                allow_methods=[apigwv2.CorsHttpMethod.ANY],
                allow_origins=["*"],
                max_age=Duration.days(10),
            ),
        )
        lambda_function = lambda_.Function(
            self,
            f"{endpoint}EndpointLambda",
            handler="lambda_function.lambda_handler",
            runtime=lambda_.Runtime.PYTHON_3_11,
            code=lambda_.Code.from_asset(f"endpoints/{endpoint}.zip"),
            description=f"handles {endpoint} endpoint.",
            function_name=f"{endpoint}EndpointLambda",
        )
        lambda_function.add_to_role_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=["dynamodb:*"],
                resources=["*"],
            )
        )

        lambda_integration = HttpLambdaIntegration(
            f"{endpoint}Integration", lambda_function
        )
        http_api.add_routes(
            path=f"/{endpoint}",
            methods=[apigwv2.HttpMethod.ANY],
            integration=lambda_integration
        )

