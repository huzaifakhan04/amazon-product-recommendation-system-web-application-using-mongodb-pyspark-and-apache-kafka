#   Importing the required libraries/modules.

from pyspark.sql import SparkSession

#   Creating an instance of a SparkSession object and connecting it to MongoDB.

spark=SparkSession \
    .builder \
    .appName("CompressedStratifiedSample") \
    .master("local") \
    .config("spark.mongodb.input.uri", "mongodb://localhost:27017/") \
    .config("spark.mongodb.output.uri", "mongodb://localhost:27017/") \
    .config("spark.executor.memory", "8g") \
    .config("spark.driver.memory", "8g") \
    .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:3.0.1") \
    .config("spark.rdd.compress", "true") \
    .config("spark.sql.parquet.compression.codec", "gzip") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR") #   Overriding the default log level.

#   Reading the dataset from the MongoDB database as a collection into the Spark DataFrame and extracting a stratified sample
#   of a specified sample size based on the product identification number (ASIN).

database="amazon_review_data"
collection="product_reviews"
size=10_000_000
sample=spark.read.format("com.mongodb.spark.sql.DefaultSource") \
    .option("uri", "mongodb://localhost:27017/"+database+"."+collection) \
    .option("partitioner", "MongoSinglePartitioner") \
    .option("partitionKey", "asin") \
    .option("pipeline", '''[
                                {
                                    '$match':
                                    {
                                        'asin':
                                        {
                                            '$exists': true
                                        }
                                    }
                                },
                                {
                                    '$sample':
                                    {
                                        'size': '''+str(size)+'''
                                    }
                                }
                            ]''') \
    .option("spark.mongodb.input.renameField", "style::_style") \
    .option("spark.mongodb.input.renameField", "style name::style_name") \
    .load() \
    .select("asin", "reviewerID", "overall")

print("Stratified sample of "+str(size)+" reviews extracted from the `"+collection+"` collection of the `"+database+"` database successfully!")

#   Saving the dataset as an Apache Parquet file.

sample.write.option("compression", "gzip").mode("overwrite").parquet("./data/sample.parquet")

print("Stratified sample of "+str(size)+" reviews saved as an Apache Parquet file successfully!")
spark.stop()    #   Stopping the SparkSession object.