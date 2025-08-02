import requests
import os
from dotenv import load_dotenv

load_dotenv()

def send_post_to_slack(message):
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    if not webhook_url:
        print("Slack webhook not set.")
        return

    payload = {"text": message}
    try:
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 200:
            print("Post sent to Slack.")
        
            with open("post_sent.txt", "w") as f:
                f.write("true")
            return True
        else:
            print("Failed to send post to Slack.")
            return False
    except Exception as e:
        print("Error sending post:", e)
