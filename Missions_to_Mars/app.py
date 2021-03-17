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
  # query Mongo database
  mars_data = mongo.db.mars_data.find_one()

  # pass the mars data into an HTML template to display the data
  return render_template("index.html", mars_data=mars_data)    


# Route that will trigger the scrape function
@app.route("/scrape")
def scraper():
  mars_data = mongo.db.mars_data
  take_mars = scrape_mars.scrape()
  mars_data.update({}, take_mars, upsert=True)
  return redirect("/", code=302)


if __name__ == "__main__":
  app.run(debug=True)
