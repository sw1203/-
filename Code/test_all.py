# -*- coding: utf-8 -*-
"""
Created on Wed May 15 18:22:38 2019

@author: sj
"""

import RPi.GPIO as GPIO
from time import sleep
import pyaudio
import threading
import wave 
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt
from pyfcm import FCMNotification

GPIO.setmode(GPIO.BCM)
GPIO.setup(12,GPIO.IN)

CHUNK = 4096
FORMAT = pyaudio.paInt16 
CHANNELS = 1 
RATE = 44000 
RECORD_SECONDS = 5 
OUTPUT_FILENAME = "voice.wav" 
push_service = FCMNotification(api_key='FCM API Key')

data_message = {
    "message_body" : "아기가 울고있어요",
    "message_title" : "울음소리 감지",
    "click_action" : "gg"
}

Button=1

def check_button():
    
    global Button
    
    while True:
        button_state=GPIO.input(12)
        if button_state == True:
            print('push')
            Button=0
            break
            
    
while(True):
    
    p = pyaudio.PyAudio() 

    stream = p.open(format=FORMAT, 
                    channels=CHANNELS, 
                    rate=RATE, 
                    input=True, 
                    frames_per_buffer=CHUNK) 


    print("* recording")        

    frames = [] 

    for i in range(0, int(RATE/CHUNK * RECORD_SECONDS)): 
        data = stream.read(CHUNK) 
        frames.append(data) 

    print("* done recording") 

    stream.stop_stream() 
    stream.close() 
    p.terminate() 

    wf = wave.open(OUTPUT_FILENAME, 'wb') 
    wf.setnchannels(CHANNELS) 
    wf.setsampwidth(p.get_sample_size(FORMAT)) 
    wf.setframerate(RATE) 
    wf.writeframes(b''.join(frames)) 
    wf.close() 


#import matplotlib.pyplot as plt



    sample_rate, data = wavfile.read(OUTPUT_FILENAME)

    spectrum, freqs, t, im = plt.specgram(data, Fs=sample_rate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))

# you can choose a frequency which you want to check

    index_of_frequency = np.where(freqs > 400)[0][0]

# find a sound data for a particular frequency

    data_for_frequency = spectrum[index_of_frequency]

# change a digital signal for a values in decibels

    data_in_db = 10 * np.log10(data_for_frequency)

#plt.figure(2)
#plt.plot(t, data_in_db, linewidth=1, alpha=0.7, color='#004bc6')
#plt.xlabel('Time (s)')
#plt.ylabel('Power (dB)')

# find a index of a max value

    index_of_max = np.argmax(data_in_db)
#print(index_of_max)

    value_of_max = data_in_db[index_of_max]
    print(value_of_max)

    if(value_of_max>20):
        print ('alarm')
        button_thread = threading.Thread(target=check_button)
        result = push_service.notify_single_device(registration_id='Push Token',
                                           data_message=data_message)
        button_thread.start()
        while True:
            if Button == 0:
                Button=1
                break
            
            elif Button == 1:
                sleep(10)
                if Button==1:
                    push_service.notify_single_device(registration_id='Push Token',
                                           data_message=data_message)
                else:
                    break
    

