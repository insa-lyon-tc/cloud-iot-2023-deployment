import socket
from picamera import PiCamera
from time import sleep
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
import base64
import os
from PIL import Image

load_dotenv("/var/mqtt/.env")

CAMERA_TOPICS = {
    "10.0.1.1": "CAMERA_1",
    "10.0.1.2": "CAMERA_2",
    "10.0.1.11": "CAMERA_3",
    "10.0.1.13": "CAMERA_4",
    "10.0.1.15": "CAMERA_5",
}

LIST_IR_CAMERA = ["10.0.1.1", "10.0.1.11"]
LIST_CAMERA = ["10.0.1.2", "10.0.1.13", "10.0.1.15"]

IP_ADDRESS = socket.gethostbyname(socket.gethostname())

RESOLUTION = (map(int, os.getenv("RESOLUTION").split(",")))
SLEEP_TIME = int(os.getenv("SLEEP_TIME"))
IMG_NAME = os.getenv("IMG_NAME")
QUALITY = int(os.getenv("QUALITY"))
ROTATION = int(os.getenv("ROTATION"))
FLIP = -1 if IP_ADDRESS in LIST_IR_CAMERA else 1

IP = os.getenv("IP")
PORT = int(os.getenv("PORT"))
TOPIC = f"{os.getenv('TOPIC_PREFIX')}_{CAMERA_TOPICS[IP_ADDRESS]}"
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
TIMEOUT = int(os.getenv("TIMEOUT"))


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connection established")
    else:
        print("Connection failed : " + str(rc))


def on_publish(client, obj, mid):
    print(f"Image published on {TOPIC}")


def setup_camera():
    camera = PiCamera()
    camera.rotation = 180
    camera.resolution = RESOLUTION
    camera.start_preview()
    return camera


def setup_mqttclient():
    mqttclient = mqtt.Client()
    mqttclient.username_pw_set(USERNAME, PASSWORD)
    mqttclient.on_connect = on_connect
    mqttclient.on_publish = on_publish
    return mqttclient


def take_picture(camera):
    sleep(SLEEP_TIME)
    camera.capture(IMG_NAME)
    camera.stop_preview()


def encode_image(img_name):
    with open(img_name, "rb") as img_file:
        data = img_file.read()
    return base64.b64encode(data).decode("utf-8")


def send_image(mqttclient, data):
    return mqttclient.publish(TOPIC, data, qos=1)


def process_image():
    image = Image.open(IMG_NAME)
    image = image.rotate(ROTATION * FLIP)
    image.save(IMG_NAME, optimize=True, quality=QUALITY)


def main():
    camera = setup_camera()
    mqttclient = setup_mqttclient()
    mqttclient.connect(IP, PORT, TIMEOUT)
    mqttclient.loop_start()
    take_picture(camera)
    process_image()
    data = encode_image(IMG_NAME)
    message = send_image(mqttclient, data)
    message.wait_for_publish()
    mqttclient.disconnect()


if __name__ == "__main__":
    main()
