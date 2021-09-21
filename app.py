import flask
from flask import request, jsonify
from PIL import Image
from io import StringIO
from flask import make_response
import keras
import numpy
import tensorflow
#import pillow


from flask import Flask, session

app = Flask(__name__)
# Check Configuration section for more details
UPLOAD_FOLDER = "/Users/utilisateur/Desktop/projet chef-d'oeuvre/static/img_save/"


app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# <label>adresse</label> : <input type="text" name="adresse" />
# 	<input type="submit" value="Envoyer" />
