# Sensor Team

## Equipe
- Vivek
- Zoé
- Alice

## Description du projet

### Rasberry List
Raspberry 3B | 10.0.1.1  | b8:27:eb:db:02:da |a405 661 | Camera IR ✅ 
Raspberry 3B | 10.0.1.2  | b8:27:eb:db:ce:33 |a405 662 | Camera  ✅
Raspberry 3B | 10.0.1.11 | b8:27:eb:2f:a4:b4 |a405 693 | Camera IR ✅ 
Raspberry 3B | 10.0.1.13 | b8:27:eb:8d:bd:c9 |a405 671 | Camera ❌ 
Raspberry 3B | 10.0.1.15 | b8:27:eb:8b:c7:15 |a405 694 | Camera ✅ 


### How to retrieve an image manually
- Book a device with a camera
- ssh <address>
- sudo usermod -a -G video <username>
- sudo raspi-config
- select : 3 Interface Options
- Enable camera
- Wait for reboot and reconnect
- raspistill -o Desktop/image.jpg or raspistill -o image.jpg
- in another terminal : scp <username>@<address>:/home/<username>/<pathToImage>image.jpg

### Techno used
- MQTT (pip install paho-mqtt and pip install pika)

### Client
- Install paho-mqtt : 
sudo apt update
sudo apt-get install python3-pip
pip3 install paho-mqtt

### Broker
- Install mpaho-mqtt : 
sudo apt update
sudo apt-get install python3-pip
pip3 install paho-mqtt
- Install Rabbit MQ : 
sudo apt-get update
sudo apt-get install rabbitmq-server
- Start Rabbit MQ : 
sudo service rabbitmq-server start
- Activation plugin mqtt : 
sudo rabbitmq-plugins enable rabbitmq_mqtt
sudo service rabbitmq-server restart
