# Load environment variables from .env
import os
from dotenv import load_dotenv
from twilio.rest import Client


load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
EMERGENCY_CONTACT_NUMBER = os.getenv("EMERGENCY_CONTACT_NUMBER")
DB_DIR = os.getenv("DB_LOCATION")


def emergency_call():
    print("ADA error in emergency_call function")
    """
    Makes an emergency call using Twilio when the prompt indicates a crisis situation.
    """
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

        # call = client.calls.create(
        #     to=EMERGENCY_CONTACT_NUMBER,
        #     from_=TWILIO_PHONE_NUMBER,
        #     url='http://demo.twilio.com/docs/voice.xml'  # This URL should point to your TwiML instructions
        # )
        print(f"Emergency call initiated, SID: {call.sid}")
    except Exception as e:
        print(f"Failed to place emergency call. {e}")




