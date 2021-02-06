import decimal
import json


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)


def apigateway_response(body, status_code=200):
    return {
        "isBase64Encoded": False,
        "headers": {
            "Content-Type": "application/json"
        },
        "statusCode": status_code,
        "body": json.dumps(body, cls=DecimalEncoder),
    }


def apigateway_get_object_id(event):
    return event["pathParameters"]["object_id"]
