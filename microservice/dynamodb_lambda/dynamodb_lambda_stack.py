from aws_cdk import (
    aws_lambda,
    aws_dynamodb,
    aws_events,
    aws_events_targets,
    Duration, Stack
)
from constructs import Construct

class DynamodbLambdaStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # create dynamo table
        demo_table = aws_dynamodb.Table(
            self, "user_info",
            partition_key=aws_dynamodb.Attribute(
                name="id",
                type=aws_dynamodb.AttributeType.STRING
            ),
            sort_key=aws_dynamodb.Attribute(
                name="username",
                type=aws_dynamodb.AttributeType.STRING
            ),
        )

        # create producer lambda function
        producer_lambda = aws_lambda.Function(self, "write_to_dynamodb_lambda_function",
                                              runtime=aws_lambda.Runtime.PYTHON_3_11,
                                              handler="lambda_function.lambda_handler",
                                              code=aws_lambda.Code.from_asset("./lambda/producer"))

        producer_lambda.add_environment("TABLE_NAME", demo_table.table_name)

        # grant permission to lambda to write to demo table
        demo_table.grant_write_data(producer_lambda)

        # create consumer lambda function
        consumer_lambda = aws_lambda.Function(self, "check_duplicate_username_lambda_function",
                                              runtime=aws_lambda.Runtime.PYTHON_3_11,
                                              handler="lambda_function.lambda_handler",
                                              code=aws_lambda.Code.from_asset("./lambda/consumer"))

        consumer_lambda.add_environment("TABLE_NAME", demo_table.table_name)

        # grant permission to lambda to read from demo table
        demo_table.grant_read_data(consumer_lambda)

        # grant permission to lambda to write to demo table
        demo_table.grant_write_data(producer_lambda)

        # create query lambda function
        query_lambda = aws_lambda.Function(self, "check_login_lambda_function",
                                              runtime=aws_lambda.Runtime.PYTHON_3_11,
                                              handler="lambda_function.lambda_handler",
                                              code=aws_lambda.Code.from_asset("./lambda/query"))

        query_lambda.add_environment("TABLE_NAME", demo_table.table_name)

        # grant permission to lambda to read from demo table
        demo_table.grant_read_data(query_lambda)
