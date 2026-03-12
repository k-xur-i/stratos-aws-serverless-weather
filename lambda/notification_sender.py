import boto3

SNS_TOPIC_ARN = "arn:aws:sns:eu-north-1:969608026041:WeatherAlertTopic:c53ed2b6-10f4-43bf-a2ae-63c6d10d9c7b"

def lambda_handler(event, context):
    sns = boto3.client("sns", region_name="us-east-1")

    for record in event["Records"]:
        message = record["body"]
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=message,
            Subject="⚠️ Extreme Weather Alert!"
        )
        print(f"Notification sent: {message}")

    return {"statusCode": 200, "body": "Notifications sent"}