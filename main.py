from flask import Flask
import data

app = Flask(__name__)

@app.route('/')
def hello_world():
    return data.get_all_tables()