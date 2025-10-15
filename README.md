# Legal Post Generator Project

## Overview

This project automates the generation and posting of legal-related content with AI-generated images, with reminders sent via Slack to ensure timely post generation. It includes scripts to generate posts, create custom AI images, overlay text on images, interact with content APIs, send messages to Slack, and send reminders.

## New Features

- **AI Image Generation**: Uses HuggingFace API to generate custom legal-themed images
- **Text Overlay**: Professional text overlay with holiday themes and multiple styling variants
- **UAE Holiday Integration**: Automatically detects UAE public holidays and themes content accordingly
- **Trending News Integration**: Fetches relevant legal news for content inspiration
- **Downloadable Images**: Generated posts can be downloaded as PNG files

## Prerequisites

- Python 3.7 or higher
- A Slack workspace with an Incoming Webhook URL for sending messages
- HuggingFace API key for image generation
- OpenRouter API key for content generation
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
   HUGGINGFACE_API_KEY=your_huggingface_api_key_here
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   OPENROUTER_MODEL=mistralai/mixtral-8x7b-instruct  # Optional: specify model
   ```

   Replace the URLs and keys with your actual credentials.

5. **Install additional dependencies** (if not already installed):

   ```bash
   pip install python-dotenv Pillow gnews4py
   ```

## Scripts

### generate_posts.py

A Streamlit web app that allows users to select a legal niche and generate 2 unique Instagram-style post ideas with AI-generated graphics. Features include:

- Legal niche selection (Corporate, Family, Criminal, IP, Immigration, Real Estate, Tax Law)
- Optional date selection for holiday-specific content
- AI-generated images tailored to the legal niche
- Professional text overlay with multiple styling variants
- UAE holiday detection and theming
- Downloadable PNG files for each post
- Automatic Slack integration

**Run the app:**

```bash
streamlit run generate_posts.py
```

### content_api.py

Contains functions to generate social media post ideas for a law firm based on a selected legal niche. Features:

- UAE public holiday detection using Nager.Date API
- Trending news article fetching from UAE sources
- Context-aware prompt building for AI content generation
- OpenRouter API integration for professional legal content
- Holiday-specific content theming

### huggingface_api.py

AI image generation using HuggingFace's Stable Diffusion XL model. Features:

- Legal niche-specific image generation
- Multiple style variants for diverse outputs
- UAE holiday theming with appropriate colors and accents
- Professional, text-friendly backgrounds
- Automatic fallback to solid color backgrounds on API failure

### img_overlay.py

Professional text overlay functionality with features:

- Multiple text placement modes (bottom center, center left, center)
- Holiday-themed accents and bokeh effects
- Text glow effects for readability
- Automatic line wrapping and sizing
- Style variants for visual diversity

### send_to_slack.py

Provides a function to send messages to a Slack channel using a webhook URL. Features:

- Error handling and logging
- Success/failure feedback
- Marker file creation (`post_sent.txt`) to track successful posts

### reminder.py

Sends a Slack reminder message at a specified time once per day.

- Configure the reminder time by setting the `reminder_hour` and `reminder_minute` variables (24-hour format)
- Checks current time every 30 seconds
- Example reminder message: "Reminder: You haven't generated today's post yet!"

**Run the reminder service:**

```bash
python reminder.py
```

## Environment Variables

- `SLACK_WEBHOOK_URL`: Your Slack incoming webhook URL
- `HUGGINGFACE_API_KEY`: HuggingFace API key for image generation
- `OPENROUTER_API_KEY`: OpenRouter API key for content generation
- `OPENROUTER_MODEL`: Optional model specification (default: mistralai/mixtral-8x7b-instruct)

## Usage

1. Ensure your `.env` file is correctly set up with all required API keys
2. Run `reminder.py` to start the reminder service (optional)
3. Run the main app: `streamlit run generate_posts.py`
4. Select a legal niche and optional date
5. Click "Generate Posts" to create content and images
6. Download generated posts or let them be sent to Slack automatically

## Supported Legal Niches

- Corporate Law
- Family Law
- Criminal Law
- Intellectual Property
- Immigration Law
- Real Estate Law
- Tax Law

## Notes

- The reminder script must be running to send reminders at the specified time
- Make sure your system time is correct to ensure timely reminders and holiday detection
- Internet connection required for API calls to HuggingFace, OpenRouter, and news services
- Generated images are 1024x1024 pixels, optimized for Instagram

## Troubleshooting

- If images fail to generate, verify `HUGGINGFACE_API_KEY` is correctly set
- If content generation fails, check `OPENROUTER_API_KEY` configuration
- If reminders aren't sent, verify `SLACK_WEBHOOK_URL` is correct
- Check internet connection and API service status
- Review console output for any error messages
- Ensure all required Python packages are installed: `pip install -r requirements.txt python-dotenv Pillow gnews4py`
