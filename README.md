# ☁️ Stratos — AWS Serverless Real-Time Weather Pipeline

A fully serverless, event-driven real-time weather monitoring and alerting system built on Amazon Web Services. Stratos automatically fetches live weather data for 5 major Indian cities every 5 minutes, detects extreme weather conditions, and sends automated email alerts — all without any manually managed servers.

🔗 **Live Dashboard:** [https://d23u0n35xg7mik.cloudfront.net/](https://d23u0n35xg7mik.cloudfront.net/)

---

## 🏗️ Architecture

```
EventBridge (every 5 min)
        ↓
Lambda: WeatherFetcher → OpenWeatherMap API
        ↓
Amazon DynamoDB (WeatherData table)
        ↓
Lambda: AlertDetector
        ↓
Amazon SQS (WeatherAlerts queue)
        ↓
Lambda: NotificationSender
        ↓
Amazon SNS → Email Alert
        
S3 + CloudFront → Live Dashboard (HTTPS)
```

---

## ⚙️ AWS Services Used

| Service | Resource | Purpose |
|---|---|---|
| Amazon EventBridge | FetchWeatherEvery5Minutes | Triggers pipeline every 5 minutes |
| AWS Lambda | WeatherFetcher | Fetches live weather data |
| AWS Lambda | AlertDetector | Detects extreme weather events |
| AWS Lambda | NotificationSender | Sends email alerts via SNS |
| Amazon DynamoDB | WeatherData | Stores all weather readings |
| Amazon SQS | WeatherAlerts | Fault-tolerant alert queue |
| Amazon SNS | WeatherAlertTopic | Email notification delivery |
| Amazon S3 | gtweather-site-dashboard | Frontend static hosting |
| Amazon CloudFront | stratos-weather | HTTPS CDN distribution |

---

## 🌆 Cities Monitored

Chennai · Mumbai · Delhi · Bangalore · Hyderabad

---

## ⚠️ Alert Thresholds

| Parameter | Threshold | Alert Type |
|---|---|---|
| Temperature | > 40°C | Extreme Heat Alert |
| Wind Speed | > 60 km/h | Storm / Gale Alert |
| Humidity | < 20% | Drought / Fire Risk |

---

## 📁 Project Structure

```
stratos-aws-serverless-weather/
├── lambda/
│   ├── weather_fetcher.py       # Fetches data from OpenWeatherMap, writes to DynamoDB
│   ├── alert_detector.py        # Scans DynamoDB, sends alerts to SQS
│   └── notification_sender.py   # Triggered by SQS, sends email via SNS
├── frontend/
│   └── weather_dashboard.html   # Live dashboard (hosted on S3 + CloudFront)
└── README.md
```

---

## 🚀 How to Deploy

### Prerequisites
- AWS Account (free tier is sufficient)
- OpenWeatherMap API key (free at [openweathermap.org](https://openweathermap.org))
- Python 3.12

### Steps

1. **DynamoDB** — Create a table named `WeatherData` with `city` (String) as partition key and `timestamp` (String) as sort key

2. **SQS** — Create a Standard queue named `WeatherAlerts`

3. **SNS** — Create a topic named `WeatherAlertTopic` and add an email subscription, confirm via email

4. **Lambda Functions** — Deploy each function in `lambda/` as a separate Lambda function named `WeatherFetcher`, `AlertDetector`, and `NotificationSender`. Set runtime to Python 3.12 and timeout to 30 seconds. Add your API key and SNS ARN as noted in the code.

5. **IAM** — Attach `AmazonDynamoDBFullAccess`, `AmazonSQSFullAccess`, and `AmazonSNSFullAccess` to each Lambda execution role

6. **EventBridge** — Create a rule with schedule `rate(5 minutes)` targeting the `WeatherFetcher` Lambda

7. **SQS Trigger** — Add the `WeatherAlerts` queue as a trigger on the `NotificationSender` Lambda

8. **Frontend** — Upload `weather_dashboard.html` to an S3 bucket with static website hosting enabled. Create a CloudFront distribution pointing to the S3 endpoint for HTTPS access.

---

## 🛠️ Built With

- Python 3.12
- AWS Lambda, DynamoDB, SQS, SNS, EventBridge, S3, CloudFront
- OpenWeatherMap API
- HTML5, CSS3, Vanilla JavaScript

