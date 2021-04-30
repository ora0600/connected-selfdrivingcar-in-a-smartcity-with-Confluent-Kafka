from flask import Flask, render_template, Response
from confluent_kafka import Consumer
import json
import sys

def get_kafka_client(topic):
    consumer = Consumer({
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'geo_consumer',  
        'session.timeout.ms': 6000,
        'auto.offset.reset': 'latest'
    })
    # Subscribe to topic
    consumer.subscribe([topic])
    return consumer

app = Flask(__name__)


@app.route('/')
def index():
    print("render index.html")
    return(render_template('index.html'))

#Consumer API
@app.route('/topic/<topicname>')
def get_messages(topicname):
    client = get_kafka_client(topicname)
    def events():
        try:
            while True:
                msg = client.poll(timeout=1.0)
                if msg is None:
                    continue
                if msg.error():
                    raise KafkaException(msg.error())
                else:
                    # Proper message
                    record_value = msg.value()
                    yield 'data:{0}\n\n'.format(record_value.decode())
        except KeyboardInterrupt:
            sys.stderr.write('%% Aborted by user\n')
        finally:
            # Close down consumer to commit final offsets.
            client.close()
    return Response(events(), mimetype="text/event-stream")

if __name__ == '__main__':
    app.run(debug=True, port=5001)





