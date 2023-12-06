from __future__ import print_function

import json
import uuid
import os
import boto3
from botocore.exceptions import ClientError

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

# set environment variable
TABLE_NAME = os.environ['TABLE_NAME']


def lambda_handler(event, context):
  table = dynamodb.Table(TABLE_NAME)
  # put item in table
  try:
    username = event['username']
    password = event['password']

    # Perform the write operation to DynamoDB
    table.put_item(
      Item={
        'id': str(uuid.uuid4()),
        'username': username,
        'password': password
      }
    )

    print("Add user succeeded:")
    return {
      'statusCode': 200,
    }

  except ClientError as e:
    return {
      'statusCode': 500,
      'body': json.dumps(str(e))
    }
