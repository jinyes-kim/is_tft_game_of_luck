import json
import boto3
import datetime


def lambda_handler(event, context):
    request = event['httpMethod']

    if request == 'GET':
        return {
            'statusCode': 200,
            'body': json.dumps('On Service')
        }

    elif request == 'POST':
        bucket = 'bucket_name'
        file_name = str(datetime.datetime.now())[:-7]
        file = event['body']
        result = upload_file_s3(bucket, file_name + '.json', file)

        if result:
            return {
                'statusCode': 200,
                'body': json.dumps("upload success")
            }
        else:
            return {
                'statusCode': 400,
                'body': json.dumps("upload fail")
            }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps('BAD REQUEST')
        }


def upload_file_s3(bucket, file_name, file):
    encode_file = bytes(json.dumps(file).encode('UTF-8'))
    s3 = boto3.client('s3')
    try:
        s3.put_object(Bucket=bucket, Key=file_name, Body=encode_file)
        return True
    except:
        return False
