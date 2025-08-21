import time
import datetime
import requests
import os
from dotenv import load_dotenv

# Load Slack webhook from .env
load_dotenv()
slack_url = os.getenv("SLACK_WEBHOOK_URL")

if not slack_url:
    raise ValueError("SLACK_WEBHOOK_URL environment variable not set")

def send_reminder():
    message = {"text": "Reminder: You haven’t generated today’s post yet!"}
    response = requests.post(slack_url, json=message)
    if response.status_code == 200:
        print("Reminder sent!")
    else:
        print(f"Failed to send reminder: {response.status_code} {response.text}")

# User declares reminder time here (hour and minute)
reminder_hour = 14
reminder_minute = 19

already_sent = False

while not already_sent:
    now = datetime.datetime.now()
    # print(f"Checking time: {now.hour}:{now.minute}")
    if now.hour == reminder_hour and now.minute == reminder_minute:
        send_reminder()
        already_sent = True
    time.sleep(30) # Check every 30 seconds
