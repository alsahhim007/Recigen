import json
import boto3
import os


def lambda_handler(event, context):
    queue_url = os.environ.get('QueueUrl')
    responses = event['Input']['getRecipeResult']['Payload']['search']
    message = {}
    for index, response in enumerate(responses):
        message[index] = {
            "instuctions": response['instructions'],
            "title": response['title'],
            "src": response['image'],
        }

    sqs_client = boto3.client('sqs')
    sqs_client.send_message(
        QueueUrl=queue_url, MessageBody=json.dumps(message))
