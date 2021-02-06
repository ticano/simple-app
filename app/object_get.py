import os
import boto3
from botocore.exceptions import ClientError


from utils import (
    apigateway_response,
    apigateway_get_object_id
)

TABLE_NAME = os.environ["TABLE_NAME"]

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, context):
    object_id = apigateway_get_object_id(event)

    key = {"object_id": object_id}

    try:
        item = table.get_item(Key=key)
        if "Item" in item:
            return apigateway_response({"item": item["Item"]})
        else:
            return apigateway_response({"success": False, "message": "Item not found."}, 404)
    except ClientError as e:
        return apigateway_response({"success": False, "message": e.response['Error']['Message']}, 500)