
from flask import Flask, render_template
from sqlalchemy import create_engine

from pandas.core.indexes.base import Index
import requests
from bs4 import BeautifulSoup 
import pandas as pd
import numpy as np


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("base.html")

@app.route("/explore")
def explore():
    return render_template("explore.html")

@app.route("/versus")
def versus():
    return render_template("versus.html")

@app.route("/homepage")
def homepage():
    return render_template("base.html")

if __name__ == "__main__":
    app.run(debug=True)
