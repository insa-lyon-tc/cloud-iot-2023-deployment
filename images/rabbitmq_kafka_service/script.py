import paho.mqtt.client as mqtt
from confluent_kafka import Producer
import os
import logging

KAFKA_SERVER = os.getenv("KAFKA_SERVER")
MQTT_SERVER = os.getenv("MQTT_SERVER")

# configure logging
logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', level=logging.INFO, datefmt="%d-%m-%y %H:%M:%S")

# mqtt
def on_connect(client, userdata, flags, rc):
    logging.info(f"Connected to RabbitMQ with return code: {rc}")
    # s'abonner au topic que team Messaging va nous communiquer
    client.subscribe("#")


def on_message(client, userdata, msg):
    global last_received_message
    logging.info(f"MQTT message received on topic {msg.topic}")
    image_base64 = msg.payload.decode("utf-8")
    #last_received_message = image_base64
    producer.produce(str(msg.topic), value=image_base64, callback=delivery_report)
    producer.flush()


def delivery_report(err, msg):
    if err is not None:
        logging.error(f"Could not send message to Kafka: {err}")
    else:
        logging.info("Message sent to Kafka successfully")

conf = {
    'bootstrap.servers': KAFKA_SERVER,  # adresses et ports des brokers Kafka
    'client.id': 'python-producer'
}

producer = Producer(conf) # producer kafka

client = mqtt.Client()
client.username_pw_set("admin","admin")
client.on_connect = on_connect
client.on_message = on_message

# connexion au broker MQTT
broker_address = MQTT_SERVER
port = 1883
client.connect(broker_address, port, 60)

client.loop_forever()

producer.flush()