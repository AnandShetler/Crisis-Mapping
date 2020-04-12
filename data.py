from googleapiclient import discovery
from google.oauth2 import service_account
from pprint import pprint #keep pprint just for testing, can remove later

import requests
import re
from bs4 import BeautifulSoup
import json

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