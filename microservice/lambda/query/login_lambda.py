from __future__ import print_function

import json
import decimal
import os
import boto3
from botocore.exceptions import ClientError

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

# set environment variable
TABLE_NAME = os.environ['TABLE_NAME']


def lambda_handler(event, context):
    table = dynamodb.Table(TABLE_NAME)

    try:
      username = event['username']
      password = event['password']

      # Perform the scan to check if the username and password match
      response = table.scan(
        FilterExpression='username = :val',
        ExpressionAttributeValues={':val': username}
      )

      if response.get('Items') and response['Items'][0].get('password') == password:
        print("Login successful")
        return {
          'statusCode': 200,
          'body': json.dumps({'login_successful': True})
        }
      else:
        print("Login failed")
        return {
          'statusCode': 200,
          'body': json.dumps({'login_successful': False})
        }

    except ClientError as e:
      return {
        'statusCode': 500,
        'body': json.dumps(str(e))
      }
