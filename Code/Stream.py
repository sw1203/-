import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from subprocess import call

cred =credentials.Certificate("firebase-adminsdk.json")
firebase_admin.initialize_app(cred, {
    'databaseURL':'firebase_URL'})
ref = db.reference('Stream')
while(True):
    if(ref.get().replace('\n','')=="On"):
        call(['bash','Stream.sh'])
    elif(ref.get().replace('\n','')=="Off"):
        call(['bash','StopStream.sh'])
        
