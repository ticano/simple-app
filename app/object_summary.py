import os
import json
from datetime import date
import logging
import botocore
import boto3
import csv


BUCKET_NAME = os.environ["BUCKET_NAME"]
KEY_PREFIX = os.environ["KEY_PREFIX"]
TABLE_NAME = os.environ["TABLE_NAME"]
TEMP_FILENAME = '/tmp/summary.csv'


s3_resource = boto3.resource('s3')
s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")

table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, context):

    today =  date.today().strftime('%d-%m-%Y')
    try:
        with open(TEMP_FILENAME, 'w') as output_file:
            writer = csv.writer(output_file)
            header = True
            first_page = True
    
            # Paginate results
            while True:
    
                # Scan DynamoDB table
                if first_page:
                    response = table.scan()
                    first_page = False
                else:
                    response = table.scan(ExclusiveStartKey = response['LastEvaluatedKey'])
    
                for item in response['Items']:
    
                    # Write header row?
                    if header:
                        writer.writerow(item.keys())
                        header = False
    
                    writer.writerow(item.values())
    
                # Last page?
                if 'LastEvaluatedKey' not in response:
                    break

        bucket_object = KEY_PREFIX + '/' + 'summary-' + today + '.csv'
        # Upload temp file to S3
        s3_resource.Bucket(BUCKET_NAME).upload_file(TEMP_FILENAME, bucket_object)
        
    except botocore.exceptions.ClientError as e:
        logging.exception("Failed to put file to S3 bucket\n\n" + str(e))

