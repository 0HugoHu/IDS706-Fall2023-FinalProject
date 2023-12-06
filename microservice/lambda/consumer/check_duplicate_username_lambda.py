from __future__ import print_function

import json
import os
import boto3
from botocore.exceptions import ClientError

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

# set environment variable
TABLE_NAME = os.environ['TABLE_NAME']

def lambda_handler(event, context):
    table = dynamodb.Table(TABLE_NAME)
    username = event['username']

    try:
      username = event['username']

      # Perform the query to check if the username exists
      response = table.scan(
        FilterExpression='username = :val',
        ExpressionAttributeValues={':val': username}
      )

      if response.get('Items'):
        print("Duplicate username")
        return {
          'statusCode': 200,
          'body': json.dumps({'duplicate': True})
        }
      else:
        print("Username is unique")
        return {
          'statusCode': 200,
          'body': json.dumps({'duplicate': False})
        }

    except ClientError as e:
      return {
        'statusCode': 500,
        'body': json.dumps(str(e))
      }
