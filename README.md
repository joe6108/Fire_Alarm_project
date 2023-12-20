## 執行步驟

1. download all package...

- `pip install Flask`
    - 用於快速建立server
- `pip install pyserial`
    - 用於arduino序列阜
- `pip install line-bot-sdk` 
    - 用於line bot

2. 打開Arduino_data_collect，編譯上傳arduino code。

3. 執行python腳本，輸入`python main.py`。

4. 打開下方的網址連結。

## 其餘事項

如要使用外網(如使用ngrok轉成外部ip)，那就需要更改index.html的url1以及url2

Line_bot也是，需要更改
#access_token = '你的 LINE Channel access token'
#secret = '你的 LINE Channel secret'

而arduino則需要更改序列阜

## 注意事項

無
 
## 功能

- arduino將數據打包成json檔傳送至序列阜。
- python腳本可以透過序列阜抓取json格式的str。
- 簡易的網頁設計。
- 一個簡易的伺服器。
- 伺服器可以以非同步的方式同時執行python腳本&運行網頁框架。

## 2023/12/18

將單個arduino運作變為兩個arduino同時運作並讀取資料，只剩完成寄送訊息給line_bot的部分。

