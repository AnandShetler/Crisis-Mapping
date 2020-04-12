from flask import Flask, render_template, url_for
import data

app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template("index.html", 
                            cases_by_state=data.get_sheet_data('1BDbzCX0-m673QatijTXJhq7dh9p1RriQmUfBcUmbvZg', 'A1:E54'),
                            policies_by_state=data.get_sheet_data('14EwUHhMnksYrYrNV7cX5rpCvASGQlcY3ZpKx-ErCmUE', 'A1:I54'))