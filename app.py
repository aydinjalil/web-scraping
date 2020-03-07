from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)
    app.config["MONGO_URI"] = "mongodb://localhost:27017/weather_app"