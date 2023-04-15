import boto3
from botocore.exceptions import ClientError
import requests
import json


def get_secret():
    secret_name = "spoonacular_API"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
        return get_secret_value_response
    except ClientError as e:
        raise e


def lambda_handler(event, context):
    api_key = get_secret()['SecretString']
    api_key = json.loads(api_key)
    ssm = boto3.client('ssm')
    response = ssm.get_parameter(Name='spoonacularURL', WithDecryption=True)
    url = response['Parameter']['Value']
    event = event['Input']
    if 'search' in event:
        search_text = event['search']
    else:
        search_text = event['lambdaResult']['Payload']['body']
    return request_spoon_recipe(api_key['api_key'], url, search_text)


def request_spoon_recipe(api_key, url, search_text):
    search_url = url + "/recipes/complexSearch"
    search_params = {"query": search_text, "apiKey": api_key, "number": 6}
    headers = {"apiKey": api_key}
    response = requests.request("GET", url=search_url, params=search_params, headers=headers)

    response = json.loads(response.text)
    ids = ''
    for r in response['results']:
        ids= ids+ str(r['id'])+','
    ids = ids.rstrip(",")
    ids_params = {"ids": ids, "apiKey": api_key}
    ids_url = url + "/recipes/informationBulk"
    response = requests.request("GET", url=ids_url,params=ids_params, headers=headers)
    return {"search": json.loads(response.text)}
