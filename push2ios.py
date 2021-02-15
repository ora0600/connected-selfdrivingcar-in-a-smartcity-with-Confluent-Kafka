from confluent_kafka import Consumer, KafkaError
import json
import http.client, urllib

c = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'push2IOS',
    'auto.offset.reset': 'largest'
})

c.subscribe(['selfdrivingcar'])

max_message=12
message_count=1

while True:
    msg = c.poll(1.0)

    if msg is None:
        continue
    if msg.error():
        print("Consumer error: {}".format(msg.error()))
        continue

    app_json_msg = json.loads(msg.value().decode('utf-8'))
    title=', Self-Driving-Car 000001' 
    message1 = 'Das Dorinthotel würde sich über ein Besuch freuen. 20% Discount für Sie!'
    #{"selfdrivingcar": "000001", "key": "000001_52ec1cb6-bdf7-49fc-935e-5d29726f3d5c", "timestamp": "2021-01-20 10:31:08.763603", "latitude": 6.9496495, "longitude": 50.3368724}
    message2 = 'Das ring werk heute im Angebot, 1 x Reifenwechseln inkl. Dunlop Reifen für 199€. Schauen Sie rein.'
    #{"selfdrivingcar": "000001", "key": "000001_ebd76d0a-af04-4bdf-bab8-04c91e528b60", "timestamp": "2021-01-20 10:36:09.223152", "latitude": 6.9475517, "longitude": 50.3354611}
    message3 = 'Heute im Eiffelstadl Bio-Schnitzel mit Pommes und Salat für 19,98€. Wir würden uns freuen (-:'
    #{"selfdrivingcar": "000001", "key": "000001_15a8f6f3-eb95-4522-aaec-5bed0561c366", "timestamp": "2021-01-20 10:33:03.944246", "latitude": 6.9437624, "longitude": 50.3330502}
    message4 = 'Business Meeting inkl. Unterkunft und Meeting Package. Buchen Sie Ihr nächstes Meeting bei uns, siehe www.lindner.de'
    #{"selfdrivingcar": "000001", "key": "000001_085622e4-65c0-415f-b4f1-079d00611961", "timestamp": "2021-01-20 10:36:21.741645", "latitude": 6.9426784, "longitude": 50.3324277}
    message5 = 'Vegane Woche bei uns. Alles Bio, frisch und sehr geschmackvoll. Schauen Sie rein, wir freuen uns auf Sie.'
    #{"selfdrivingcar": "000001", "key": "000001_448c021f-6af4-4fd0-b3cf-acb1df70e1a8", "timestamp": "2021-01-20 10:31:56.344242", "latitude": 6.9373174, "longitude": 50.3259029}
    message6 = 'Achtung in der nächsten Kurve ein Unfall, bite fahren sie langsam...'
    #{"selfdrivingcar": "000001", "key": "000001_1a733688-a827-47f1-b475-275f5c16ea16", "timestamp": "2021-01-20 10:34:04.033901", "latitude": 6.9380496, "longitude": 50.3341507}
    latitude=app_json_msg['latitude']
    longitude=app_json_msg['longitude']
    #print(latitude)
    #print(longitude)
    if latitude == 6.9496495 and  longitude == 50.3368724:
        message = message1
    elif latitude == 6.9475517 and longitude == 50.3354611:
        message = message2
    elif latitude == 6.9437624 and  longitude == 50.3330502:
        message = message3
    elif latitude == 6.9426784 and longitude == 50.3324277:
        message = message4
    elif latitude == 6.9373174 and longitude == 50.3259029:
        message = message5
    elif latitude == 6.9380496 and longitude == 50.3341507:
        message = message6
    else: 
        message = ''
    
    # send message to IOS 
    if message_count <= max_message and message != "":
        print (message)
        conn = http.client.HTTPSConnection("api.pushover.net:443")
        conn.request("POST", "/1/messages.json",
        urllib.parse.urlencode({
            "token": "PASTE YOUR TOKEN",
            "user": "PASTE YOUR USER",
            "message": message,
        }), { "Content-type": "application/x-www-form-urlencoded" })
        response=conn.getresponse()
        print('Status: %s Reason:%s' % (response.status, response.reason))
        conn.close()
        message_count=message_count + 1
c.close()