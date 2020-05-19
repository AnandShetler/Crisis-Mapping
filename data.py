from googleapiclient import discovery
from google.oauth2 import service_account
from pprint import pprint #keep pprint just for testing, can remove later

import requests
import re
from bs4 import BeautifulSoup
import json

geo_id_dict = { "Alabama": 1,"Alaska": 2,"Arizona": 4,"Arkansas": 5,"California": 6,"Colorado": 8,"Connecticut": 9,"Delaware": 10,"District of Columbia":11,"Florida": 12,"Georgia": 13,"Hawaii": 15,"Idaho": 16,"Illinois": 17,"Indiana": 18,"Iowa": 19,"Kansas": 20,"Kentucky": 21,"Louisiana": 22,"Maine": 23,"Maryland": 24,"Massachusetts": 25,"Michigan": 26,"Minnesota": 27,"Mississippi": 28,"Missouri": 29,"Montana": 30,"Nebraska": 31,"Nevada": 32,"New Hampshire": 33,"New Jersey": 34,"New Mexico": 35,"New York": 36,"North Carolina": 37,"North Dakota": 38,"Ohio": 39,"Oklahoma": 40,"Oregon": 41,"Pennsylvania": 42,"Rhode Island": 44,"South Carolina": 45,"South Dakota": 46,"Tennessee": 47,"Texas": 48,"Utah": 49,"Vermont": 50,"Virginia": 51,"Washington": 53,"West Virginia": 54,"Wisconsin":55,"Wyoming": 56}

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

def gen_map_data(cases_table, col, policies_table=False):
    ret = []
    if policies_table:
        for i in range(3,len(policies_table)):
            ret.append([geo_id_dict[cases_table[i][0]],float(cases_table[i][2]) if not policies_table[i][col] == "-" else -1])
    else:
        for i in range(3,len(cases_table)):
            ret.append([geo_id_dict[cases_table[i][0]],float(cases_table[i][col].replace(",",""))])
    return ret

# pprint(gen_map_data(get_sheet_data('1BDbzCX0-m673QatijTXJhq7dh9p1RriQmUfBcUmbvZg', 'A1:E54'),3))
print(get_state_policies_key())