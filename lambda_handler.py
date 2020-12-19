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
        file = event['body']
        bucket = 'tft-jinyes-data'
        result = upload_file_s3(bucket, file)

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


def upload_file_s3(bucket, file):
    try:
        dt = datetime.datetime.utcnow().strftime("%Y-%m-%d")
        s3 = boto3.resource('s3')
        obj = s3.Object(bucket, 'dt={}/match-history.json'.format(dt))
        obj.put(Body=file)
        return True
    except:
        return False

