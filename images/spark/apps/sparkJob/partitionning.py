from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType, IntegerType

def generate_image_paths(folder_path, num_images=100):
    return [f'{folder_path}/image{counter}.jpeg' for counter in range(1, num_images + 1)]

def get_partition_num(image_path):
    image_num = int(image_path.split('image')[-1].split('.')[0])
    return image_num % optimal_partitions

# Initialize Spark Session
spark = SparkSession.builder.appName("SimplePartitioning").master("local[*]").getOrCreate()
optimal_partitions = 20

# Generate image paths
folder_path = '/opt/spark-apps/images'
image_paths = generate_image_paths(folder_path)

# Create DataFrame from image paths
df = spark.createDataFrame(image_paths, StringType()).toDF("image_path")

# Register UDF
partition_udf = udf(get_partition_num, IntegerType())
df = df.withColumn("partition_num", partition_udf(df["image_path"]))

# Convert DataFrame to an RDD
images_rdd = df.rdd

# Custom partitioning function
def custom_partitioner(key):
    return int(key)

# Key the RDD by partition number and repartition using a custom partitioner
partitioned_rdd = images_rdd.keyBy(lambda row: row.partition_num).partitionBy(optimal_partitions, custom_partitioner)

# Collect and print partition contents
partitioned_data = partitioned_rdd.mapPartitionsWithIndex(lambda idx, it: [(idx, [row for row in it])]).collect()
for partition_idx, rows in partitioned_data:
    print(f"Partition {partition_idx}:")
    for _, row in rows:
        print(row)

# Stop Spark session
spark.stop()
