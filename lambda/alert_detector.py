import boto3
from boto3.dynamodb.conditions import Attr
import json

TABLE_NAME = "WeatherData"
QUEUE_NAME = "WeatherAlerts"

# Thresholds for extreme weather
TEMP_HIGH = 40      # Celsius
WIND_HIGH = 60      # km/h
HUMIDITY_LOW = 20   # percent

def lambda_handler(event, context):
    dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
    sqs = boto3.client("sqs", region_name="us-east-1")
    table = dynamodb.Table(TABLE_NAME)

    queue_url = sqs.get_queue_url(QueueName=QUEUE_NAME)["QueueUrl"]

    response = table.scan()
    items = response.get("Items", [])

    for item in items:
        alerts = []
        temp = float(item.get("temperature", 0))
        wind = float(item.get("wind_speed", 0))
        humidity = float(item.get("humidity", 100))

        if temp > TEMP_HIGH:
            alerts.append(f"HIGH TEMPERATURE: {temp}°C in {item['city']}")
        if wind > WIND_HIGH:
            alerts.append(f"HIGH WIND SPEED: {wind} km/h in {item['city']}")
        if humidity < HUMIDITY_LOW:
            alerts.append(f"LOW HUMIDITY: {humidity}% in {item['city']}")

        for alert in alerts:
            sqs.send_message(QueueUrl=queue_url, MessageBody=alert)
            print(f"Alert sent: {alert}")

    return {"statusCode": 200, "body": "Alert check complete"}