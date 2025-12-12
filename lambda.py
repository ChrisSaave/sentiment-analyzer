import json
import boto3

comprehend = boto3.client(“comprehend”)


def lambda_handler(event, context):
    “””
    Expected event format:
    {
        “text”: “I love this product”
    }
    or, if called through API Gateway:
    {
        “body”: “{\”text\”: \”I love this product\”}”
    }
    “””

    # CORS headers used in all responses
    cors_headers = {
        “Access-Control-Allow-Origin”: “*”,
        “Access-Control-Allow-Headers”: “Content-Type”,
        “Access-Control-Allow-Methods”: “OPTIONS,POST”
    }

    # Handle CORS preflight (OPTIONS) requests for HTTP API v2
    method = event.get(“requestContext”, {}).get(“http”, {}).get(“method”)
    if method == “OPTIONS”:
        return {
            “statusCode”: 200,
            “headers”: cors_headers,
            “body”: “”
        }

    # Normal POST handling
    body = event
    if “body” in event:
        body = event[“body”]
        if isinstance(body, str):
            body = json.loads(body)

    text = body.get(“text”)

    if not text:
        return {
            “statusCode”: 400,
            “headers”: cors_headers,
            “body”: json.dumps({“error”: “text is required”})
        }

    response = comprehend.detect_sentiment(
        Text=text,
        LanguageCode=“en”
    )

    result = {
        “sentiment”: response[“Sentiment”],
        “scores”: response[“SentimentScore”]
    }

    return {
        “statusCode”: 200,
        “headers”: cors_headers,
        “body”: json.dumps(result)
    }
 
