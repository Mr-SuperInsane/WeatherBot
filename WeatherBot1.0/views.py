from flask import request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, FollowEvent,
    TextMessage, TextSendMessage, FlexSendMessage, ImageSendMessage, TemplateSendMessage, ConfirmTemplate, MessageAction
)
import json

from app import app
from crud import check_person, add_person, check_region, upgrade_region
from function import get_weather

line_bot_api = LineBotApi('KfnKU7XCuJfM16hCFerNyxLxeNZ2euAged/MG8PYmt6pfaTAi/r90+aUEDxGAa649NvVdbrLN+u8hsBw7hzvWDXFaUep2yqRZ3x1WMeJjjf/HcYhPqnC3SJqN8QwwyRoB5j0W6k9J3aTwZbRgia4XgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('97f246036a53aa0f878d19c5bc86ab3b')

region_list = ['大阪','能勢','豊中','枚方','東大阪','堺','岸和田','河内長野','阪南','城崎','豊岡','丹波','朝来','姫路','神戸','明石','宝塚','尼崎','北淡','南淡','京都','宮津','舞鶴','福知山','和知','亀岡','宇治','八幡','城陽','余呉','長浜','高島','彦根','米原','堅田','近江八幡','大津','甲賀','奈良','大和高田','橿原','桜井','五條','吉野','大台ヶ原山','十津川','和歌山','橋本','有田','御坊','田辺','中辺路','白浜','串本','新宮','四日市','鈴鹿','伊賀','津','名張','伊勢','鳥羽','志摩','尾鳶','熊野']

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    get_message = event.message.text
    user_id = event.source.user_id
    return_message = check_person(user_id)
    if get_message in region_list:
        if return_message == 'True':
            # ユーザーIDがDBに存在する
            line_bot_api.reply_message(
                event.reply_token,
                [TextSendMessage(text='登録地域を変更したい場合は「はい」を選択してください。'),TextSendMessage(text='誤操作の場合は「いいえ」を押してください。'),
                TemplateSendMessage(
                    alt_text='登録地域を変更しますか？',
                    template=ConfirmTemplate(
                        text='登録地域を変更しますか？',
                        actions=[
                            # 「はい」の場合はポストバックアクションの処理でデータベースを更新・「いいえ」の場合は何もしない
                            MessageAction(
                                label='はい',
                                text=f'{get_message}に変更する'
                            ),
                            MessageAction(
                                label='いいえ',
                                text=f'{get_message}に変更しない'
                            )
                        ]
                    )
                )]
            )
        else:
            # ユーザーIDがDBに存在しない
            add_person(user_id=user_id, region=get_message)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='地域が登録されました。天気予報のデータを取得する場合や登録地域を変更する場合はメニューから操作してください。')
            )

    elif 'に変更する' in get_message:
        update_region = get_message.replace('に変更する','')
        upgrade_region(user_id=user_id, update_region=update_region)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f'地域を{update_region}に変更しました')
        )

    elif 'に変更しない' in get_message:
        pass

    elif get_message == '天気予報':
        if return_message == 'True':
            #データベースに存在する場合
            region = check_region(user_id=user_id)
            url, today, today_sunrise, today_sunset, today_maximum, today_least, today_morning, today_afternoon, today_weather_img,tomorrow, tomorrow_sunrise, tomorrow_sunset, tomorrow_maximum, tomorrow_least, tomorrow_morning, tomorrow_afternoon, tomorrow_weather_img,tomorrow_comment = get_weather(region=region)
            line_bot_api.reply_message(
                event.reply_token,
                [TextSendMessage(text=f'【今日/{today}の天気予報】\n日の出:{today_sunrise}\n日の入:{today_sunset}\n最高気温:{today_maximum}℃\n最低気温:{today_least}℃\n午前降水確率:{today_morning}%\n午後降水確率:{today_afternoon}%'),ImageSendMessage(original_content_url=today_weather_img, preview_image_url=today_weather_img),
                TextSendMessage(text=f'【明日/{tomorrow}の天気予報】\n日の出:{tomorrow_sunrise}\n日の入:{tomorrow_sunset}\n最高気温:{tomorrow_maximum}℃\n最低気温:{tomorrow_least}℃\n午前降水確率:{tomorrow_morning}%\n午後降水確率:{tomorrow_afternoon}%'),ImageSendMessage(original_content_url=tomorrow_weather_img, preview_image_url=tomorrow_weather_img),
                TextSendMessage(text=f'【明日/{tomorrow}のコメント】\n{tomorrow_comment}')]
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='地域を選択して登録してください。')
            )

    elif get_message == '地域変更':
        if return_message == 'True':
            flex_message_open = open('flex_message.txt','r',encoding='utf-8')
            flex_message_json = json.load(flex_message_open)
            line_bot_api.reply_message(
                event.reply_token,
                [TextSendMessage(text='変更する地域を選択してください。'),
                FlexSendMessage(alt_text='地域を選択してください',contents=flex_message_json)]
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='地域を選択して登録してください。')
            )
    
    elif get_message == '登録情報':
        region = check_region(user_id=user_id)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f'地域:{region}')
        )

    elif get_message == 'アラーム設定':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='現在アラーム機能は開発中のため利用できません。')
        )

    #対応外のメッセージの場合
    else:
        if return_message == 'True':
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='天気予報のデータを取得する場合や登録地域を変更する場合はメニューから操作してください。')
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='地域を選択して登録してください。')
            )



    '''
    line_bot_api.reply_message(
        event.reply_token,
        [TextSendMessage(text=f'【{today}の天気予報】\n日の出:{today_sunrise}\n日の入:{today_sunset}\n最高気温:{today_maximum}℃\n最低気温:{today_least}℃\n午前降水確率:{today_morning}%\n午後降水確率:{today_afternoon}%'),ImageSendMessage(original_content_url=today_weather_img, preview_image_url=today_weather_img),
        TextSendMessage(text=f'【{tomorrow}の天気予報】\n日の出:{tomorrow_sunrise}\n日の入:{tomorrow_sunset}\n最高気温:{tomorrow_maximum}℃\n最低気温:{tomorrow_least}℃\n午前降水確率:{tomorrow_morning}%\n午後降水確率:{tomorrow_afternoon}%'),ImageSendMessage(original_content_url=tomorrow_weather_img, preview_image_url=tomorrow_weather_img),
        TextSendMessage(text=f'【{tomorrow}のコメント】\n{tomorrow_comment}')
        ]
    '''

#あいさつメッセージ(アカウント追加時に自動送信)
@handler.add(FollowEvent)
def follow_message(event):
    if event.type == 'follow':
        flex_message_open = open('flex_message.txt','r',encoding='utf-8')
        flex_message_json = json.load(flex_message_open)
        line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage(text='WeatherBotを追加していただきありがとうございます。始めにお住まいの都道府県を選択してください。'),
            FlexSendMessage(alt_text='地域を選択してください',contents=flex_message_json)]
        )

if __name__ == "__main__":
    app.run(debug=True)