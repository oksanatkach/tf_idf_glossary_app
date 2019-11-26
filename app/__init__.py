from flask import Flask
import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask_bootstrap import Bootstrap

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
DOWNLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'downloads')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
bootstrap = Bootstrap(app)

from app.models import Session
session = Session()

from app import routes