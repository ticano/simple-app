import os
import boto3

from app.utils import (
    apigateway_response,
    apigateway_get_object_id,
)

TABLE_NAME = os.environ["TABLE_NAME"]

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, context):
    object_id = apigateway_get_object_id(event)

    key = {"object_id": object_id}

    try:
        item = table.get_item(Key=key)["Item"]
        return apigateway_response({"item": item})
    except:
        return apigateway_response({"success": False, "message": "Error getting object"}, 400)
