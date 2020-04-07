from flask import Flask, render_template
import data

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("index.html", 
                            cases_by_state=data.get_sheet_data('1BDbzCX0-m673QatijTXJhq7dh9p1RriQmUfBcUmbvZg', 'A1:E54'),
                            policies_by_state=data.get_sheet_data('14EwUHhMnksYrYrNV7cX5rpCvASGQlcY3ZpKx-ErCmUE', 'A1:I54'))