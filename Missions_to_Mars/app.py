# import necessary libraries
from flask import Flask, render_template, redirect
import scrape_mars

### Here I switched from pymongo to PyMongo from flask_pymongo so that flask can automatically make the mongo connection
# import pymongo
from flask_pymongo import PyMongo


### Here I switched from pymongo to PyMongo from flask_pymongo so that flask can automatically make the mongo connection

# #NOTE: This must have the MongoDB connection running first, so be sure to double-check it. You have to type "mongo" in the terminal before you start the program
# # The default port used by MongoDB is 27017
# # https://docs.mongodb.com/manual/reference/default-mongodb-port/
# # create instance of Flask app
# app = Flask(__name__)
# conn = 'mongodb://localhost:27017'
# client = pymongo.MongoClient(conn)
# # Declare the database
# db = client.mars_assignment_db
# # Drops collection in case there is a duplicate already there
# db.collection.drop()
# # Declare the collection
# collection = db.mars_assignment_db


# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_assignment_db")



# create route that renders index.html template
@app.route("/")
def echo():
    # Find one record of data from the mongo database
    mars_dictionary = mongo.db.collection.find_one()
    # Return template and data    
    return render_template("index.html", mars_dictionary=mars_dictionary)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function    
    scraped_data = scrape_mars.scrape()
    print(f"{scraped_data}")

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, scraped_data, upsert=True)

    ##This is http code (302) that means redirect. The "/" is where it will redirect to, which here means the homepage of index.html
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
