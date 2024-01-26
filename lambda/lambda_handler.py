import json

def handler(event, context):
    print(event)
    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Hello from Lambda!"}),
        "headers": {"Access-Control-Allow-Origin": "*"},
    }
