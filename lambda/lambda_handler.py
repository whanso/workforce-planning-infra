def handler(event, context):
    print(event)
    return {
        "statusCode": 200,
        "body": {"message": "Hello from Lambda!"},
        "headers": {"Access-Control-Allow-Origin": "*"},
    }
