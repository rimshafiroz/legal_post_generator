import os
from dotenv import load_dotenv

load_dotenv()

def print_env_var(var_name):
    value = os.getenv(var_name)
    if value:
        print(f"{var_name}: {value}")
    else:
        print(f"{var_name} is NOT set.")

if __name__ == "__main__":
    print_env_var("GOOGLE_API_KEY")
    print_env_var("REPLICATE_API_TOKEN")
    print_env_var("SLACK_WEBHOOK_URL")