from linebot import (
    LineBotApi,
    WebhookHandler,
)
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent,
    FollowEvent,
    TextMessage,
    TextSendMessage,
)
import os
import openai


# 環境変数取得
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]
YOUR_OPENAI_APIKEY = os.environ["YOUR_OPENAI_APIKEY"]

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

DEFAULT_EN_SYSTEM_MESSAGE = "You are a helpful assistant."
DEFAULT_JA_SYSTEM_MESSAGE = "あなたは優秀なアシスタントです。"


def lambda_handler(event, context):
    # get X-Line-Signature header value
    signature = event["headers"]["x-line-signature"]
    body = event["body"]

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        return {
            "statusCode": 400,
            "body": "Invalid signature"
        }

    return {
        "statusCode": 200,
        "body": "OK"
    }


@handler.add(FollowEvent)
def handle_follow(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=help_message())
    )


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    response_text = choose_response(event.message.text)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=response_text)
    )


def choose_response(text):
    command = text.split(" ")[0]

    if command not in ["h", "help", "s", "gpt-4", "gpt-3.5-turbo"]:
        return "有効なコマンドではありません。hまたはhelpでコマンド一覧を表示します。"
    elif command == "h" or command == "help":
        response = help_message()

    elif command == "s":
        response = "sコマンドは現在開発中です。"

    elif command == "gpt-4" or command == "gpt-3.5-turbo":
        try:
            language = text.split(" ")[1]
            input_text = " ".join(text.split(" ")[2:])
        except IndexError:
            return "コマンドの形式が間違っています。hまたはhelpでコマンド一覧を表示します。"

        response = chat_completion(command, language, input_text)

    return response


def help_message():
    f = open("help_message.txt", "r")
    help_txt = f.read()
    f.close()
    return help_txt


def chat_completion(model, language, text):
    openai.api_key = YOUR_OPENAI_APIKEY
    if language == "en":
        system_massage = DEFAULT_EN_SYSTEM_MESSAGE
    elif language == "ja":
        system_massage = DEFAULT_JA_SYSTEM_MESSAGE
    else:
        return "対応言語は en または ja の2種類です。hまたはhelpでコマンド一覧を表示します。"

    messages = [
        {"role": "system", "content": system_massage},
        {"role": "user", "content": text}
    ]
    completion = openai.ChatCompletion.create(
        model=model,
        messages=messages
    )
    response = completion.choices[0].message["content"]
    return response


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
