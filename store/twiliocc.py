# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
import sys

def send_whatsapp_message(body):
    # Find your Account SID and Auth Token at twilio.com/console
    # and set the environment variables. See http://twil.io/secure
    account_sid = 'AC8377f54cdd5a489e9adee3de643a5317'
    auth_token = '4e0d1c268576e6cbab20646a6f75f6cb'
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
            from_='whatsapp:+14155238886',
            to='whatsapp:+2349166059162',
            body=body
        )

    print(message.sid)

if __name__ == "__main__":
    # Check if the body argument is provided
    if len(sys.argv) != 2:
        print("Usage: python script.py 'your_message_body'")
        sys.exit(1)

    message_body = sys.argv[1]
    send_whatsapp_message(message_body)
