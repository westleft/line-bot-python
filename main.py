import os
import re
import json
import requests
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from fastapi.params import Header
from starlette.requests import Request
from models.message_request import MessageRequest
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, FollowEvent, PostbackEvent
from linebot.models import TextSendMessage, FlexSendMessage
from skills import *
from skills import skills


app = FastAPI()

load_dotenv()

line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))


def get_message(request: MessageRequest):
    for pattern, skill in skills.items():
        if re.match(pattern, request.intent):
            return skill(request)
    request.intent = '{not_match}'
    return skills['{not_match}'](request)

@app.post("/api/line")
async def callback(request: Request, x_line_signature: str = Header(None)):
    body = await request.body()
    try:
        handler.handle(body.decode("utf-8"), x_line_signature)
    except InvalidSignatureError:
        raise HTTPException(
            status_code=400, detail="Invalid signature. Please check your channel access token/channel secret.")
    return 'OK'


@handler.add(event=MessageEvent, message=TextMessage)
def handle_message(event):
    msg_request = MessageRequest()
    msg_request.intent = event.message.text
    msg_request.message = event.message.text
    msg_request.user_id = event.source.user_id

    func = get_message(msg_request)
    line_bot_api.reply_message(event.reply_token, func)

# 加入好友
@handler.add(event=FollowEvent)
def handle_message(event):
    flex_message = FlexSendMessage(
        alt_text='選單',
        contents=json.load(open('./messages/card.json', 'r', encoding='utf-8'))
    )
    line_bot_api.reply_message(event.reply_token, flex_message)

# 天氣
@handler.add(event=PostbackEvent)
def handle_message(event):
    # 回傳卡片
    card = json.load(open('./messages/weather.json', 'r', encoding='utf-8'))

    try:
        # 爬蟲
        payload = {}
        headers = {
            'accept': 'application/json',
            'Cookie': 'TS01dbf791=0107dddfefdf0f1de44404bb56e72168df5349707ba3cafde81e1f03ac000dfc0911fe61d63e070e61a9e1def9310ee8e687eebeeb'
        }

        city = event.postback.data
        url = f"https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=CWB-BCE7C2F2-93BA-41D8-A955-3C6211EBCFE8&locationName={city}&elementName="

        response = requests.request("GET", url, headers=headers, data=payload)

        data = response.json()['records']['location']

        # 今天日期
        today = data[0]['weatherElement'][0]['time'][0]['startTime'][:10]
        card['header']['contents'][0]['contents'][0]['text'] = f"台灣 | {city} | {today}"
        # 天氣概況
        wx = data[0]['weatherElement'][0]['time'][0]['parameter']['parameterName']
        card['header']['contents'][0]['contents'][1]['text'] = wx
        # 最高溫
        maxT = data[0]['weatherElement'][4]['time'][0]['parameter']['parameterName']
        card['body']['contents'][0]['contents'][1]['text'] = f"最高溫度 | {maxT}°C"
        # 最低溫
        minT = data[0]['weatherElement'][2]['time'][0]['parameter']['parameterName']
        card['body']['contents'][1]['contents'][1]['text'] = f"最低溫度 | {minT}°C"
        # 降雨率
        pop = data[0]['weatherElement'][1]['time'][0]['parameter']['parameterName']
        card['body']['contents'][2]['contents'][1]['text'] = f"降雨機率 | {pop}%"
        # 舒適度
        ci = data[0]['weatherElement'][3]['time'][0]['parameter']['parameterName']
        card['body']['contents'][3]['contents'][1]['text'] = f"舒適度    | {ci}"

        flex_message = FlexSendMessage(
            alt_text='選單',
            contents = card
        )

        line_bot_api.reply_message(event.reply_token, flex_message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage("機器人忙碌中...請稍後再試!"))