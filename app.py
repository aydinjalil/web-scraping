from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


@app.route("/")
def home():
    scrape_data = mongo.db.scrape_data.find_one()
    return render_template("index.html", scrape_data=scrape_data)
@app.route("/scrape")
def scrape():
    # Run scraped functions
    scrape_data = mongo.db.scrape_data
    mars_data = scrape_mars.scrape_nasa()
    mars_data = scrape_mars.scrape_image()
    mars_data = scrape_mars.scrape_weather()
    mars_data = scrape_mars.mars_facts()
    mars_data = scrape_mars.hemispheres()
    print(mars_data)
    scrape_data.update({}, mars_data, upsert=True)


    #Redirecting back to home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
