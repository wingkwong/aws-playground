import json
import boto3

glue = boto3.client(service_name='glue', region_name='ap-southeast-1',
              endpoint_url='https://glue.ap-southeast-1.amazonaws.com')

def lambda_handler(event, context):
    try:
       glue.start_crawler(Name='crawler-name')
    except Exception as e:
        print(e)
        print('Error starting crawler')
        raise e
