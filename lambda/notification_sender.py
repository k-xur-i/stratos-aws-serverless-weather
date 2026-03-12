import boto3

SNS_TOPIC_ARN = "arn"

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