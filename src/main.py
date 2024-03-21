from boto3 import resource
from json import loads, dumps
from uuid import uuid4

db = resource("dynamodb", endpoint_url="http://dynamodb-local:8000")
table = db.Table("comments")


def index():
    response = table.scan()
    return {
        "statusCode": 200,
        "body": dumps(response["Items"]),
        "headers": {"content-type": "application/json"},
    }


def create(event):
    data = loads(event["body"])

    table.put_item(Item={"uuid": str(uuid4()), "comment": data["comment"]})

    return {"statusCode": 200, "body": dumps({"message": "Created!"})}


def handler(event, context):
    if event["httpMethod"] == "GET":
        return index()
    elif event["httpMethod"] == "POST":
        return create(event)
