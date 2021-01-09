#!/usr/bin/env python
# coding: utf-8

# In[7]:


# !pip install slacker
# !pip install websocket-client
# !pip install flask


# In[16]:


from slacker import Slacker
import json
from flask import Flask, request, make_response
import os


# In[5]:


token = os.getenv('SLACK_BOT_TOKEN')
print(token)
slack = Slacker(token)
# slack.chat.post_message('#gagkobot-dev', '시작')
app = Flask(__name__)


# In[19]:


def get_answer(user_query):
    if user_query == "!ping":
        return "!pong"
    else:
        return ""


# In[1]:


def event_handler(event_type, slack_event):
    print(slack_event)
    channel = slack_event["event"]["channel"]
    user_query = slack_event['event']['text'].strip()
    answer = get_answer(user_query)
    if answer != "":
        slack.chat.post_message(channel, answer)
        return make_response("ok", 200, )
    else:
        message = "[%s] cannot find event handler" % event_type
        return make_response(message, 200, {"X-Slack-No-Retry": 1})


# In[21]:


@app.route('/', methods=['POST'])
def hello_there():
    slack_event = json.loads(request.data)
    
    if "challenge" in slack_event:
        return make_response(slack_event["challenge"], 200, {"content_type": "application/json"})
    
    if "event" in slack_event:
        event_type = slack_event["event"]["type"]
        return event_handler(event_type, slack_event)

    return make_response("There are no slack request events", 404, {"X-Slack-No-Retry": 1})


# In[5]:


if __name__ == '__main__':
    app.run(debug=True)

