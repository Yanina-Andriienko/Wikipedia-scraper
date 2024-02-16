import json
from bs4 import BeautifulSoup
import requests
import re


def get_first_paragraph(wikipedia_url):

    print(wikipedia_url)  # keep this for the rest of the notebook
    session = requests.Session()
    req = session.get(wikipedia_url).text
    soup = BeautifulSoup(req, 'lxml')
    paragraphs = soup.find_all('p')

    first_paragraph = None
    regex_list = [r"\(.*?\)|\[.*?\]", r"[\n\t]", "[\xa0]"]
    for p in paragraphs:
        if p.text.strip():
            first_paragraph = p.text
            for regex in regex_list:
                first_paragraph = re.sub(regex, '', first_paragraph)

            if len(first_paragraph) > 100:
                break

    return first_paragraph


def get_leaders():

    root_url = 'https://country-leaders.onrender.com'
    cookie_url = root_url + '/cookie/'
    countries_url = root_url + '/countries'

    def get_cookies():

        return requests.get(cookie_url).cookies

    cookies = get_cookies()

    session = requests.Session()  # Create a session object
    countries_response = session.get(countries_url, cookies=cookies)
    countries = countries_response.json()
    leaders_per_country = {}

    for country in countries:

        leaders_url = root_url + '/leaders?country=' + country
        leaders_response = session.get(leaders_url, cookies=cookies)
        # Check if cookies are expired or invalid
        if leaders_response.status_code != 200:  # Assuming non-200 status code indicates cookie error
            cookies = get_cookies()  # Fetch new cookie
            # Retry the request with new cookies
            leaders_response = requests.get(leaders_url, cookies=cookies)
        leaders_data = leaders_response.json() if leaders_response.ok else []

        leaders_per_country[country] = []

        for leader in leaders_data:

            first_paragraph = get_first_paragraph(leader['wikipedia_url'])
            leaders_per_country[country].append({
                'first_name': leader['first_name'],
                'last_name': leader['last_name'],
                'wikipedia_url': leader['wikipedia_url'],
                'first_paragraph': first_paragraph

            })

    return leaders_per_country


def save(leaders_per_country):
    with open("leaders.json", "w") as outfile:
        json.dump(leaders_per_country, outfile)


result = get_leaders()          # calls for 'get leader' function
print(result)                   # prints results

save(result)                # calls for 'save' function

with open('leaders.json', 'r') as fp:      # opens saved file
    data = json.load(fp)                   # stores result into 'data' variable

print(data)                              # prints data variable
