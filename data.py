import requests
import re
from bs4 import BeautifulSoup

def get_all_tables():
    page = requests.get("https://www.kff.org/health-costs/issue-brief/state-data-and-policy-actions-to-address-coronavirus/")
    soup = BeautifulSoup(page.content, features="html.parser")
    tables = soup.find_all('div', attrs={'data-app-js':re.compile("[\{]")})
    # print(tables)
    ret = ""
    for x in tables:
        ret += str(x)
    return ret

print(get_all_tables())