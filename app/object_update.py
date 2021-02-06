import datetime
import json
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
    updated_at = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()

    object_id = apigateway_get_object_id(event)

    #payload = json.loads(event["body"])

    key = {"object_id": object_id}
    expression = "set updated_at = :updated_at"
    values = {":updated_at": updated_at}

    try:
        item = table.update_item(
                Key=key,
                UpdateExpression=expression,
                ExpressionAttributeValues=values,
                ReturnValues="UPDATED_NEW",
        ).get("Attributes")
    
        return apigateway_response({"item": item})
    except:
        return apigateway_response({"success": False, "message": "Error updating object"}, 400)