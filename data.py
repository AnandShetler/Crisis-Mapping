from googleapiclient import discovery
from google.oauth2 import service_account
from pprint import pprint #keep pprint just for testing, can remove later

def get_sheet_data(spreadsheet_id, range_):
    credentials = service_account.Credentials.from_service_account_file("sheetsAPICredentials.json")
    service = discovery.build('sheets', 'v4', credentials=credentials)
    request = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_)
    response = request.execute()
    return response
