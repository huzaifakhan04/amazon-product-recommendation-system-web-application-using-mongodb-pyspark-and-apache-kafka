# Amazon.com Product Recommendation System Web Application Using MongoDB, PySpark, & Apache Kafka:

This repository builds upon the work of [**Exploratory Data Analysis (EDA) on Amazon Review Data (2018) Using MongoDB & PySpark**](https://github.com/huzaifakhan04/exploratory-data-analysis-on-amazon-review-data-using-mongodb-and-pyspark) and includes a web application that is connected to a product recommendation system developed with the comprehensive Amazon Review Data (2018) dataset, consisting of nearly 233.1 million records and occupying approximately 128 gigabytes (GB) of data storage, using MongoDB, PySpark, and Apache Kafka, as part of the final project for the Fundamental of Big Data Analytics (DS2004) course.

### Dependencies:

* Jupyter Notebook ([install](https://docs.jupyter.org/en/latest/install.html))
* PySpark ([install](https://spark.apache.org/docs/latest/api/python/getting_started/install.html))
* MongoDB Community Edition ([install](https://www.mongodb.com/docs/manual/administration/install-community/))
* Apache Kafka ([install](https://kafka.apache.org/downloads))
* PyMongo ([install](https://pymongo.readthedocs.io/en/stable/installation.html))
* kafka-python ([install](https://kafka-python.readthedocs.io/en/master/install.html))
* Matplotlib ([install](https://matplotlib.org/stable/users/installing/index.html))
* seaborn ([install](https://seaborn.pydata.org/installing.html))
* Flask ([install](https://flask.palletsprojects.com/en/2.3.x/installation/))

## Introduction:

Product recommendation systems are types of software that use data analysis and machine learning techniques to suggest products to customers based on their interests, past purchases, and browsing history. These systems can be found on e-commerce websites, such as Amazon.com, and are designed to provide personalised recommendations to users in real-time. Recommendation systems work by analysing vast amounts of data, such as user behaviour, product attributes, and transaction history. Based on this data, the system generates recommendations that are relevant to the user's interests and preferences. For example, if a user has previously purchased a book on a specific topic, the recommendation system may suggest other books on the same topic, or related topics.

The Amazon Review Data (2018) dataset can be utilised to train a product recommendation system that offers personalised product suggestions to users based on their purchase history, as well as the satisfaction levels of other users who have reviewed and rated products on the platform. However, since the dataset is vast, it is crucial to carefully analyse and select the relevant features that will effectively contribute to the product recommendation system, in order to avoid both overfitting and underfitting of the machine learning model.

## What Is Our Approach?

Similar to our approach in conducting Exploratory Data Analysis (EDA) on the Amazon Review Data (2018) dataset **Amazon Review Data (2018) Analysis.ipynb, 1-38)**, we employed an inferential statistical method for training our product recommendation model. The rationale for using a sample to make inferences about the entire population is to minimise the computational burden associated with processing the complete dataset, which is often impractical for a single machine. While deep learning typically requires large amounts of data, machine learning can be effectively used to develop robust training methodologies even with small datasets. This is particularly useful for hypothesis-driven research, which is our primary objective with the product recommendation system. **(Vabalas et al., 2019)** In any case, it is important to note that any dataset is essentially a subset of a larger population.

To ensure the accuracy of our results, it is crucial to carefully analyse and mitigate potential biases in the data. This is particularly important in machine learning, which is sensitive to biases that can result in skewed performance estimates. To address this issue, we will apply the stratified random sampling approach we discussed earlier to extract a representative sample of 10,000,000 records from the population while maintaining the same product distribution as in the original dataset. **(compress.py, 1-61)** Since the sample size is quite large, we have compressed it into an Apache Parquet file format, which reduces the dataset's size by over 90%.

### What Is the Alternating Least Squares (ALS) Algorithm?

Alternating Least Squares (ALS) is a collaborative filtering algorithm used for developing product recommendation systems. The algorithm aims to learn the latent or hidden factors that influence user-item interactions, by decomposing the user-item rating matrix into two low-rank matrices representing the user and item latent factors.

Alternating Least Squares (ALS) works iteratively, alternating between fixing one set of latent factors and solving for the other using a least-squares optimisation algorithm. In particular, in each iteration, the algorithm fixes the item latent factors and solves for the user latent factors using least-squares optimisation, and then fixes the user latent factors and solves for the item latent factors using least-squares optimisation.

### Why the Alternating Least Squares (ALS) Algorithm?

Alternating Least Squares (ALS) has several advantages for product recommendation systems. It is scalable and computationally efficient, particularly for large and sparse datasets. It can handle implicit feedback data, where user-item interactions are only known to exist or not exist, and not their specific ratings. It can also handle missing data, where not all users have rated all items. Additionally, Alternating Least Squares (ALS) can provide item recommendations in real-time, making it suitable for online recommendation systems.

## Usage:

* ``Product Recommendation Model.ipynb`` — Contains the implementation (MLlib) of the trained and tested product recommendation system on the Amazon Review Data (2018) dataset.
* ``src\data.py`` — Source code for storing the dataset from the JavaScript Object Notation (JSON) file into a MongoDB database as a collection.
* ``src\compress.py`` — Source code for extracting a stratified random sample of a specified sample size from the dataset stored in the MongoDB database as a collection and storing it as an Apache Parquet file.
* ``src\validate.py`` — Source code to validate the accuracy and functionality of the trained product recommendation system using a practical example.
* ``model\product_recommendation_model`` — Directory containing the trained machine learning model for the product recommendation system.
* ``app\application.py`` — Source for the web application (Flask) associated with the product recommendation system through an Apache Kafka cluster.
* ``app\recommendation.py`` — Source code for the Apache Kafka cluster connected to the trained machine learning model for the product recommendation system enabling the generation of product recommendations.
* ``templates`` — Contains the source codes for the web pages (``login.html``, ``dashboard.html``, ``review.html``, ``loading.html``, and ``recommendation.html``) rendered by the web application (Flask).
* ``static`` — Contains all the icons and visual elements utilised by the web application (Flask).
* ``.hintrc`` — Configuration file to customise ESLint's behaviour by specifying specific settings and rules.

## Instructions (Execution):

* Download the ``All_Amazon_Review.json.gz`` file from the Amazon Review Data (2018) [collection](https://nijianmo.github.io/amazon/index.html) website.
* Run ``src\data.py`` to save the dataset from the JavaScript Object Notation (JSON) file into a MongoDB database as a collection (make sure that MongoDB is already set up and running).
* Once the data is stored, run ``src\compress.py`` to extract a stratified random sample of a specified size from the dataset stored in MongoDB and save the sample as an Apache Parquet file.
* Execute the ``Product Recommendation Model.ipynb`` file (1-16) to transform the collection and store it back in MongoDB for permanent access (you don't have to execute the entire file).
* Open a Terminal instance and run ``app\recommendation.py`` on the side (make sure that an Apache Kafka cluster has been successfully established and is operational, with two topics named **credentials** and **recommendations**).
* Open a separate Terminal instance to run ``app\application.py`` and open the provided link to the host port.
* Enter a valid username that corresponds to any **reviewerID** value from the transformed collection in the MongoDB database (the password doesn't matter).
* On the ``/dashboard`` page, click on the **Review** button and submit any content.
* After submitting, there will be a five-minute wait on the ``/loading`` page while the product recommendations are generated.
* Once the wait is over, you will be redirected to the ``/recommendation`` page to view the generated product recommendations.

#### Note:

The source code files were specifically written for **macOS Ventura** and may need modifications to ensure proper execution on other operating systems.

## Contributors:

This project exists thanks to the extraordinary people who contributed to it.
* **[Wajeeh Ul Hassan](https://github.com/wajeehulhassanr) (i212684@nu.edu.pk)**
* **[Mohammad Abubakar Siddiq](https://github.com/bakar0208) (i212742@nu.edu.pk)**

---

### References:

* Ni, J., Li, J. and McAuley, J. (2019) ‘Justifying Recommendations using Distantly-Labeled Reviews and Fine-Grained Aspects’, *Empirical Methods in Natural Language Processing (EMNLP)* [Preprint]. Available at: https://cseweb.ucsd.edu//~jmcauley/pdfs/emnlp19a.pdf (Accessed: 25 June 2023).
* Vabalas, A. et al. (2019) *‘Machine learning algorithm validation with a limited sample size’*, PLOS ONE, 14(11). doi:10.1371/journal.pone.0224365.
* *Collaborative Filtering* (no date) *Google*. Available at: https://developers.google.com/machine-learning/recommendation/collaborative/basics (Accessed: 11 May 2023). 
