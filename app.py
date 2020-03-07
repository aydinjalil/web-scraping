from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


@app.route("/")
def home():
    scrape_data = mongo.db.collection.find()
    return render_template("index.html", news=mars_app)

@app.route("/scrape")
def scrape():
    # Run scraped functions
    nasa_info = scrape_mars.scrape_nasa()
    mars_image = scrape_mars.scrape_image()
    mars_weather = scrape_mars.scrape_weather()
    mars_html = scrape_mars.mars_facts()
    hemispheres = scrape_mars.hemispheres()

    # Store results into a dictionary
    post = {
        "title": nasa_info['title'],
        "paragraph": nasa_info['para'],
        "image": mars_image,
        "weather": mars_weather,
        "html": mars_html,
        "images": hemispheres
    }

    # Insert scraped news into database
    mongo.db.collection.insert_one(post)

    #Redirecting back to home page
    return redirect("/", code=302)


if __name__ == "+__main__":
    app.run(debug=True)
