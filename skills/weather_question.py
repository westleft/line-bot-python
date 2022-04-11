from typing import Text
from linebot.models import MessageAction, TextSendMessage, PostbackAction, QuickReply, QuickReplyButton
from models.message_request import MessageRequest

from skills import add_skill

@add_skill('查詢天氣')
def get(message_request: MessageRequest):
    try :
        cityArr = ["臺北市", "新北市", "桃園市", "基隆市", "新竹市", "宜蘭縣", "花蓮縣", "高雄市", "苗栗縣", "臺中市", "臺南市"]
        citys = []
        for city in cityArr:
            citys.append(
                QuickReplyButton(
                    action=PostbackAction(
                        label=f'{city}',
                        # display_text=f'幫我查詢 {city} 天氣概況',
                        data=f'天氣縣市 {city}'
                    )
                )
            )

        message = TextSendMessage(
            text="請選擇要查詢的縣市:",
            quick_reply = QuickReply(
                items = citys
            )
        )

        return [
            message
        ]
    except:
        message = TextSendMessage(
            text="目前系統忙碌中，請稍後再查詢"
        )

        return [
            message
        ]
