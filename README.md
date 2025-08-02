# Legal Post Generator Project

## Overview

This project automates the generation and posting of legal-related content, with reminders sent via Slack to ensure timely post generation. It includes scripts to generate posts, interact with content APIs, send messages to Slack, and send reminders.

## Prerequisites

- Python 3.7 or higher
- A Slack workspace with an Incoming Webhook URL for sending messages
- `pip` for installing Python dependencies

## Setup

1. **Clone the repository** (if not already done):

   ```bash
   git clone <repository-url>
   cd legal_post_generator
   ```

2. **Create and activate a virtual environment** (recommended):

   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On Unix or MacOS
   source venv/bin/activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file** in the project root directory with the following content:

   ```
   SLACK_WEBHOOK_URL=https://hooks.slack.com/services/your/webhook/url
   ```

   Replace the URL with your actual Slack Incoming Webhook URL.

## Scripts

### reminder.py

Sends a Slack reminder message at a specified time once per day.

- Configure the reminder time by setting the `reminder_hour` and `reminder_minute` variables in the script (24-hour format).
- The script checks the current time every 60 seconds and sends the reminder when the time matches.
- Example reminder message: "Reminder: You haven’t generated today’s post yet!"

**Run the script:**

```bash
python reminder.py
```

### generate_posts.py

A Streamlit web app that allows users to select a legal niche and generate 3-4 social media post ideas based on the selected niche. It uses the content_api.py module to fetch post ideas and sends the generated posts to Slack using send_to_slack.py. The app provides user feedback on the success or failure of sending posts to Slack.

### content_api.py

Contains functions to generate social media post ideas for a law firm based on a selected legal niche. It builds a prompt with firm context and sends it to the Together AI API to generate professional and impactful post ideas. Requires the TOGETHER_API_KEY environment variable to access the API.

### send_to_slack.py

Provides a function to send messages to a Slack channel using a webhook URL specified in the SLACK_WEBHOOK_URL environment variable. It handles sending the message, error checking, and logs success or failure. It also writes a marker file `post_sent.txt` upon successful posting.

## Usage

1. Ensure your `.env` file is correctly set up with the Slack webhook URL.
2. Run `reminder.py` to start the reminder service.
3. Use other scripts as needed to generate and send posts.

## Notes

- The reminder script must be running to send the reminder at the specified time.
- Make sure your system time is correct to ensure timely reminders.
- You can customize the reminder message in `reminder.py` by editing the `message` dictionary.

## Troubleshooting

- If reminders are not sent, verify that the `SLACK_WEBHOOK_URL` is correctly set in the `.env` file.
- Check your internet connection and Slack webhook permissions.
- Review the console output for any error messages.
