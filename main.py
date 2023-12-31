from flask import Flask, request, render_template
import json # 處理json
import serial  # 引用pySerial模組
from os import path
import threading
import time

# 載入 LINE Message API 相關函式庫
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# 處理arduino的部分
COM_PORT = 'COM5'    # 指定通訊埠名稱
BAUD_RATES = 115200    # 設定傳輸速率
ser = serial.Serial(COM_PORT, BAUD_RATES)   # 初始化序列通訊埠
file_path = './json_file/data.json' # 想儲存的檔案名稱
COM_PORT_2 = 'COM9'
ser_2 = serial.Serial(COM_PORT_2, BAUD_RATES)   # 初始化序列通訊埠
file_path_2 = './json_file/data2.json' # 想儲存的檔案名稱
# Line的部分
line_user_path = './Line_userid/user_id.json' # 儲存line好友的userid的位置
# Line_setting
#access_token = '你的 LINE Channel access token'
access_token = ''
#secret = '你的 LINE Channel secret'
secret = ''

# 中斷標誌，用來通知執行緒停止
stop_flag = threading.Event()

# json_file儲存的數據大小
json_Max_backut = 100

def occur_fire(userid, last, now, id, point):  
    line_bot_api = LineBotApi(access_token)      
    try:
        line_bot_api.push_message(userid, TextSendMessage(text=f'現在發生火災，地點在{point}區域'))
        return 'OK'
    except:
        print('error')

def get_update_data():
    while not stop_flag.is_set():
        time.sleep(1)
        try:
            ## 進行初始化
            if path.isfile(file_path) is False:
                with open(file_path, 'w') as file:
                    init_data = {}
                    init_data['total'] = json_Max_backut
                    init_data['count'] = 0
                    init_data['data'] = []
                    json.dump(init_data, file, indent=2)
            killed_key = 0
            listObj = []
            while killed_key == 0:
                while ser.in_waiting:     
                    data_raw = ser.readline()  
                    data = data_raw.decode()  
                    # str 轉 dict (json格式)
                    j = json.loads(data)
                    print('接收到的資料：', j)
                    temp = j["temp"]
                    hum = j["humidy"]
                    aqi = j["aqi"]
                    with open(file_path) as fp:
                        listObj = json.load(fp)          
                    total = listObj["total"] 
                    index = listObj["count"]
                    count = index
                    listObj["count"] = count + 1
                    print(total, index)
                    if(count > 0):
                        count = (count-1) % total
                        last_temp = listObj["data"][count]["temp"]
                        last_hum = listObj["data"][count]["humidy"]
                        if((aqi > 2000 and hum > last_hum) or temp > 50):
                            print("fire occur ?!")
                            if path.isfile(line_user_path) is True:
                                userid_buffer = []
                                with open(line_user_path) as fp:
                                    userid_buffer = json.load(fp)
                                    num = userid_buffer['count']
                                    for i in range(num):
                                        userid = userid_buffer['user'][i]['userid']  
                                        occur_fire(userid, last_temp, temp, (count+1)%total, "A")
                    num_index = index % total
                    if(index < total):
                        listObj["data"].append({
                            "temp": temp,
                            "humidy": hum,
                            "aqi": aqi
                        })
                    else:
                        listObj["data"][num_index]["temp"] = temp
                        listObj["data"][num_index]["humidy"] = hum
                        listObj["data"][num_index]["aqi"] = aqi
                    with open(file_path, 'w') as file:
                        json.dump(listObj, file, indent=2)

                    
        except KeyboardInterrupt:
            print("ctrl + C")
        except json.decoder.JSONDecodeError:
            print("接收到的數據不是有效的 JSON 格式")
        finally:
            ser.close()    # 清除序列通訊物件
            print("clear ser...")
