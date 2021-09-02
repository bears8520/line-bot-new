from flask import Flask, request, abort #架設伺服器用

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, TemplateSendMessage, ButtonsTemplate, URITemplateAction
)
import random

app = Flask(__name__)

#放上API的KEY
line_bot_api = LineBotApi('7CbFNT/tzPu/tFGNYX/wOFBbpO8TfVyY7JZWZkig58JbFuGd0RTNHZjjGiv3y6s/s/JMPGTKb3LUgzVULJgdHDQKP++slrmqvgRfE2MyIGAKIBvWYosSjJuWbGC0WT/USieMLIauE3oinLh27duUdQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('deafe6c5de383d0f1705e1014ffc0ba2')


@app.route("/callback", methods=['POST'])
#將資料callback回去給使用者
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
    msg = event.message.text
    girls = []
    with open('girls.txt', 'r', encoding='utf-8-sig') as f:
        for girl in f:
            girls.append(girl.strip()) #將文件內的字一行一行放入list
    i = random.choice(girls)#隨機從list中拿出一個

    if msg in ['熊哥', '貝卡']: #以下皆為訊息判別式
        msg = TextSendMessage(text='好帥')
    elif msg == '抽':#回傳圖片
        msg = ImageSendMessage(
        original_content_url=i, 
        preview_image_url=i
    )
    elif msg in ['抽屁', '幹', '機器人閉嘴', '閉嘴', '靠', '低能']:
        msg = TextSendMessage(text='炒殺小?')
    elif '87' in msg:
        msg = TextSendMessage(text='你才87')
    elif '想我的+1' in msg:
        msg = TextSendMessage(text='+1')
    elif msg == '!貝卡': #選單製造
        msg = TemplateSendMessage(
            alt_text='請用手機操作選單',
            template=ButtonsTemplate(
                thumbnail_image_url='https://i.imgur.com/GAghGccl.jpg',
                title='嗨~',
                text='你今天想要什麼<3?',
                actions=[
                    URITemplateAction(
                        label='貝卡小屋',
                        uri='https://home.gamer.com.tw/homeindex.php?owner=jiff852'
                    ),
                    URITemplateAction(
                        label='貝卡FB粉專',
                        uri='https://www.facebook.com/bears0518/'
                    ),
                    URITemplateAction(
                        label='貝卡YouTube',
                        uri='https://www.youtube.com/channel/UC4TlloLCVjhIyXoBTmDIPFw'
                    )
                ]
            )
        )
    line_bot_api.reply_message(event.reply_token,msg)


if __name__ == "__main__":
    app.run()