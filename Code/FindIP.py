import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
test ="ifconfig | grep -w 192 | awk '{ print $2}'"

cred =credentials.Certificate("firebase-adminsdk.json")
firebase_admin.initialize_app(cred, {
    'databaseURL':'Firebase url'})
ref = db.reference('IpNum')
ref.set(os.popen(test).read())
