from pyspark import SparkContext, SparkConf
import subprocess
import os

# Set up the Spark context
conf = SparkConf().setMaster("spark://10.0.1.176:7077").setAppName("ObjectDetection")
sc = SparkContext(conf=conf)

# Assuming you have a list of image paths to process
#image_paths = ['/opt/tflite1/images/image1.jpg','/opt/tflite1/images/image2.jpg', '/opt/tflite1/images/image3.jpg','/opt/tflite1/images/image4.jpg']

def generate_image_paths(folder_path, num_images=255):
    image_paths = []

    for counter in range(1, num_images+1):
        image_path = f'{folder_path}/image{counter}.jpg'
        image_paths.append(image_path)

    return image_paths

# images from 1 to 64 already in workers.
folder_path = '/opt/tflite1/images'
image_paths = generate_image_paths(folder_path)

images_rdd = sc.parallelize(image_paths)
images_rdd = images_rdd.repartition(10)

# Define a function that calls the object detection script
def run_object_detection(image_path):
    # Define the command to run the object detection Python script
    script_path = '/opt/tflite1/TFLite_detection_image.py'
    model_dir = '/opt/tflite1/Sample_TFLite_model'
    python_interpreter = "/opt/tflite1/tflite1-env/bin/python3"

    # Here we are calling the Python script with subprocess
    command = [python_interpreter, script_path, '--modeldir', model_dir, '--image', image_path,'--save_results', 
        '--noshow_results']
    
    try:
        # Run the command and capture output
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return f"Processed {image_path}. Output: {result.stdout}"
    except subprocess.CalledProcessError as e:
        # Handle exceptions for errors in subprocess and include stderr in the output
        error_message = f"An error occurred: {e}. Output: {e.stdout}, Error: {e.stderr}"
        print(error_message)
        return error_message
    
    # Optionally return something, like an indication that the process was successful
    return f"Processed {image_path}"

# Use the map operation to run object detection on all images
results = images_rdd.map(run_object_detection).collect()

# Do something with the results if needed
for result in results:
    print(result)

# Stop the Spark context
sc.stop()

