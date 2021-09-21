from flask import Flask, render_template, request, redirect, flash, url_for
import main
import urllib.request
from app import app
from werkzeug.utils import secure_filename
from main import getPrediction
from mongoconnect import connection_mongo, insert_data
import os
import keras
import numpy
import tensorflow
import flask
#import pillow

 

# @app.route('/', methods=['POST', 'GET'])
# def index():
#     if request.method == 'POST':
#         result = request.form
#         n = result['adresse']
#         return n
#     else:
#         return render_template('index.html')


 


def geolocal() : 
    
    
    return(render_template("geo2.html"))

def coord(): 
    latitude = request.form["latitude"]    
    longitude= request.form["longitude"]
    print(latitude, longitude)
    return longitude, latitude

