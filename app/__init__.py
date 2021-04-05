from flask import Flask
# sdasd

app = Flask(__name__, template_folder='templates' , static_folder='static/css')
from app import admin


