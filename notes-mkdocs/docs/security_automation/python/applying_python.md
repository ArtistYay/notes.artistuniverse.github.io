---
tags:
  - Python
  - Computer Programming
---

## What is an API?

An API (Application Programming Interface) is a set of rules that allows different software systems to communicate. In network automation, APIs let you read/modify device configurations, pull monitoring data, or control cloud resources — all programmatically from Python. Most modern network equipment and platforms expose REST APIs.

## The `requests` Library — Making HTTP API Calls
The `requests` library is how Python communicates with web-based APIs over HTTP:
```python
import requests

# GET — retrieve data from an API endpoint
url = "https://jsonplaceholder.typicode.com/posts"
response = requests.get(url)

# Always check the status code before using the response
if response.status_code == 200:
    data = response.json()    # parse the JSON response into a Python dict/list
    for post in data:
        print(f"Post ID: {post['id']}, Title: {post['title']}")
else:
    print(f"Request failed with status: {response.status_code}")
```

Common HTTP status codes:
- `200` — OK, request succeeded
- `201` — Created successfully
- `400` — Bad request (something wrong with what you sent)
- `401` — Unauthorized (bad credentials)
- `404` — Not found
- `500` — Server error

## Full API Read → Modify → Push Workflow
```python
import requests
import json

url = "http://network-device-api/config"

# Step 1: Read current config from the API
response = requests.get(url)
data = response.json()

# Step 2: Save a local backup before making changes
with open("config_backup.json", "w") as file:
    json.dump(data, file)

# Step 3: Modify the configuration
data["setting"] = "new value"

# Step 4: Save the updated config locally
with open("config_updated.json", "w") as file:
    json.dump(data, file)

# Step 5: Push the updated configuration back to the device
response = requests.put(url, data=json.dumps(data))
print(f"Update status: {response.status_code}")
```

## Log Analysis with `pandas`
The `pandas` library makes analyzing structured data like CSV logs straightforward. A DataFrame works like a spreadsheet in Python — you can filter rows, group data, count occurrences, and much more:
```python
import pandas as pd

# Load a CSV log file into a DataFrame
df = pd.read_csv("logs.csv")

# Filter: keep only rows where the 'activity' column equals 'suspicious'
suspicious_df = df[df["activity"] == "suspicious"]

# Group by user and count how many suspicious events each user had
user_activity_count = suspicious_df.groupby("user").size()
print(user_activity_count)
```

## AWS Cloud Automation with `boto3`
```python
import boto3

# Create an S3 client with credentials
s3 = boto3.client(
    "s3",
    aws_access_key_id="YOUR_ACCESS_KEY",
    aws_secret_access_key="YOUR_SECRET_KEY",
    region_name="us-east-1"
)

# Try to create a bucket — wrap in try/except since it might already exist
try:
    s3.create_bucket(Bucket="my-unique-bucket-name")
    print("Bucket created successfully")
except Exception as e:
    print(f"Error: {e}")
```