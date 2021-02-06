import datetime
import json
import os
import uuid

import boto3
from botocore.exceptions import ClientError

from utils import apigateway_response

TABLE_NAME = os.environ["TABLE_NAME"]

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, context):
    event_body = json.loads(event["body"])
    
    make = event_body["make"]
    model = event_body["model"]
    category = event_body["category"]
    year = event_body["year"]

    now = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
    object_id = str(uuid.uuid4())
    item = {
        "object_id": object_id,
        "make": make,
        "model": model,
        "category": category,
        "year": year,
        "created_at": now,
        "updated_at": now
    }

    try:
        table.put_item(Item=item)
        return apigateway_response({"success": True, "item": item})
    except ClientError as e:
        return apigateway_response({"success": False, "message": e.response['Error']['Message']}, 500)
