import json
import boto3
import urllib.request
from datetime import datetime


API_KEY = "api"
CITIES = ["Chennai", "Mumbai", "Delhi", "Bangalore", "Hyderabad"]
TABLE_NAME = "WeatherData"

def lambda_handler(event, context):
    dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
    table = dynamodb.Table(TABLE_NAME)

    for city in CITIES:
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read())

            weather_record = {
                "city": city,
                "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                "temperature": str(data["main"]["temp"]),
                "humidity": str(data["main"]["humidity"]),
                "wind_speed": str(data["wind"]["speed"]),
                "condition": data["weather"][0]["description"]
            }

            table.put_item(Item=weather_record)
            print(f"Saved data for {city}")

        except Exception as e:
            print(f"Error fetching data for {city}: {str(e)}")

    return {"statusCode": 200, "body": "Weather data saved successfully"}