from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType, IntegerType
import subprocess
import subprocess
import base64
import cv2
import numpy as np
import importlib.util
from confluent_kafka import Consumer, KafkaError, Producer
import os
import logging
import sys
import zlib
spark = SparkSession.builder.appName("ObjectDetection").master("spark://0.0.0.0:7077").getOrCreate()
optimal_partitions = 1

topicNum=1
def object_detection(binary_image):
    # Import TensorFlow libraries
    pkg = importlib.util.find_spec('tflite_runtime')
    if pkg:
        from tflite_runtime.interpreter import Interpreter
    else:
        from tensorflow.lite.python.interpreter import Interpreter

    # Define the paths to model and label map
    CWD_PATH = os.getcwd()
    PATH_TO_CKPT = os.path.join(CWD_PATH, "/opt/spark-apps/tf-model", "detect.tflite")
    PATH_TO_LABELS = os.path.join(CWD_PATH, "/opt/spark-apps/tf-model", "labelmap.txt")

    with open(PATH_TO_LABELS, 'r') as f:
        labels = [line.strip() for line in f.readlines()]

    if labels[0] == '???':
        del labels[0]

    interpreter = Interpreter(model_path=PATH_TO_CKPT)
    interpreter.allocate_tensors()

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    height = input_details[0]['shape'][1]
    width = input_details[0]['shape'][2]
    floating_model = (input_details[0]['dtype'] == np.float32)
    input_mean = 127.5
    input_std = 127.5

    outname = output_details[0]['name']

    if 'StatefulPartitionedCall' in outname:
        boxes_idx, classes_idx, scores_idx = 1, 3, 0
    else:
        boxes_idx, classes_idx, scores_idx = 0, 1, 2

    nparr = np.frombuffer(binary_image, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    imH, imW, _ = image.shape
    image_resized = cv2.resize(image_rgb, (width, height))
    input_data = np.expand_dims(image_resized, axis=0)

    if floating_model:
        input_data = (np.float32(input_data) - input_mean) / input_std

    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()

    boxes = interpreter.get_tensor(output_details[boxes_idx]['index'])[0]
    classes = interpreter.get_tensor(output_details[classes_idx]['index'])[0]
    scores = interpreter.get_tensor(output_details[scores_idx]['index'])[0]

    detections = []
    person_count = 0

    for i in range(len(scores)):
        if 0.5 < scores[i] <= 1.0:
            ymin = int(max(1, (boxes[i][0] * imH)))
            xmin = int(max(1, (boxes[i][1] * imW)))
            ymax = int(min(imH, (boxes[i][2] * imH)))
            xmax = int(min(imW, (boxes[i][3] * imW)))

            object_name = labels[int(classes[i])]
            if object_name == 'Person':
                person_count += 1
                cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (10, 255, 0), 2)

                label = f'{object_name}: {int(scores[i]*100)}%'
                labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
                label_ymin = max(ymin, labelSize[1] + 10)
                cv2.rectangle(image, (xmin, label_ymin-labelSize[1]-10), (xmin+labelSize[0], label_ymin+baseLine-10), (255, 255, 255), cv2.FILLED)
                cv2.putText(image, label, (xmin, label_ymin-7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

                detections.append([object_name, scores[i], xmin, ymin, xmax, ymax])
    result_image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    success, encoded_image = cv2.imencode('.jpg', result_image, [int(cv2.IMWRITE_JPEG_QUALITY), 50])

    if not success:
        raise Exception("Erreur lors de l'encodage de l'image résultante")

    return encoded_image
# Function to print partition contents
def print_partition_contents(index, iterator):
    partition_content = [f"Partition {index}: {row}" for _, row in iterator]
    return partition_content

def generate_image_paths(folder_path):
    # Define a list of image extensions to look for
    valid_extensions = ('.jpg', '.jpeg')
    
    # List all files in the folder and filter for images
    image_paths = [os.path.join(folder_path, file) for file in os.listdir(folder_path)
                   if file.endswith(valid_extensions)]

    return image_paths


def get_partition_num(image_path):
    image_num = int(image_path.split('img')[-1].split('.')[0])
    return image_num % optimal_partitions

def custom_partitioner(key):
    return int(key)

def read_images_in_folder_as_binary(folder_path):
    # Define a list to store binary images
    binary_images = []

    # Define a list of image extensions to look for
    valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')

    # List all files in the folder and filter for images
    image_paths = [os.path.join(folder_path, file) for file in os.listdir(folder_path)
                   if file.lower().endswith(valid_extensions)]

    for image_path in image_paths:
        try:
            with open(image_path, 'rb') as file:
                binary_image = file.read()
                binary_images.append(binary_image)
        except Exception as e:
            # Handle any exceptions that may occur while reading the image
            print(f"Error reading {image_path}: {str(e)}")

    return binary_images

kafka_producer = Producer({
        'bootstrap.servers': 'kafka.kafka.svc.cluster.local:9092',
        'client.id': 'python'
    })

def send_image(producer, topic, image_base64):
    producer.produce(topic, key=None, value=image_base64)
    producer.flush()

def detection_distribue(binary_images):
    topic = 'CIT_CAMERA_PROCESSED_'+str(topicNum)

    rdd = spark.sparkContext.parallelize(binary_images)
    results = rdd.map(object_detection)
    results_list = results.collect()

            # Create DataFrame from image paths
            #df = spark.createDataFrame(image_paths, StringType()).toDF("image_path")

            # Register UDF
            #partition_udf = udf(get_partition_num, IntegerType())
            #df = df.withColumn("partition_num", partition_udf(df["image_path"]))

            #df.show(truncate=False)
            # Convert DataFrame to an RDD
            #images_rdd = df.rdd



            #partitioned_rdd = images_rdd.keyBy(lambda row: row.partition_num).partitionBy(optimal_partitions, custom_partitioner)



            # Collect and print partition contents
            #partition_contents = partitioned_rdd.mapPartitionsWithIndex(print_partition_contents).collect()
            #for content in partition_contents:
            #    print(content)
#    save_directory = "saved_images"
#    os.makedirs(save_directory, exist_ok=True)
    for idy, (result_image) in enumerate(results_list):
        data=base64.b64encode(result_image).decode("utf-8")
        print("#######size",sys.getsizeof(data))
       # compressed3 = zlib.compress(result_image, 9)

        #print("#######size after ",sys.getsizeof(compressed3))
        # Define the file path for saving the result image

#result_file_path = os.path.join(save_directory, f"resultiiimage{idy}.jpg")   
        try:
            send_image(kafka_producer, topic, data)
            print("################ SENT ")
        except Exception as e:
            print(f"Erreur lors de l'envoi de l'image sur le topic {topic}: {e}")

kafka_consumer_conf = {
    'bootstrap.servers': 'kafka.kafka.svc.cluster.local:9092',
    'group.id': 'salah1',
    'auto.offset.reset': 'earliest'
}
logging.basicConfig(level=logging.INFO)
images_bin=[]
while True:
    try:
        consumer = Consumer(kafka_consumer_conf)
        consumer.subscribe(['CIT_CAMERA_'+str(topicNum)])

        logging.info("Début de la consommation du topic "+str(topicNum))

        while len(images_bin)<5:

            msg = consumer.poll(1.0)  # Utilisation de poll avec timeout
            if msg is None:
                # Vous pourriez vouloir sortir de la boucle ou continuer après un certain temps.
                continue
            if msg.error():
                logging.error(f"Erreur de consommation: {msg.error()}")
                continue

            try:
                logging.info("Message consommé")
                image_base64 = msg.value().decode("utf-8")
                image_binary = base64.b64decode(image_base64)
                print("size input",sys.getsizeof(image_binary))
                images_bin.append(image_binary)

                logging.info(f"Image ajouté")

            except Exception as e:
                logging.error(f"Erreur lors du traitement du message : {e}")

        logging.info(f"############## TRAITEMENET topic " +str(topicNum)+ "###################")
        detection_distribue(images_bin)
        logging.info(f"############## FIN TRAITEMENT topic"+str(topicNum)+" ###################")
        if(topicNum>=4):
            topicNum =1
        else:
            topicNum+=1
        images_bin=[]
    except KeyboardInterrupt:
        logging.info("Arrêt de la consommation sur demande de l'utilisateur")
        break
    finally:
        consumer.close()
        logging.info("Consumer fermé")

spark.stop()