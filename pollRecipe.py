import boto3
import os
import json

sqs = boto3.client('sqs')
queue_url = os.environ.get('QueueUrl')


def lambda_handler(event, context):
    response = sqs.receive_message(QueueUrl=queue_url)
    if 'Messages' in response:
        message_body = response['Messages'][0]['Body']
        data = json.loads(message_body)
        sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=response['Messages'][0]['ReceiptHandle']
        )
        return {
            "statusCode": 200,
            'headers': {
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,GET,POST"
            },
            "body": data
        }
    else:
        return {
            "statusCode": 200,
            'headers': {
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,GET,POST"
            },
            "Message": 'No messages in queue'
        }
