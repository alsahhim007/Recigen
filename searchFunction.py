import json
import os
import boto3


def lambda_handler(event, context):
    step_arn = os.environ.get('StepFunc')
    poll_url = os.environ.get('PollUrl')
    extract_image_lambda = os.environ.get('ExtractFromImage')
    get_recipe_lambda = os.environ.get('GetRecipe')
    result_to_queue_lambda = os.environ.get('ResultToQueue')
    step_function_client = boto3.client('stepfunctions')

    if 'image' in event:
        data = save_image_lambda(event)
        data['extractFromImage'] = extract_image_lambda
        data['getRecipe'] = get_recipe_lambda
        data['resultToQueue'] = result_to_queue_lambda
    else:
        data = event
        data['type'] = 'text'
        data['getRecipe'] = get_recipe_lambda
        data['resultToQueue'] = result_to_queue_lambda
    step_function_client.start_execution(
        stateMachineArn=step_arn,
        input=json.dumps(data)
    )

    return {
        "statusCode": 200,
        'headers': {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,GET,POST"
        },
        "body": {
            "message": "To poll the recipe info use its url: " + poll_url
        }
    }


def save_image_lambda(event):
    lambda_client = boto3.client('lambda')
    lambda_function = os.environ.get('SaveImageLambda')

    response = lambda_client.invoke(
        FunctionName=lambda_function,
        InvocationType='RequestResponse',
        Payload=json.dumps(event)
    )
    return json.loads(response['Payload'].read())
