import boto3
import json
import uuid

db = boto3.resource(
    'dynamodb', endpoint_url='http://docker.for.mac.localhost:8000/')
table = db.Table('comments')


def index():
    response = table.scan()
    return {'statusCode': 200, 'body': json.dumps(response['Items'])}


def create(event):
    data = json.loads(event['body'])

    table.put_item(
        Item={
            'uuid': str(uuid.uuid4()),
            'comment': data['comment']
        }
    )

    return {'statusCode': 200, 'body': json.dumps({'message': 'Created!'})}


def handler(event, context):
    if event['httpMethod'] == 'GET':
        return index()
    elif event['httpMethod'] == 'POST':
        return create(event)
