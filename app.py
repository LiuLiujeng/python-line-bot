from flask import Flask, request, abort

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

line_bot_api = LineBotApi('Pa0KGreTE3P9YG3Vv7x27SzC3MsKF8JXIT9jxeHf2JUM6c1STuNjdwamZgoIWVFBseQDmpNeOonbgEExlyG3rgyWOhZDX48e0/15WzntiQRpUMqDt+l3AITb3NX4/oblJks5kCalGOlJDzIuexfSpwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('e5788a58601431797a4549f2fe9758a1')


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
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
