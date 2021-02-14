from http import HTTPStatus
import json
import os

from flask import Flask, request, make_response
from slacker import Slacker

token = os.getenv('SLACK_BOT_TOKEN')
debug = os.getenv('DEBUGGING')
slack = Slacker(token)
app = Flask(__name__)


def get_answer(user_query_arr):
    if user_query_arr[0] == "!ping":
        return "!pong"
    else:
        return ""


def event_handler(event_type, slack_event):
    channel = slack_event["event"]["channel"]
    user_query = slack_event['event']['text'].strip()
    user_query_arr = user_query.split(" ")

    if user_query_arr[0][0] == "!":
        answer = get_answer(user_query_arr)

        if answer != "":
            slack.chat.post_message(channel, answer)
            return make_response("", HTTPStatus.OK)
        else:
            return make_response("[%s] is not a command" % user_query_arr[0], HTTPStatus.BAD_REQUEST, {"X-Slack-No-Retry": 1})
    else:
        return make_response("", HTTPStatus.NO_CONTENT, {"X-Slack-No-Retry": 1})


@app.route('/', methods=['POST'])
def slack_request():
    slack_event = json.loads(request.data)

    if "challenge" in slack_event:
        return make_response(slack_event["challenge"], HTTPStatus.OK, {"content_type": "application/json"})

    if "event" in slack_event:
        event_type = slack_event["event"]["type"]
        return event_handler(event_type, slack_event)

    return make_response("There are no slack request events", HTTPStatus.NOT_FOUND, {"X-Slack-No-Retry": 1})


if __name__ == '__main__':
    app.run(debug=debug)
