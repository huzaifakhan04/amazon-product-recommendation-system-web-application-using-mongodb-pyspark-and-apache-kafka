#   Importing the required libraries/modules.

from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType
from pyspark.ml.recommendation import ALSModel
from pymongo import MongoClient

#   Creating an instance of a SparkSession object and connecting it to MongoDB.

spark=SparkSession \
    .builder \
    .appName("ProductRecommendationModel") \
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
database=client["amazon_review_data"]   #   Connecting to the `amazon_review_data` database.
collection=database["features"] #   Connecting to the `features` collection.
reviewer_id="A2P5KJLAVF7KG4"
reviewer_id_index=collection.find_one({"reviewerID": reviewer_id})["reviewerID_index"]  #   Retrieving the corresponding indexed value for the particular reviewerID.

#   Creating a Spark DataFrame containing the corresponding indexed value for the particular reviewerID.

user_dataframe=spark.createDataFrame([int(reviewer_id_index)], IntegerType()).toDF("reviewerID_index")

#   Generating the top three product recommendations for the particular reviewerID.

recommendations=model.recommendForUserSubset(user_dataframe, 3)
recommendations=recommendations.toPandas()  #   Converting the Spark DataFrame into a pandas.DataFrame.
print("Product recommendations for "+reviewer_id+" generated successfully!")

#   Retrieving the indexed ASIN values and predicted scores for the top three product recommendations.

recommendations=recommendations["recommendations"][0]
asin_index=[i[0] for i in recommendations]
scores=[i[1] for i in recommendations]

#   Retrieving the corresponding ASINs for the top three product recommendations.

asin=collection.find({"asin_index": {"$in": asin_index}}, {"_id": 0, "asin": 1, "title": 1})
asin=list(asin)
asin=[i["asin"] for i in asin]  #   Extracting the ASINs from the list of dictionaries.
print("Top Three Product Recommendations For "+reviewer_id+":")
print(asin)

spark.stop()    #   Stopping the SparkSession object.