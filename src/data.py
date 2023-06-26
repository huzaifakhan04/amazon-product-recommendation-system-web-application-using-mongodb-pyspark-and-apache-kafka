#   Importing the necessary libraries/modules.

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, LongType, DoubleType, BooleanType, IntegerType, MapType

#   Creating an instance of a SparkSession object and connecting it to MongoDB.

spark=SparkSession \
    .builder \
    .appName("AmazonReviewData") \
    .master("local") \
    .config("spark.mongodb.input.uri", "mongodb://localhost:27017/") \
    .config("spark.mongodb.output.uri", "mongodb://localhost:27017/") \
    .config("spark.executor.memory", "8g") \
    .config("spark.driver.memory", "8g") \
    .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:3.0.1") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR") #   Overriding the default log level.

#   Defining the schema of the dataset to be loaded into the Spark DataFrame.

schema=StructType([
    StructField("asin", StringType(), nullable=False),  #   Unique indentification number for the product.
    StructField("overall", DoubleType(), nullable=False),   #   Rating given by the reviewer between one and five.
    StructField("reviewText", StringType(), nullable=False),    #   Review given by the reviewer.
    StructField("reviewerID", StringType(), nullable=False),    #   Unique identification number for the reviewer.
    StructField("reviewerName", StringType(), nullable=False),  #   Name of the reviewer.
    StructField("summary", StringType(), nullable=False),   #   Summary of the review.
    StructField("unixReviewTime", LongType(), nullable=False),  #   Time when the review was given in unix time.
    StructField("verified", BooleanType(), nullable=False), #   Whether the review was verified or not.
    StructField("vote", IntegerType(), nullable=True),  #   Number of votes the review received.
    StructField("image", StringType(), nullable=True),   #   Image associated with the review.
    StructField("style", MapType(StringType(), StringType(), valueContainsNull=True), nullable=True),   #   Style of the product.
])

#   Reading the dataset from the JavaScript Object Notation (JSON) file into the Spark DataFrame.

dataframe=spark.read.format("json").option("mode", "DROPMALFORMED").schema(schema).load("./data/All_Amazon_Review.json.gz")

print("JavaScript Object Notation (JSON) file stored in the Spark DataFrame successfully!")

#   Writing the Spark DataFrame into the MongoDB database as a collection.

database="amazon_review_data"
collection="product_reviews"
dataframe.select("asin", "reviewerID", "reviewerName", "reviewText", "summary", "overall", "unixReviewTime", "verified", "vote", "image", "style").write \
    .format("com.mongodb.spark.sql.DefaultSource") \
    .option("uri", "mongodb://localhost:27017/"+database+"."+collection) \
    .option("replaceDocument", "false") \
    .option("partitioner", "MongoSinglePartitioner") \
    .option("partitionKey", "asin") \
    .save()

print("Spark DataFrame stored in the `"+database+"` database as the `"+collection+"` collection successfully!")
spark.stop()    #   Stopping the SparkSession object.