def get_update_data_2():
    while not stop_flag.is_set():
        time.sleep(1)
        try:
            ## 進行初始化
            if path.isfile(file_path_2) is False:
                with open(file_path_2, 'w') as file:
                    init_data = {}
                    init_data['total'] = json_Max_backut
                    init_data['count'] = 0
                    init_data['data'] = []
                    json.dump(init_data, file, indent=2)
            killed_key = 0
            listObj = []
            if ser_2.in_waiting:     
                data_raw = ser_2.readline()
                data_raw = ser_2.readline()
                data_raw = ser_2.readline()
            while killed_key == 0:
                while ser_2.in_waiting:     
                    data_raw = ser_2.readline()  
                    data = data_raw.decode()  
                    # str 轉 dict (json格式)
                    j = json.loads(data)
                    print('接收到的資料：', j)
                    temp = j["temp"]
                    hum = j["humidy"]
                    aqi = j["aqi"]
                    with open(file_path_2) as fp:
                        listObj = json.load(fp)          
                    total = listObj["total"] 
                    index = listObj["count"]
                    count = index
                    listObj["count"] = count + 1
                    print(total, index)
                    if(count > 0):
                        count = (count-1) % total
                        last_temp = listObj["data"][count]["temp"]
                        last_hum = listObj["data"][count]["humidy"]
                        if((aqi > 2000 and hum > last_hum) or temp > 50):
                            print("fire occur ?!")
                            if path.isfile(line_user_path) is True:
                                userid_buffer = []
                                with open(line_user_path) as fp:
                                    userid_buffer = json.load(fp)
                                    num = userid_buffer['count']
                                    for i in range(num):
                                        userid = userid_buffer['user'][i]['userid']  
                                        occur_fire(userid, last_temp, temp, (count+1)%total, "B")
                    num_index = index % total
                    if(index < total):
                        listObj["data"].append({
                            "temp": temp,
                            "humidy": hum,
                            "aqi": aqi
                        })
                    else:
                        listObj["data"][num_index]["temp"] = temp
                        listObj["data"][num_index]["humidy"] = hum
                        listObj["data"][num_index]["aqi"] = aqi
                    with open(file_path_2, 'w') as file:
                        json.dump(listObj, file, indent=2)             
        except KeyboardInterrupt:
            print("ctrl + C")
        except json.decoder.JSONDecodeError:
            print("接收到的數據不是有效的 JSON 格式")
        
        finally:
            ser_2.close()    # 清除序列通訊物件
            print("clear ser...")

get_arduino_thread = threading.Thread(target=get_update_data)
get_arduino_thread_2 = threading.Thread(target=get_update_data_2)
@app.route("/", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)                    # 取得收到的訊息內容
    try:
        json_data = json.loads(body)                         # json 格式化訊息內容
        print(json_data)
        line_bot_api = LineBotApi(access_token)              # 確認 token 是否正確
        handler = WebhookHandler(secret)                     # 確認 secret 是否正確
        signature = request.headers['X-Line-Signature']      # 加入回傳的 headers
        handler.handle(body, signature)                      # 綁定訊息回傳的相關資訊

        # 加入好友時，儲存對方的userid
        # 刪除好友時，刪除對方的userid
        event_Is = json_data['events'][0]['type']
        if event_Is=="follow":
            print("this is a follow enevt")
            user_id = json_data['events'][0]['source']['userId']
            if path.isfile(line_user_path) is False:
                with open(line_user_path, 'w') as file:
                    init_data = {}
                    init_data['count'] = 0
                    init_data['user'] = []
                    json.dump(init_data, file, indent=2)
            listObj = []
            with open(line_user_path) as fp:
                listObj = json.load(fp)
                count = listObj["count"]
                listObj["count"] = listObj["count"] + 1
                listObj["user"].append({
                    "userid" : user_id
                })
            with open(line_user_path, 'w') as file:
                json.dump(listObj, file, indent=2)
        elif event_Is=="unfollow":
            user_id = json_data['events'][0]['source']['userId']
            if path.isfile(line_user_path) is True:
                listObj = []
                with open(line_user_path) as fp:
                    listObj = json.load(fp)
                    count = listObj['count']
                    listObj['count'] = listObj['count'] - 1
                    for i in range(count):
                        if listObj['user'][i]['userid'] == user_id:
                            print("delete a userid...")
                            del listObj['user'][i]
                            break
                with open(line_user_path, 'w') as file:
                    json.dump(listObj, file, indent=2)
    except:
        print(body)                                          # 如果發生錯誤，印出收到的內容
    return 'OK'                                              # 驗證 Webhook 使用，不能省略
@app.route("/json", methods=['GET', 'POST'])
def send_json():
    listObj = []
    with open("./json_file/data.json") as fp:
        listObj = json.load(fp) 
    return json.dumps(listObj)
@app.route("/json2", methods=['GET', 'POST'])
def send_json_2():
    listObj2 = []
    with open("./json_file/data2.json") as fp:
        listObj2 = json.load(fp) 
    return json.dumps(listObj2)
@app.route("/home", methods=['GET', 'POST'])
def home():
    return render_template("index.html")
@app.route("/test", methods=['GET', 'POST'])
def test():
    if path.isfile(line_user_path) is True:
        userid_buffer = []
        with open(line_user_path) as fp:
            userid_buffer = json.load(fp)
            num = userid_buffer['count']
            for i in range(num):
                userid = userid_buffer['user'][i]['userid'] 
                occur_fire(userid, 0, 0, 0, "hi") 
                print(userid)
    return 'OK'        

if __name__ == "__main__":
    try:
        if ser.in_waiting:     
            data_raw = ser.readline()
        if ser_2.in_waiting:     
            data_raw = ser_2.readline()
        get_arduino_thread_2.start()
        get_arduino_thread.start()
        app.run()
    except KeyboardInterrupt:
        print("ctrl + C")
    finally:
        get_arduino_thread.join()
        get_arduino_thread_2.join()
        print("success clear last process...\n")