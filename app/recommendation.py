#   Importing the required libraries/modules.

from kafka import KafkaProducer
from kafka import KafkaConsumer
from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType
from pyspark.ml.recommendation import ALSModel
from pymongo import MongoClient
import json
import time

#   Creating an instance of a SparkSession object and connecting it to MongoDB.

spark=SparkSession \
    .builder \
    .appName("ProductRecommendationSystem") \
    .master("local") \
    .config("spark.mongodb.input.uri", "mongodb://localhost:27017/") \
    .config("spark.mongodb.output.uri", "mongodb://localhost:27017/") \
    .config("spark.executor.memory", "8g") \
    .config("spark.driver.memory", "8g") \
    .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:3.0.1") \
    .config("spark.sql.autoBroadcastJoinThreshold", "-1") \
    .config("spark.storage.memoryFraction", "1") \
    .config("spark.rdd.compress", "true") \
    .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
    .config("spark.kryoserializer.buffer.max", "1g") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR") #   Overriding the default log level.
model=ALSModel.load("./model/product_recommendation_model") #   Loading the trained product recommendation model.
print("Product recommendation model loaded successfully!")

client=MongoClient("mongodb://localhost:27017/")    #   Creating an instance of the MongoClient object and connecting it to MongoDB.
database=client["amazon_review_data"]   #   Connecting to the database.
collection=database["features"] #   Connecting to the collection.

#   Creating an instance of a KafkaConsumer object and connecting it to the `credentials` topic.

consumer=KafkaConsumer("credentials",
                        bootstrap_servers="localhost:9092",
                        value_deserializer=lambda x: json.loads(x.decode("utf-8")))

#   Creating an instance of a KafkaProducer object and connecting it to the Apache Kafka Broker.

producer=KafkaProducer(bootstrap_servers="localhost:9093",
                        value_serializer=lambda x: json.dumps(x).encode("utf-8"))

#   Function to generate the product recommendations for the particular user.

def get_recommendations(username):
    reviewer_id_index=collection.find_one({"reviewerID": username})["reviewerID_index"] #   Retrieving the corresponding indexed value for the particular reviewerID.

    #   Creating a Spark DataFrame containing the corresponding indexed value for the particular reviewerID.

    user_dataframe=spark.createDataFrame([int(reviewer_id_index)], IntegerType()).toDF("reviewerID_index")
    recommendations=model.recommendForUserSubset(user_dataframe, 3)
    recommendations=recommendations.toPandas()  #   Converting the Spark DataFrame into a pandas.DataFrame.
    print("Product recommendations for "+username+" generated successfully!")
    spark.stop()    #   Stopping the SparkSession object.

    #   Retrieving the indexed ASIN values and predicted scores for the top three product recommendations.

    recommendations=recommendations["recommendations"][0]
    asin_index=[i[0] for i in recommendations]
    scores=[i[1] for i in recommendations]

    #   Retrieving the corresponding ASINs for the top three product recommendations from the database.

    asin=collection.find({"asin_index": {"$in": asin_index}}, {"_id": 0, "asin": 1, "title": 1})

    asin=list(asin)
    asin_list=[i["asin"] for i in asin] #   Extracting the ASINs from the list of dictionaries.
    return scores, asin_list

#   Iterating through the KafkaConsumer object to retrieve the username from the `credentials` topic.

for message in consumer:
    username=message.value
    scores, asin_list=get_recommendations(username) #   Retrieving the product recommendations for the particular reviewerID.
    print("Sending the product recommendations for "+username+" to the Apache Kafka Consumer...")
    producer.send("recommendations", value={"scores": scores, "asin_list": asin_list})  #   Sending the product recommendations to the `recommendations` topic.
    print("Product recommendations for "+username+" sent successfully!")
    time.sleep(300) #   Waiting for 5 minutes before sending the next set of product recommendations.
    break