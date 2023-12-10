import requests
import os
from dotenv import load_dotenv


def send(message):

    load_dotenv()
    line_notify_token = os.getenv("LINE_NOTIFY_TOKEN")

    url = "https://notify-api.line.me/api/notify"
    headers = {
        "Authorization": f"Bearer {line_notify_token}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"message": message}

    response = requests.post(url, headers=headers, data=data)

    if response.status_code != 200:
        return False

    return True

if __name__ == "__main__":
    msg = 'hello'
    result = send(msg)
    if result:
        print("Message sent successfully")
    else:
        print("Failed to send message")
