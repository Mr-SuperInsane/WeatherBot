import requests
from bs4 import BeautifulSoup
import json

with open('region_url.json', 'r', encoding='utf-8')as file:
    region_url_dict = json.load(file)

def get_weather(region):
    url = region_url_dict[region]
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    today = soup.select('#card_forecast > div:nth-of-type(2) > div > div.switchContent > div:nth-of-type(1) > section > div > div.wTable__body > div:nth-of-type(1) > div.wTable__day > p')[0].contents[0]
    today_sunrise = soup.select('#card_forecast > div:nth-of-type(2) > div > div.switchContent > div:nth-of-type(1) > section > div > div.wTable__body > div:nth-of-type(1) > div.wTable__content > div > div:nth-of-type(1) > div.day2Table__item.day2Info.no-global > ul > li:nth-of-type(1)')[0].contents[0]
    today_sunset = soup.select('#card_forecast > div:nth-of-type(2) > div > div.switchContent > div:nth-of-type(1) > section > div > div.wTable__body > div:nth-of-type(1) > div.wTable__content > div > div:nth-of-type(1) > div.day2Table__item.day2Info.no-global > ul > li:nth-of-type(2)')[0].contents[0]
    today_maximum = soup.select('#card_forecast > div:nth-of-type(2) > div > div.switchContent > div:nth-of-type(1) > section > div > div.wTable__body > div:nth-of-type(1) > div.wTable__content > div > div:nth-of-type(2) > div:nth-of-type(1) > p > span.text.wTable__item')[0].contents[0]
    today_least = soup.select('#card_forecast > div:nth-of-type(2) > div > div.switchContent > div:nth-of-type(1) > section > div > div.wTable__body > div:nth-of-type(1) > div.wTable__content > div > div:nth-of-type(2) > div:nth-of-type(2) > p > span.text.wTable__item')[0].contents[0]
    today_morning = soup.select('#card_forecast > div:nth-of-type(2) > div > div.switchContent > div:nth-of-type(1) > section > div > div.wTable__body > div:nth-of-type(1) > div.wTable__content > div > div:nth-of-type(3) > div:nth-of-type(1) > p > span.text.wTable__item')[0].contents[0]
    today_afternoon = soup.select('#card_forecast > div:nth-of-type(2) > div > div.switchContent > div:nth-of-type(1) > section > div > div.wTable__body > div:nth-of-type(1) > div.wTable__content > div > div:nth-of-type(3) > div:nth-of-type(2) > p > span.text.wTable__item')[0].contents[0]
    today_weather_img = soup.select('#card_forecast > div:nth-of-type(2) > div > div.switchContent > div:nth-of-type(1) > section > div > div.wTable__body > div:nth-of-type(1) > div.wTable__content > div > div:nth-of-type(1) > div.day2Table__item.weather')[0].find('img').get('src')
    today_weather_img = 'https:' + str(today_weather_img)
    tomorrow = soup.select('#card_forecast > div:nth-of-type(2) > div > div.switchContent > div:nth-of-type(1) > section > div > div.wTable__body > div:nth-of-type(2) > div.wTable__day > p')[0].contents[0]
    tomorrow_sunrise = soup.select('#card_forecast > div:nth-of-type(2) > div > div.switchContent > div:nth-of-type(1) > section > div > div.wTable__body > div:nth-of-type(2) > div.wTable__content > div > div:nth-of-type(1) > div.day2Table__item.day2Info.no-global > ul > li:nth-of-type(1)')[0].contents[0]
    tomorrow_sunset = soup.select('#card_forecast > div:nth-of-type(2) > div > div.switchContent > div:nth-of-type(1) > section > div > div.wTable__body > div:nth-of-type(2) > div.wTable__content > div > div:nth-of-type(1) > div.day2Table__item.day2Info.no-global > ul > li:nth-of-type(2)')[0].contents[0]
    tomorrow_maximum = soup.select('#card_forecast > div:nth-of-type(2) > div > div.switchContent > div:nth-of-type(1) > section > div > div.wTable__body > div:nth-of-type(2) > div.wTable__content > div > div:nth-of-type(2) > div:nth-of-type(1) > p > span.text.wTable__item')[0].contents[0]
    tomorrow_least = soup.select('#card_forecast > div:nth-of-type(2) > div > div.switchContent > div:nth-of-type(1) > section > div > div.wTable__body > div:nth-of-type(2) > div.wTable__content > div > div:nth-of-type(2) > div:nth-of-type(2) > p > span.text.wTable__item')[0].contents[0]
    tomorrow_morning = soup.select('#card_forecast > div:nth-of-type(2) > div > div.switchContent > div:nth-of-type(1) > section > div > div.wTable__body > div:nth-of-type(2) > div.wTable__content > div > div:nth-of-type(3) > div:nth-of-type(1) > p > span.text.wTable__item')[0].contents[0]
    tomorrow_afternoon = soup.select('#card_forecast > div:nth-of-type(2) > div > div.switchContent > div:nth-of-type(1) > section > div > div.wTable__body > div:nth-of-type(2) > div.wTable__content > div > div:nth-of-type(3) > div:nth-of-type(2) > p > span.text.wTable__item')[0].contents[0]
    tomorrow_weather_img = soup.select('#card_forecast > div:nth-of-type(2) > div > div.switchContent > div:nth-of-type(1) > section > div > div.wTable__body > div:nth-of-type(2) > div.wTable__content > div > div:nth-of-type(1) > div.day2Table__item.weather')[0].find('img').get('src')
    tomorrow_comment = soup.select('#card_forecast > div:nth-of-type(2) > div > div.switchContent > div.switchContent__item.act > div > p:nth-of-type(2)')[0].contents[0]
    tomorrow_weather_img = 'https:' + str(tomorrow_weather_img)

    return today, today_sunrise, today_sunset, today_maximum, today_least, today_morning, today_afternoon, today_weather_img,tomorrow, tomorrow_sunrise, tomorrow_sunset, tomorrow_maximum, tomorrow_least, tomorrow_morning, tomorrow_afternoon, tomorrow_weather_img,tomorrow_comment
