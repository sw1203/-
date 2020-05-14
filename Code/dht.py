import Adafruit_DHT
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import datetime

dht_type=22 #DHT타입
bcm_pin=23  #핀 번호

cred =credentials.Certificate("firebase-adminsdk.json")
firebase_admin.initialize_app(cred, {
    'databaseURL':'FirebaseURL'})
ref = db.reference('humitemp')

while True:
    humidity, temperature=Adafruit_DHT.read_retry(dht_type, bcm_pin)
    humid=str(round(humidity,1))
    temp=str(round(temperature,1))
    ref.push('온도: '+temp+", 습도: "+humid+"\t시간: "+str(datetime.datetime.now()).split('.')[0])
    time.sleep(3)
        
