import random
import socketio
import eventlet
import numpy as np
from flask import Flask
from keras.models import load_model
import base64
from io import BytesIO
from PIL import Image
import cv2
import json
import threading
import uuid
import time
from datetime import datetime
import pytz
from confluent_kafka import Producer

sio = socketio.Server()
app = Flask(__name__) #'__main__'
speed_limit = 10

p = Producer({'bootstrap.servers': 'localhost:9092'})
# GEO Data
input_file = open ('geo.json')
json_array = json.load(input_file)
index: int = 0
carkey = '"000001"'
carid = '000001'
data = {}
data['selfdrivingcar'] = '000001'

#GENERATE UUID
def generate_uuid():
    return uuid.uuid4()

def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: {0}: {1}"
              .format(msg.value(), err.str()))
    else:
        print("Message produced: {0}".format(msg.value()))
    
    print("delivery_callback. error={}. message={}".format(err, msg))
    print("message.topic={}".format(msg.topic()))
    print("message.timestamp={}".format(msg.timestamp()))
    print("message.key={}".format(msg.key()))
    print("message.value={}".format(msg.value()))
    print("message.partition={}".format(msg.partition()))
    print("message.offset={}".format(msg.offset()))


def sendit2Kafka():
    global index
    if index == 39:
        index = 0
    # current position
    coordinates = json_array[index]['location']
    lat = str(coordinates['lat'])
    lon = str(coordinates['lon'])
    # build record
    data['selfdrivingcarid'] = data['selfdrivingcar'] + '_' + str(generate_uuid())
    tz = pytz.timezone('Europe/Berlin')
    data['cargroup'] = data['selfdrivingcar']
    data['timestamp_car'] = str(datetime.now(tz))
    data['latitude'] = coordinates['lat']
    data['longitude'] = coordinates['lon']
    message = json.dumps(data)   
    threading.Timer(2.5, sendit2Kafka).start()
    print("#########################################")
    print(message)
    #p.produce('selfdrivingcar', key=carkey, value=message, callback=acked)
    #cts = current_milli_time()
    p.produce('selfdrivingcar', key=carkey, value=message, on_delivery=acked)# , timestamp=1614342029354)
    #p.poll(0.5)
    #p.flush(30)
    p.flush()
    print("#########################################")
    index=index+1    

def img_preprocess(img):
    img = img[60:135,:,:]
    img = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)
    img = cv2.GaussianBlur(img,  (3, 3), 0)
    img = cv2.resize(img, (200, 66))
    img = img/255
    return img
 
 
@sio.on('telemetry')
def telemetry(sid, data):    
    speed = float(data['speed'])
    image = Image.open(BytesIO(base64.b64decode(data['image'])))
    image = np.asarray(image)
    image = img_preprocess(image)
    image = np.array([image])
    steering_angle = float(model.predict(image))
    throttle = 1.0 - speed/speed_limit
    print('{} {} {}'.format(steering_angle, throttle, speed))
    send_control(steering_angle, throttle)
 


@sio.on('connect')
def connect(sid, environ):
    print('Connected')
    send_control(0, 0)
 
def send_control(steering_angle, throttle):
    sio.emit('steer', data = {
        'steering_angle': steering_angle.__str__(),
        'throttle': throttle.__str__()
    })
 
if __name__ == '__main__':
   model = load_model('model.h5')
   # Start a thread sending every 3 seconds data to Kafka
   sendit2Kafka() 
   app = socketio.Middleware(sio, app)
   eventlet.wsgi.server(eventlet.listen(('', 4567)), app)
   


   