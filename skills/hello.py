from typing import Text
from linebot.models import TextSendMessage
from models.message_request import MessageRequest
from skills import add_skill


@add_skill('hello')
def get(message_request: MessageRequest):
    text='$ Cony $'
    emoji = [
        {
            "index": 0,
            "productId": "5ac21184040ab15980c9b43a",
            "emojiId": "002"
        },
        {
            "index": 7,
            "productId": "5ac21184040ab15980c9b43a",
            "emojiId": "001"
        }
    ]

    sender = {
        "name": "gg",
        "iconUrl": "https://line.me/conyprof"
    }

    return [
        # TextSendMessage(text='$ LINE emoji $', emojis=emoji)
        TextSendMessage(text=text, emojis=emoji, sender = sender)
    ]
