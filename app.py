import os
import sys
import json
import random

from urllib.parse import urlencode
from urllib.request import Request, urlopen

from flask import Flask, request

application = Flask(__name__)

@application.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    log(data)
    if data['sender_type'] == 'bot' or data['text'] != "/roll":
       return "ok", 200

    log('Received {}'.format(data))

    roll = random.randint(1, 20)
    if roll == 1:
        roll = "a failure"
    elif roll < 5:
        roll = str(roll) + " ouch"
    elif roll == 20:
        roll = "CRITICAL"

    msg = '{}, you rolled "{}".'.format(data['name'], roll)
    send_message(msg)

    return "ok", 200

def send_message(msg):
    url  = 'https://api.groupme.com/v3/bots/post'
    #url = 'https://web.groupme.com/chats'

    data = {
        'bot_id' : os.getenv('GROUPME_BOT_ID'),
        'text'   : msg,
        }
    request = Request(url, urlencode(data).encode())
    json = urlopen(request).read().decode()
  
def log(msg):
    print(str(msg))
    sys.stdout.flush()

if __name__=="__main__":
    application.run()