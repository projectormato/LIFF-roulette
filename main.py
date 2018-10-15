from flask import Flask, request, abort, render_template, make_response
from flask_bootstrap import Bootstrap
import os, uuid, base64

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

from PIL import Image
import warnings
warnings.simplefilter('error', Image.DecompressionBombWarning)

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/sketch")
def sketch():
    return render_template('sketch.html')


line_bot_api = LineBotApi(os.environ.get('ACCESS_TOKEN'))
handler = WebhookHandler(os.environ.get('CHANNEL_SECRET'))

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
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == '決断':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=os.environ.get('DECISION_LIFF_APP')))
    elif event.message.text == 'お絵かき':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=os.environ.get('SKETCH_LIFF_APP')))

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=int(os.environ.get("PORT",5000)))
