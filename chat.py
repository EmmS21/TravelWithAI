from twilio.rest import Client
import os
from langchain_community.chat_models import ChatPerplexity
from langchain_core.prompts import ChatPromptTemplate

def send_whatsapp(body, number):
    account_sid = os.environ.get('SID')
    auth_token = os.environ.get('AUTH_TOKEN')
    client = Client(account_sid, auth_token)
    message = client.messages.create(
    from_='whatsapp:+14155238886',
    body=body,
    to=number,
    )
    return message.sid

