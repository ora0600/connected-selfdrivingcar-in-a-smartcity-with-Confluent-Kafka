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
from pykafka import KafkaClient
 
sio = socketio.Server()
app = Flask(__name__) #'__main__'
speed_limit = 10

client = KafkaClient(hosts='localhost:9092')
topic = client.topics['selfdrivingcar']
producer = topic.get_sync_producer()
# GEO Data
input_file = open ('geo.json')
json_array = json.load(input_file)
index: int = 0
data = {}
data['selfdrivingcar'] = '000001' 

#GENERATE UUID
def generate_uuid():
    return uuid.uuid4()

def sendit2Kafka():
    global index
    if index == 39:
        index = 0
    # current position
    coordinates = json_array[index]['location']
    # build record
    data['key'] = data['selfdrivingcar'] + '_' + str(generate_uuid())
    data['timestamp'] = str(datetime.utcnow())
    data['latitude'] = coordinates['lat']
    data['longitude'] = coordinates['lon']
    message = json.dumps(data)   
    threading.Timer(2.5, sendit2Kafka).start()
    print("#########################################")
    #print("send current location to kafka:")
    #print(json_array[index]['name'])
    #print(json_array[index]['location'])
    print(message)
    # produce to kafka
    producer.produce(message.encode('ascii'))
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
    #randomval = random.choice(nearby)
    #if speed > 0:
    #    location = 'Highway / Autobahn'
    #else:
    #    location = 'Stopped! '
    #print('{} {} {}'.format(location, randomval, speed)) 
    print('{} {} {}'.format(steering_angle, throttle, speed))
    # Hier muss man die Aktionen machen, vielleicht mit einer Bilderkennung
    print('Data send in realtime to Confluent Kafka cluster')

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
   


   