import os
from dotenv import load_dotenv, find_dotenv
from twilio.rest import Client

dotenv_path = find_dotenv()

TWILIO_TOKEN = os.environ.get("TWILIO_TOKEN")
TWILIO_SID = os.environ.get("TWILIO_SID")


account_sid = TWILIO_SID
auth_token = TWILIO_TOKEN
client = Client(account_sid, auth_token)

message = client.messages.create(
  from_='+18667401602',
  body='Hello from Twilio',
  to='+18777804236'
)

print(message.sid)