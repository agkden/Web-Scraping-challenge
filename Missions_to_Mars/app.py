# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
#import pymongo
import scrape_mars


# Create instance of Flask app
app = Flask(__name__)


# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


# Route to render index.html template using data from Mongo
@app.route("/")
def index():        

  #return render_template("index.html")


# Route that will trigger the scrape function
@app.route("/scrape")
def scraper():
  
  #return redirect("/", code=302)


if __name__ == "__main__":
  app.run(debug=True)
