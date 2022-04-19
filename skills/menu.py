from typing import Text
from linebot.models import TextSendMessage, FlexSendMessage
from models.message_request import MessageRequest
from skills import add_skill
import json


@add_skill('選單')
def get(message_request: MessageRequest):
    flex_message = FlexSendMessage(
        alt_text='選單',
        contents=json.load(open('./messages/card.json', 'r', encoding='utf-8'))
    )
    return [
        flex_message
    ]
