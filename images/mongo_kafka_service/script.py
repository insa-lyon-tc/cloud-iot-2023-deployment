import os
import base64
from confluent_kafka import Consumer, KafkaError
from pymongo import MongoClient
import logging

# configure logging
logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', level=logging.INFO, datefmt="%d-%m-%y %H:%M:%S")

# Connexion à MongoDB
mongo_ip = os.getenv('MONGO_CLUSTER_IP')
mongo_port = os.getenv('MONGO_CLUSTER_PORT')
mongo_client = MongoClient(f'mongodb://{mongo_ip}:{mongo_port}')
mongodb = mongo_client['cit']

# Configuration du KafkaConsumer
kafka_ip = os.getenv('KAFKA_CLUSTER_IP')
kafka_port = os.getenv('KAFKA_CLUSTER_PORT')
conf = {
    'bootstrap.servers': f'{kafka_ip}:{kafka_port}',
    'group.id': 'python1',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
consumer.subscribe(['CIT_CAMERA_1', 'CIT_CAMERA_2', 'CIT_CAMERA_3', 'CIT_CAMERA_4', 'CIT_CAMERA_5', 'CIT_CAMERA_PROCESSED_1', 'CIT_CAMERA_PROCESSED_2', 'CIT_CAMERA_PROCESSED_3', 'CIT_CAMERA_PROCESSED_4', 'CIT_CAMERA_PROCESSED_5'])

# Consommation des messages depuis Kafka
try:
    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                # Pas d'erreur, atteint la fin de la partition
                continue
            else:
                print(msg.error())
                break

        try:
            # Décoder la chaîne Base64 du message
            base64_data = msg.value()
            decoded_data = base64.b64decode(base64_data)

            # Extraire le nom du topic du message
            topic_name = msg.topic()

            # Stocker les données Base64 dans la collection MongoDB correspondante
            collection = mongodb[topic_name]
            collection.insert_one({'data': decoded_data})

            logging.info(f"Message inserted into MongoDB for topic {topic_name}")
        except Exception as e:
            print(f"Could not process message: {e}")

except KeyboardInterrupt:
    pass
finally:
    # Fermeture propre du consumer
    consumer.close()