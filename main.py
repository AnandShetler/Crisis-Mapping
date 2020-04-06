from flask import Flask, render_template
import data

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("index.html", data=data.get_all_tables())