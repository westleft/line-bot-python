from typing import Text
from linebot.models import FlexSendMessage, TextSendMessage
from models.message_request import MessageRequest
from skills import add_skill
from bs4 import BeautifulSoup
import json
import requests
import urllib


@add_skill('查看本周新片')
def get(message_request: MessageRequest):
    url = 'https://movies.yahoo.com.tw/movie_thisweek.html'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}

    res = requests.get(url, headers=headers)
    soups = BeautifulSoup(res.text, 'html.parser').find(
        class_='release_list').find_all('li')

    data = []
    for soup in soups:
        messageTemplete = json.load(open('./messages/movie.json', 'r', encoding='utf-8'))
        # 電影名
        title = soup.find(class_='release_movie_name').find('a').text.replace(' ','').replace('\n', '')
        messageTemplete['body']['contents'][0]['text'] = title

        # 封面照
        img = soup.find('img')['data-src']
        messageTemplete['hero']['url'] = img

        # 上映時間
        showDate = soup.find(class_='release_movie_time').text.replace(' ','').replace('\n', '')
        messageTemplete['body']['contents'][1]['contents'][0]['text'] = showDate

        # 電影簡介
        discription = soup.find(class_='release_text').text.replace(' ','').replace('\n', '')[0: 45] + '...'
        messageTemplete['body']['contents'][2]['contents'][0]['text'] = discription

        # 預告片連結
        url = f'https://www.youtube.com/results?search_query={urllib.parse.quote(title)}'
        messageTemplete['footer']['contents'][0]['action']['uri'] = url

        data.append(messageTemplete)
        # print(url)
    flex_message = FlexSendMessage(
        alt_text='本周電影新片單',
        contents = {
            "type": "carousel",
            "contents": data
        }    
    )

    return [
        flex_message
    ]
