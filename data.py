from googleapiclient import discovery
from google.oauth2 import service_account

import requests
import re
from bs4 import BeautifulSoup
import json
import pandas as pd

geo_id_dict = { "Alabama": 1,"Alaska": 2,"Arizona": 4,"Arkansas": 5,"California": 6,"Colorado": 8,"Connecticut": 9,"Delaware": 10,"District of Columbia":11,"Florida": 12,"Georgia": 13,"Hawaii": 15,"Idaho": 16,"Illinois": 17,"Indiana": 18,"Iowa": 19,"Kansas": 20,"Kentucky": 21,"Louisiana": 22,"Maine": 23,"Maryland": 24,"Massachusetts": 25,"Michigan": 26,"Minnesota": 27,"Mississippi": 28,"Missouri": 29,"Montana": 30,"Nebraska": 31,"Nevada": 32,"New Hampshire": 33,"New Jersey": 34,"New Mexico": 35,"New York": 36,"North Carolina": 37,"North Dakota": 38,"Ohio": 39,"Oklahoma": 40,"Oregon": 41,"Pennsylvania": 42,"Rhode Island": 44,"South Carolina": 45,"South Dakota": 46,"Tennessee": 47,"Texas": 48,"Utah": 49,"Vermont": 50,"Virginia": 51,"Washington": 53,"West Virginia": 54,"Wisconsin":55,"Wyoming": 56}
population_dict = { "California": 39512223, "Texas": 28995881, "Florida": 21477737, "New York": 19453561, "Pennsylvania": 12801989, "Illinois": 12671821, "Ohio": 11689100, "Georgia": 10617423, "North Carolina": 10488084, "Michigan": 9986857, "New Jersey": 8882190, "Virginia": 8535519, "Washington": 7614893, "Arizona": 7278717, "Massachusetts": 6949503, "Tennessee": 6833174, "Indiana": 6732219, "Missouri": 6137428, "Maryland": 6045680, "Wisconsin": 5822434, "Colorado": 5758736, "Minnesota": 5639632, "South Carolina": 5148714, "Alabama": 4903185, "Louisiana": 4648794, "Kentucky": 4467673, "Oregon": 4217737, "Oklahoma": 3956971, "Connecticut": 3565287, "Utah": 3205958, "Iowa": 3155070, "Puerto Rico": 3193694, "Nevada": 3080156, "Arkansas": 3017825, "Mississippi": 2976149, "Kansas": 2913314, "New Mexico": 2096829, "Nebraska": 1934408, "Idaho": 1787065, "West Virginia": 1792147, "Hawaii": 1415872, "New Hampshire": 1359711, "Maine": 1344212, "Montana": 1068778, "Rhode Island": 1059361, "Delaware": 973764, "South Dakota": 884659, "North Dakota": 762062, "Alaska": 731545, "District of Columbia": 705749, "Vermont": 623989, "Wyoming": 578759, "Guam": 165718, "U.S. Virgin Islands": 104914, "American Samoa": 55641 }

def get_sheet_data(spreadsheet_id, range_):
    credentials = service_account.Credentials.from_service_account_file("sheetsAPICredentials.json")
    service = discovery.build('sheets', 'v4', credentials=credentials)
    request = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_)
    response = request.execute()
    return response['values']

def get_state_policies_key():
    page = requests.get("https://www.kff.org/health-costs/issue-brief/state-data-and-policy-actions-to-address-coronavirus/")
    soup = BeautifulSoup(page.content, features="html.parser")
    tables = soup.find_all('div', attrs={'data-app-js':re.compile("[\{]")})
    return json.loads(tables[3]['data-app-js'])['gdocs_key']

# if no policy_table then returns list of [geo id, number value] pairs
# if policy_table exists then returns list of [list of policy names, list of [geo id, index of associated policy type] pairs]
def gen_map_data(cases_table, col, policies_table=False):
    ret = []
    if policies_table:
        names = policies_table[2][col].split("; ")
        for i in range(0,len(names)):
            x = names[i].replace("Grace Period Extended for ","")
            names[i] = x[:(x.index("(")-1)]
        for i in range(3,len(policies_table)):
            str = policies_table[i][col] if not "Proposed" in policies_table[i][col] else "Proposed"
            ret.append([geo_id_dict[cases_table[i][0]],len(names)-1 if str == "-" else names.index(str)])
        return [names, ret]
    else:
        for i in range(3,len(cases_table)):
            ret.append([geo_id_dict[cases_table[i][0]],float(cases_table[i][col].replace(",",""))])
        return ret

# returns dict of state : [new cases from 1/22 to most recent]
def state_cases_over_time():
    data = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv")
    out = {"Date" : data.keys().tolist()[11:]}
    data = data.values.tolist()
    for i in range(1, len(data)):
        dx = [data[i][11]]
        for x in range(12, len(data[0])):
            dx.append(data[i][x]-data[i][x-1])
        state = data[i][6]
        if (state in out):
            out[state] = list(map(lambda x,y: x+y, out[state], dx))
        else:
            out[state] = dx
    return out

def gen_policy_chart_data(policy_index, policy_table, state_cases_dx):
    occurrences = { "No Action": 0, "US Average": 50 }
    table_dict = { "Date": state_cases_dx["Date"], "No Action": [0 for x in range(0, len(state_cases_dx["Alaska"]))], "US Average": [0 for x in range(0, len(state_cases_dx["Alaska"]))] }
    for i in range(3, len(policy_table)):
        case = policy_table[i][policy_index]
        state = policy_table[i][0]
        table_dict["US Average"] = list(map(lambda x,y: x+(y*1000000/population_dict[state]), table_dict["US Average"], state_cases_dx[state]))
        if case in occurrences:
            occurrences[case] += 1
            table_dict[case] = list(map(lambda x,y: x+(y*1000000/population_dict[state]), table_dict[case], state_cases_dx[state]))
        else:
            if case == "-":
                occurrences["No Action"] += 1
                table_dict["No Action"] = list(map(lambda x,y: x+(y*1000000/population_dict[state]), table_dict["No Action"], state_cases_dx[state]))
            else:
                occurrences[case] = 1
                table_dict[case] = list(map(lambda x: (x*1000000/population_dict[state]), state_cases_dx[state]))
    for key in list(table_dict.keys())[1:]:
        if not occurrences[key] == 0:
            table_dict[key] = list(map(lambda x: x/occurrences[key], table_dict[key]))
    help = pd.DataFrame(data=table_dict)
    return [help.columns.values.tolist()] + help.values.tolist()