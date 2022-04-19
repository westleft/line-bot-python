from typing import Text
from linebot.models import TextSendMessage, FlexSendMessage
from models.message_request import MessageRequest
from skills import add_skill
from helpers.googlemap import GoogleMapSearch
import googlemaps
import json

@add_skill('美食地圖')
def get(message_request: MessageRequest):
    latitude = message_request.intent.split(' ')[1]
    longitude = message_request.intent.split(' ')[2]
    location = (latitude, longitude)
    radius = 5000
    map = GoogleMapSearch(location, radius)
    resturants = map.get_info()


    data = []
    for item in resturants:
        messageTemplete = json.load(open('./messages/resturant.json', 'r', encoding='utf-8'))

        messageTemplete['hero']['url'] = item['photo']
        messageTemplete['body']['contents'][0]['text'] = item['name']
        messageTemplete['body']['contents'][1]['contents'][5]['text'] =  str(item['rating'])

        for i in range(5):
            print(f"第{i}")
            if(i < item['rating']):
                print(f"金色")
                messageTemplete['body']['contents'][1]['contents'][i]['url'] = "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
            else:
                print(f"灰色")
                messageTemplete['body']['contents'][1]['contents'][i]['url'] = "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png"

        # messageTemplete['footer']['contents'][0]['action']['uri'] = f"https://www.google.com/maps/place?q={item['name']}"
        data.append(messageTemplete)

        if(len(data) == 12):
            break

    flex_message = FlexSendMessage(
        alt_text='美食選單',
        contents = {
            "type": "carousel",
            "contents": data
        }
    )

    return [
        flex_message,
    ]