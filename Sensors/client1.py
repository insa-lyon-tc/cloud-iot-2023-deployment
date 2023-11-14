import paho.mqtt.client as mqtt
import base64

# Callback appelée lors de la connexion au broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connexion établie avec succès")
        client.subscribe("test")  # Abonnement au sujet "test/topic"
    else:
        print("Échec de la connexion, code de résultat : " + str(rc))

# Callback appelée lors de la réception d'un message
def on_message(client, userdata, message):
    print("Message reçu sur le sujet '" + message.topic + "': " + str(message.payload))

# Configuration du client MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Charger l'image depuis un fichier
with open("image.jpg", "rb") as image_file:
    image_data = image_file.read()


# Convertir les données de l'image en Base64
image_base64 = base64.b64encode(image_data).decode("utf-8")
client.username_pw_set("cit","cit")

# Connexion au broker RabbitMQ (ajuster l'adresse du broker si nécessaire)
client.connect("10.0.1.13", 1883, 60)  # Utilisez localhost si RabbitMQ est sur la même machine

# Boucle principale du client MQTT
client.loop_start()

# Publication d'un message sur le sujet "test/topic"
client.publish("test", image_base64)

# Attente pendant quelques secondes pour permettre la réception du message
import time
time.sleep(5)

# Déconnexion du client MQTT
client.disconnect()