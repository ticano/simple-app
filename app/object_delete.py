import os
import boto3
from botocore.exceptions import ClientError

from utils import (
    apigateway_response,
    apigateway_get_object_id,
)


BUCKET_NAME = os.environ["BUCKET_NAME"]
TABLE_NAME = os.environ["TABLE_NAME"]

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, context):
    object_id = apigateway_get_object_id(event)

    try:
        table.delete_item(Key={"object_id": object_id})
        return apigateway_response({"sucess": True})
    except ClientError as e:
        return apigateway_response({"success": False, "message": e.response['Error']['Message']}, 500)
