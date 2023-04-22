# LINE_ChatBot_AWS

## 実行方法
```
pip install -r requirements.txt -t ./lambda
cd lambda
zip -r python.zip ./*
```
python.zip を lambda あげる

## 環境構築
LINE_CHANNEL_ACCESS_TOKEN, LINE_CHANNEL_SECRET, YOUR_OPENAI_APIKEY の三種類を lambda関数 -> 設定 -> 環境変数に登録

## メモ
LINE bot 側や AWS の API Gateway, lambda の設定を時間があれば書く
