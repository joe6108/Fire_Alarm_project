from flask import Flask, request, render_template
import json # 處理json
import serial  # 引用pySerial模組
from os import path
import threading
import time

app = Flask(__name__)

# 處理arduino的部分
COM_PORT = 'COM5'    # 指定通訊埠名稱
BAUD_RATES = 115200    # 設定傳輸速率
#ser = serial.Serial(COM_PORT, BAUD_RATES)   # 初始化序列通訊埠
file_path = './json_file/data.json' # 想儲存的檔案名稱
listObj = []

# 中斷標誌，用來通知執行緒停止
stop_flag = threading.Event()

# json_file儲存的數據大小
json_Max_backut = 30

def get_update_data():
    temp_change_parm = 0
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

            while killed_key == 0:
                while ser.in_waiting:          
                    data_raw = ser.readline()  
                    data = data_raw.decode()  
                    #print('接收到的原始資料：', data_raw)
                    # str 轉 dict (json格式)
                    j = json.loads(data)
                    print('接收到的資料：', j)
                    temp = j["temp"]
                    hum = j["humidy"]
                    killed_key = j["killed_key"]
                    if killed_key == 1:
                        # 在某個時間點手動設置中斷標誌，通知執行緒停止
                        time.sleep(5)
                        stop_flag.set()
                        break
                    with open(file_path) as fp:
                        listObj = json.load(fp)          
                    total = listObj["total"] 
                    index = listObj["count"]
                    count = index + 1
                    print(total, index)
                    listObj["count"] = count

                    ## 測試參數，用於觀測循環存入是否成功
                    temp_change_parm += 1
                    temp += temp_change_parm
                    hum -= temp_change_parm

                    if(index < total):
                        listObj["data"].append({
                            "temp": temp,
                            "humidy": hum
                        })
                    else:
                        index %= total
                        listObj["data"][index]["temp"] = temp
                        listObj["data"][index]["humidy"] = hum
                    with open(file_path, 'w') as file:
                        json.dump(listObj, file, indent=2)
        except KeyboardInterrupt:
            print("ctrl + C")

get_arduino_thread = threading.Thread(target=get_update_data)

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template("index.html")
@app.route("/json", methods=['GET', 'POST'])
def send_json():
    listObj = []
    with open("./json_file/data.json") as fp:
        listObj = json.load(fp) 
    return json.dumps(listObj)

if __name__ == "__main__":
    try:
        #get_arduino_thread.start()
        app.run()
    finally:
        stop_flag.set()
        #get_arduino_thread.join()
        #ser.close()    # 清除序列通訊物件
        print("success clear last process...\n")