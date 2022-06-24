#引用必要套件
import requests , json , time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

with open('apikey.txt','r') as f:
 apikey = f.read()

city_num=[["宜蘭縣", 3369296],["桃園市", 3369297], ["新竹縣", 3369298], ["苗栗縣", 3369299], ["彰化縣", 3369300], ["南投縣", 3369301], ["雲林縣", 3369302], ["嘉義縣", 3369303], ["屏東縣", 3369304], ["臺東縣", 3369305], ["花蓮縣", 3369306], ["澎湖縣", 3369307], ["基隆市", 312605], ["新竹市", 313567], ["嘉義市", 312591], ["臺北市", 315078], ["高雄市", 313812], ["新北市", 2515397], ["臺中市", 315040], ["臺南市", 314999], ["連江縣", 3369309], ["金門縣", 2332525]]

cred = credentials.Certificate("firebase_key.json") # 引用私密金鑰
firebase_admin.initialize_app(cred)                                     # 初始化firebase，注意不能重複初始化
db = firestore.client()                                                 # 初始化firestore

nowTime = int(time.time())                                              #初始unix系統時間到現在時間的秒數
struct_time = time.localtime(nowTime)                                   #以tuple方式轉換秒數至現今時間
timeString = time.strftime("%Y-%m-%d-%I:%M:%S-%P", struct_time)         #把現今時間轉換至特定格式

def get_weather_into_firebase_hourly():                                        #從url中拿取資料，並寫入到資料庫
    for code_number in city_num:
        url = "http://dataservice.accuweather.com/forecasts/v1/hourly/1hour/{}?apikey={}&language=zh-tw".format(code_number[1],apikey)  #擷取資料的url
        data = requests.get(url).json()                 #再用requests取出來，並轉換成json檔案的形式
        city_name = code_number[0]
        doc_ref = db.collection("weather_data").document(city_name)     #在firebase中創建集合以及文件
        doc_ref.set({"天氣資料":data})                                 #以({"天氣資料":data})在文件裡新增欄位

get_weather_into_firebase_hourly()