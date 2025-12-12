# Sentiment Analyzer (AWS Serverless Project)

A lightweight web application that analyzes customer feedback in real time using **AWS Lambda**, **Amazon Comprehend**, and **API Gateway**. The frontend is a simple HTML/JavaScript page that sends text to a serverless backend for sentiment classification.

---

## Architecture Overview

User → Browser (HTML + JS)
→ API Gateway (POST /sentiment)
→ Lambda Function
→ Amazon Comprehend
→ Lambda returns sentiment result
→ Browser displays output


---

## AWS Services Used

- **Amazon Comprehend** — Performs sentiment analysis  
- **AWS Lambda** — Backend Python logic  
- **API Gateway (HTTP API v2)** — Exposes REST endpoint  
- **IAM** — Secure role allowing Lambda → Comprehend  
- **Static Hosting or Website** — Hosts the frontend demo  

---

## Project Files

| File | Description |
|------|-------------|
| `lambda.py` | Lambda function that calls Comprehend |
| `sentiment.html` | Frontend that sends POST requests to API Gateway |
| `README.md` | Project documentation |

---

## Lambda Function (Python)

```python
import json
import boto3

comprehend = boto3.client("comprehend")

def lambda_handler(event, context):
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Methods": "POST, OPTIONS"
    }

    method = event.get("requestContext", {}).get("http", {}).get("method")
    if method == "OPTIONS":
        return {"statusCode": 200, "headers": headers}

    body = json.loads(event.get("body", "{}"))
    text = body.get("text", "")

    if not text:
        return {
            "statusCode": 400,
            "headers": headers,
            "body": json.dumps({"error": "No text provided"})
        }

    result = comprehend.detect_sentiment(Text=text, LanguageCode="en")

    response = {
        "sentiment": result["Sentiment"],
        "scores": result["SentimentScore"]
    }

    return {
        "statusCode": 200,
        "headers": headers,
        "body": json.dumps(response)
    }


<!DOCTYPE html>
<html>
<head>
    <title>Sentiment Analyzer</title>
    <style>
        body { font-family: Arial; margin: 40px; }
        textarea { width: 600px; height: 150px; }
        button { padding: 10px 20px; margin-top: 10px; }
        #result { margin-top: 20px; white-space: pre-wrap; }
    </style>
</head>
<body>
    <h1>Sentiment Analyzer</h1>

    <textarea id="feedback"></textarea><br>
    <button onclick="analyze()">Analyze Sentiment</button>

    <div id="result"></div>

    <script>
        const API_URL = "YOUR_API_GATEWAY_URL";

        async function analyze() {
            const text = document.getElementById("feedback").value;
            if (!text) return alert("Enter some text first!");

            try {
                const response = await fetch(API_URL, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ text })
                });

                const result = await response.json();
                document.getElementById("result").innerText =
                    JSON.stringify(result, null, 2);
            } catch (err) {
                document.getElementById("result").innerText =
                    "Error calling API.";
                console.error(err);
            }
        }
    </script>
</body>
</html>

Testing With Postman

POST →
https://your-api-id.execute-api.region.amazonaws.com/prod/sentiment

JSON Body:
{
  "text": "This is an example sentence."
}
Common Issue: CORS Error "Origin null"

Occurs when opening HTML via:

file:///C:/...

Fix: run a local development server:
python -m http.server 8080


Open in browser:
http://localhost:8080/sentiment.html

Live Project

Live demo and full explanation available here:

https://chrissaave.net/sentiment-analyzer/

Video Tutorial (Coming Soon)

Will include:

IAM setup

Lambda walkthrough

API Gateway creation

Testing with Postman

Frontend build

Fixing browser CORS

Hosting the project

Author

Chris Saave
AWS • AI • Serverless • Cloud Projects
