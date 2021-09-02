from flask import Flask, request, abort #架設伺服器用

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

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
    if ['熊哥', '貝卡'] in msg: #以下皆為訊息判別式
        msg = TextSendMessage(text='好帥')
    line_bot_api.reply_message(event.reply_token,msg)


if __name__ == "__main__":
    app.run()