#   Importing the required libraries/modules.

from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from kafka import KafkaProducer
from kafka import KafkaConsumer
import json
import os

application=Flask(__name__, template_folder="templates", static_folder="static")    #   Creating a Flask object.
application.config["UPLOAD_FOLDER"]=r"static/files" #   Configuring the upload folder.

#   Creating an instance of a KafkaProducer object and connecting it to the Apache Kafka Broker.

producer=KafkaProducer(bootstrap_servers="localhost:9092",
                        value_serializer=lambda x: json.dumps(x).encode("utf-8"))

#   Creating an instance of a KafkaConsumer object and connecting it to the `recommendations` topic.

consumer=KafkaConsumer("recommendations",
                        bootstrap_servers="localhost:9093",
                        value_deserializer=lambda x: json.loads(x.decode("utf-8")),
                        auto_offset_reset="earliest")

#   Function to render the favicon.

@application.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(application.root_path, "static"), "favicon.png", mimetype="image/vnd.microsoft.icon")

#   Function to render the login page.

@application.route("/")
def index():
    return render_template("login.html")

#   Function to manage the login process.

@application.route("/login", methods=["POST"])
def login():
    global username
    username=request.form["username"]   #   Retrieving the username from the login form.
    print("-")
    print("reviewerID: "+username)
    print("-")
    return redirect(url_for("dashboard"))   #   Redirecting to the dashboard page.

#   Function to render the dashboard page.

@application.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

#   Function to render the review page.

@application.route("/review", methods=["GET"])
def review():
    return render_template("review.html")

#   Function to render the loading page.

@application.route("/loading")
def loading():
    return render_template("loading.html")

#   Function to manage the review submission process.

@application.route("/submit_review", methods=["POST"])
def submit_review():
    producer.send("credentials", value=username)    #   Sending the reviewerID for the particular user to the `credentials` topic.
    return redirect(url_for("loading")) #   Redirecting to the loading page.

#   Function to render the recommendation page.

@application.route("/recommendation")
def recommendation():
    global scores
    global asin_list

    #   Iterating through the KafkaConsumer object to retrieve the ASINs and predicted scores of
    #   the recommended products from the `credentials` topic.

    for message in consumer:
        scores=list(message.value["scores"])
        asin_list=list(message.value["asin_list"])
        if asin_list and scores:
            break

    recommendation_one=asin_list[-1]
    recommendation_two=asin_list[-2]
    recommendation_three=asin_list[-3]

    #   Converting the predicted scores into percentage values.

    match_one=round(scores[-1]*10, 1)
    match_two=round(scores[-2]*10, 1)
    match_three=round(scores[-3]*10, 1)

    #   Converting the predicted scores into absolute values.

    match_one=abs(match_one)
    match_two=abs(match_two)
    match_three=abs(match_three)

    #   Ensuring that the predicted scores do not exceed 100%.

    if match_one>100:
        match_one=100
    if match_two>100:
        match_two=100
    if match_three>100:
        match_three=100

    return render_template("recommendation.html",
                            recommendation_one=recommendation_one, recommendation_two=recommendation_two, recommendation_three=recommendation_three,
                            match_one=str(match_one), match_two=str(match_two), match_three=str(match_three))

#   Driver function.

if __name__=="__main__":
    application.run(debug=True, port=3000)