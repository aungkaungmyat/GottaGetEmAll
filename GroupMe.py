from groupy import Client
import json
import requests

CREDENTIALS_FILE = "groupme_credentials.json"


with open(CREDENTIALS_FILE) as f:
    tc = json.load(f)

client = Client.from_token(tc['access_token_key'])

messages = client.bots.post(tc['bot_id'], "Yoda left the conversation")

