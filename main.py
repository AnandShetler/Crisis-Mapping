from flask import Flask, render_template, url_for
import data

app = Flask(__name__)

@app.route('/')
def home_page():
    cases_by_state_table = data.get_sheet_data('1BDbzCX0-m673QatijTXJhq7dh9p1RriQmUfBcUmbvZg', 'A1:E54')
    policies_by_state_table = data.get_sheet_data(data.get_state_policies_key(), 'A1:I54')
    return render_template(
        "index.html", 
        cases_by_state=cases_by_state_table,
        policies_by_state=policies_by_state_table,
        num_of_cases_map=data.gen_map_data(cases_by_state_table,1),
        cases_per_mil_map=data.gen_map_data(cases_by_state_table,2),
        map_data_test=data.gen_map_data(cases_by_state_table,3,policies_by_state_table))