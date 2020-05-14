import dlib
import cv2
import datetime
import threading
import firebase_admin
import RPi.GPIO as GPIO
from imutils import face_utils
from time import sleep
from pyfcm import FCMNotification
from firebase_admin import credentials
from firebase_admin import db

GPIO.setmode(GPIO.BCM)
GPIO.setup(12,GPIO.IN)

data = {
    "message_body": "현재 카메라 영상을 확인하려면 누르세요.",
    "message_title" : "얼굴이 인식되지 않았습니다!!",
    "click_action" : "Dialog"
    }

cred =credentials.Certificate("firebase-adminsdk.json")
firebase_admin.initialize_app(cred, {
    'databaseURL':'firebaseURL'})
DetectFace = db.reference('DetectFace')
emergency = db.reference('emergency')
stream = db.reference('Stream')
push_service = FCMNotification(api_key='FCM API Key')
#predict_model = 'shape_predictor_68_face_landmarks.dat'
face_detector = dlib.get_frontal_face_detector()
#landmark_predictor = dlib.shape_predictor(predict_model)
while(True):
    if stream.get().replace('\n','')=='Off':
        sleep(3)
        cap = cv2.VideoCapture(0)
        break;

def Alarm():
    sleep(5)
    if DetectFace.get().replace('\n','')=='1':
        emergency.set('Uncheck')
        
def check():
    while True:
        button_state = GPIO.input(12)
        if button_state == True: #button Push
            stream.set('Off')
            sleep(3)
            DetectFace.set('0')
            break

while (True):
    if stream.get().replace('\n','')=='On':
        cap.release()
        while True:
            if stream.get().replace('\n','')=='Off':
                sleep(3)
                cap = cv2.VideoCapture(0)
                break;
                    
    ret, frame =cap.read()
    frame = cv2.resize(frame,None,fx=0.5, fy=0.5,interpolation=cv2.INTER_AREA)
    frames= cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces = face_detector(frames,0)
    faces2= face_detector(cv2.flip(frames,0),0)
    if not faces and not faces2:
        print('no')
        Alarm_thread = threading.Thread(target=Alarm)
        button_thread = threading.Thread(target=check)
        cap.release()
        stream.set('On')
        DetectFace.set('1')
        push_service.notify_single_device(registration_id = 'Push Token',data_message=data)
        Alarm_thread.start()
        button_thread.start()
        while True:
            if DetectFace.get().replace('\n','')=='0':
                cap = cv2.VideoCapture(0)
                break
            
    else:
        print('yes')
#        for f in faces:
#            cv2.rectangle(frame,(f.left(),f.top()),(f.right(),f.bottom()),(0,255,0),2)
#            landmark = landmark_predictor(frame,f)
#            landmark = face_utils.shape_to_np(landmark)
#            for (i,(x,y)) in enumerate(landmark):
#                if i in range(48,68) or i in range(27,36):
#                    cv2.circle(frame,(x,y),2,(0,255,0),-1)
    
#    img = cv2.flip(frame,1)
#    cv2.imshow('frame',img)
#    sleep(0.02)
#    if cv2.waitKey(1) & 0xFF ==ord('q'):
#        break
#얼굴이 잡히는지만 확인하면 됬음으로 landmark(눈,코,입) 등을 굳이 확인할 필요가 없었다.
cap.release()
cv2.destroyAllWindows()
