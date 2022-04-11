from typing import Text
from linebot.models import TextSendMessage
from models.message_request import MessageRequest
from linebot.models import TextSendMessage, FlexSendMessage
from skills import add_skill
import requests
import json


@add_skill('天氣縣市')
def get(message_request: MessageRequest):
    card = json.load(open('./messages/weather.json', 'r', encoding='utf-8'))
    city = message_request.intent.split(' ')[1]

    try:
        # 爬蟲
        payload = {}
        headers = {
            'accept': 'application/json',
            'Cookie': 'TS01dbf791=0107dddfefdf0f1de44404bb56e72168df5349707ba3cafde81e1f03ac000dfc0911fe61d63e070e61a9e1def9310ee8e687eebeeb'
        }

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
        card['body']['contents'][3]['contents'][1]['text'] = f"舒適度 | {ci}"

        flex_message = FlexSendMessage(
            alt_text='選單',
            contents = card
        )

        return [
            flex_message
        ]
    except:
        return [
            TextSendMessage(text='機器人忙碌中...請稍後再試!')
        ]