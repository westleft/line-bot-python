from typing import Text
from linebot.models import CarouselTemplate, TemplateSendMessage, LocationAction, CarouselColumn
from models.message_request import MessageRequest
from skills import add_skill


@add_skill('找美食')
def get(message_request: MessageRequest):

    location = TemplateSendMessage(
             alt_text='地址選擇器',
             template=CarouselTemplate(
                 columns=[
                     CarouselColumn(
                         thumbnail_image_url='https://images.unsplash.com/photo-1548345680-f5475ea5df84?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=873&q=80',
                         title='請選擇地址',
                         text='傳送地址後才能替您查詢周邊美食喔!',
                         actions=[
                            LocationAction(label='傳送地址')
                        ]
                     )
                 ]
             )
    )

    return [
        location
    ]
