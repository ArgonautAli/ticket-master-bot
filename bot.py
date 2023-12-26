import slack_sdk
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter

env_path = Path(".")/".env"
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'],"/slack/events", app)

client = slack_sdk.WebClient(token=os.environ['SLACK_TOKEN'])
BOT_ID = client.api_call("auth.test")["user_id"]

# client.chat_postMessage(channel="#test-ahk", text="hello world")

@slack_event_adapter.on("reaction_added")
def reaction_added(event_data):
  channel_id = event_data["event"]["item"]["channel"]
  message_id = event_data["event"]["item"]["ts"]

  emoji = event_data["event"]["reaction"]
# print("event_data",event_data)
#   print("event_data message",event_data)
  result = client.conversations_history(
        channel=channel_id,
        inclusive=True,
        oldest=message_id,
        limit=1
    )

  message = result["messages"][0]
    # Print message text
  print("messages",message["blocks"])
  blocks = message["blocks"]

  for block in blocks:
    for bl in block.get("elements"):
       print('bl.get("type")',bl)
       if bl.get("type") == "link":
          print("bl1", bl)

    
       

@slack_event_adapter.on("message")
def message(payload):
    event = payload.get("event", {})
    print("event",event)
#     channel_id = event.get("channel")
#     user_id = event.get("user")
#     text = event.get("text")
#     if(user_id != BOT_ID):
#         client.chat_postMessage(channel=channel_id, text=text)


if __name__ == "__main__":
    app.run(debug=True, port=8000)