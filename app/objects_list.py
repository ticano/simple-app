import os
import boto3
from botocore.exceptions import ClientError

from utils import apigateway_response


TABLE_NAME = os.environ["TABLE_NAME"]

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, context):
    
    try:
        response = table.scan()
        items = response.get('Items', [])

        return apigateway_response({"items": items})
    except ClientError as e:
        return apigateway_response({"success": False, "message": e.response['Error']['Message']}, 500)

