# %%
import requests
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import os

app = Flask(__name__)

line_bot_api = LineBotApi('LrMgKNTRX8uzQkt1r1npaphUVeaWjA519o4CGQ1WcQXW+67qKVntkLpiZ3CTSrClgd81vxQ35P9+0pjIhwlB0saVNpQWcSZpsSWXEVB/QDENpDKuOm/DT5HBW/JzEMxSLzCQqDXKWMpxuyLl9Dlx3QdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('fba10ff5fcef3748c499bedeb3529f21')


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    data = {
        "model":"llama2", 
        "prompt": event.message.text,
        "stream": False
    }
    response = requests.post('http://localhost:11434/api/generate', json=data).json()
    message = TextSendMessage(text=response["response"])
    line_bot_api.reply_message(event.reply_token, message)
    # stricker_message = StickerSendMessage(sticker_id=446, package_id=1988)
    # line_bot_api.reply_message(event.reply_token, stricker_message)


import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)