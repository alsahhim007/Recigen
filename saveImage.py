import boto3
import os
import datetime


def lambda_handler(event, context):
    s3 = boto3.client('s3')
    image_bucket = os.environ.get('ImageBucket')
    now = datetime.datetime.now()
    file_name = 'image_{}.jpg'.format(now.strftime('%Y%m%d%H%M%S'))
    image_data = event['image']
    s3.put_object(Bucket=image_bucket, Key=file_name,
                  Body=image_data, ContentType='image/jpeg')
    
    return { "bucketName": image_bucket, "fileName": file_name, "type": "image"}
