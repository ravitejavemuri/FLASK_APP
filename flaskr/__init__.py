import os
from flask import Flask, render_template
import requests
import json
import csv
import pandas as pd 
from sklearn.cluster import KMeans

headers = {
    "content-type": "application/json"
}

def create_app(test_config = None):
    # create and configure th app
    app = Flask(__name__,instance_relative_config=True )
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        DATABASE = os.path.join(app.instance_path,'flaskr.sqlite'),
    )
 
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/dog')
    def dog():
        response =  requests.get("https://dog.ceo/api/breed/boxer/images/random",headers)
        data = response.json()
        return render_template("dogs.html", url=data['message'] )
    @app.route('/')
    def index():
        return "Index"
    @app.route('/render')
    def render():
        return render_template("base.html", message="Hello Flask!")
    @app.route('/learn')
    def learn():
        feature = []
        response = requests.get("https://raw.githubusercontent.com/datasets/investor-flow-of-funds-us/master/data/weekly.csv")
        resp_decoded = response.content.decode('utf-8')
        cr = csv.reader(resp_decoded.splitlines(), delimiter=',')
        my_list = list(cr)
        data = pd.DataFrame(my_list)
        data = data.drop([0], axis=1)
        data = data.drop([0], axis=0)
        data_top = data.head(10)
        # print(data[1])
        kmeans= KMeans(n_clusters=4).fit(data_top)
        labels = kmeans.labels_
        print(labels)
        print(kmeans.cluster_centers_)
        print(kmeans.predict(data.head(20)))

        return resp_decoded
    
        
    return app   