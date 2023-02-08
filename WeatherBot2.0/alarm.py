from crud import get_alarm_user, check_region
from function import get_weather
import views
from linebot.models import TextSendMessage, ImageSendMessage
import schedule
from time import sleep

def alarm():
    data_list = get_alarm_user()
    for data in data_list:
        user_id = data.user_id

        region = check_region(user_id=user_id)
        today, today_sunrise, today_sunset, today_maximum, today_least, today_morning, today_afternoon, today_weather_img,tomorrow, tomorrow_sunrise, tomorrow_sunset, tomorrow_maximum, tomorrow_least, tomorrow_morning, tomorrow_afternoon, tomorrow_weather_img,tomorrow_comment = get_weather(region=region)
        views.line_bot_api.push_message(
                user_id,
                [TextSendMessage(text=f'【今日/{today}の天気予報】\n日の出:{today_sunrise}\n日の入:{today_sunset}\n最高気温:{today_maximum}℃\n最低気温:{today_least}℃\n午前降水確率:{today_morning}%\n午後降水確率:{today_afternoon}%'),ImageSendMessage(original_content_url=today_weather_img, preview_image_url=today_weather_img),
                TextSendMessage(text=f'【明日/{tomorrow}の天気予報】\n日の出:{tomorrow_sunrise}\n日の入:{tomorrow_sunset}\n最高気温:{tomorrow_maximum}℃\n最低気温:{tomorrow_least}℃\n午前降水確率:{tomorrow_morning}%\n午後降水確率:{tomorrow_afternoon}%'),ImageSendMessage(original_content_url=tomorrow_weather_img, preview_image_url=tomorrow_weather_img),
                TextSendMessage(text=f'【明日/{tomorrow}のコメント】\n{tomorrow_comment}')]
            )

schedule.every().day.at('6:00').do(alarm)
while True:
    schedule.run_pending()
    sleep(1)