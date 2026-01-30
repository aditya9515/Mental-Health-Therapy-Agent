# Setup OLLAMA medgemma 4b
import ollama
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
EMERGENCY_CONTACT_NUMBER = os.getenv("EMERGENCY_CONTACT_NUMBER")

def Query_medgemma(prompt: str) -> str:
    """
    Calls the medgemma 4b model from Ollama and returns the response    
    as a therapist
    """
    system_prmpt = """
    You are Dr. Emily Hartman, a warm and experienced clinical psychologist. 
    Respond to patients with:

    1. Emotional attunement ("I can sense how difficult this must be...")
    2. Gentle normalization ("Many people feel this way when...")
    3. Practical guidance ("What sometimes helps is...")
    4. Strengths-focused support ("I notice how you're...")

    Key principles:
    - Never use brackets or labels
    - Blend elements seamlessly
    - Vary sentence structure
    - Use natural transitions
    - Mirror the user's language level
    - Always keep the conversation going by asking open-ended questions to dive into the root cause of patients problem
    """
    try:
        response = ollama.chat(
            model="alibayram/medgemma:4b",
            messages=[
                {"role": "system", "content": system_prmpt},
                {"role": "user", "content": prompt}
            ],
            options={
                "num_predict": 350,
                "temperature": 0.7,
                "top_p": 0.9
            }
        )
        return response['message']['content'].strip()
    except Exception as e:
        return f"I am having technical difficulties right now. Please try again later. {e}"

# Setting up Twilio for emergency calls
from twilio.rest import Client

def emergency_call():
    """
    Makes an emergency call using Twilio when the prompt indicates a crisis situation.
    """
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

        call = client.calls.create(
            to=EMERGENCY_CONTACT_NUMBER,
            from_=TWILIO_PHONE_NUMBER,
            url='http://demo.twilio.com/docs/voice.xml'  # This URL should point to your TwiML instructions
        )
        print(f"Emergency call initiated, SID: {call.sid}")
    except Exception as e:
        print(f"Failed to place emergency call. {e}")

# Test
if __name__ == "__main__":
    # print(Query_medgemma("I feel anxious all the time and can't sleep."))
    emergency_call()
