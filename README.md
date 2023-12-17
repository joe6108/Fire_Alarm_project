## 執行步驟

1. download all package...

- `pip install Flask`
- `pip install pyserial`

2. 打開Arduino_data_collect，編譯上傳arduino code。

3. 執行python腳本，輸入`python main.py`。

4. 打開下方的網址連結。

## 其餘事項

如要使用外網，那就需要更改index.html的url1以及url2

Line_bot也是，需要更改
#access_token = '你的 LINE Channel access token'
#secret = '你的 LINE Channel secret'

而arduino則需要更改序列阜

## 注意事項

必須透過按鈕先停止數據收集，否則不知會發生什麼事。
 
## 功能

- arduino將數據打包成json檔傳送至序列阜。
- python腳本可以透過序列阜抓取json格式的str。
- 簡易的網頁設計。
- 一個簡易的伺服器。
- 伺服器可以以非同步的方式同時執行python腳本&運行網頁框架。
- 可以透過按鈕去中斷資料收集的部分。

