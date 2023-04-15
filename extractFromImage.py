import boto3
import base64
import re

s3 = boto3.client('s3')
textract = boto3.client('textract')


def lambda_handler(event, context):
    event = event['Input']
    bucket_name = event['bucketName']
    file_name = event['fileName']

    s3_object = s3.get_object(Bucket=bucket_name, Key=file_name)
    image = s3_object['Body'].read().decode("utf8")

    img_str = base64.b64decode(image)

    response = textract.detect_document_text(Document={
        'Bytes': img_str, 'S3Object': {
            'Bucket': bucket_name,
            'Name': file_name}})

    text = ''
    for item in response['Blocks']:
        if item['BlockType'] == 'LINE':
            text += item['Text'] + ','

    search_data = clean_text(text)

    return {
        'statusCode': 200,
        'body': search_data
    }


def clean_text(text):
    text = text.replace(",", " ")
    text = text.strip()
    search_data = re.sub('[^a-zA-Z ]', "", text)
    return search_data
