from typing import Text
from linebot.models import TextSendMessage, TemplateSendMessage
from linebot.models.template import ButtonsTemplate, ConfirmTemplate, CarouselTemplate, CarouselColumn
from linebot.models.actions import MessageAction, LocationAction
from models.message_request import MessageRequest
from skills import add_skill


@add_skill('buttons')
def get(message_request: MessageRequest):

    location = TemplateSendMessage(
        alt_text='Actions',
        template=ButtonsTemplate(
            title='Menu',
            text='地址選擇器',
            actions=[
                LocationAction(label='請選擇地址')
            ]
        )
    )
    return [
        location
    ]
