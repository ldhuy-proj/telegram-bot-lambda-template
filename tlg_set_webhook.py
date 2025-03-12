import requests
import os
import sys

def set_telegram_webhook():
    bot_token = os.getenv("BOT_TOKEN")
    lambda_function_url = os.getenv("LAMBDA_FUNCTION_URL")

    if not bot_token or not lambda_function_url:
        print("Missing BOT_TOKEN or LAMBDA_FUNCTION_URL")
        sys.exit(1)

    url = f"https://api.telegram.org/bot{bot_token}/setWebhook"
    params = {"url": lambda_function_url}

    try:
        response = requests.get(url, params=params)
        response_data = response.json()

        if response_data.get("ok") == True:
            print("✅ Webhook set successfully!")
            sys.exit(0)
        else:
            print(f"Failed to set Webhook: {response_data}")
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    set_telegram_webhook()
