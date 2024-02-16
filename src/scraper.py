import re
import requests
from bs4 import BeautifulSoup
import json


class WikipediaScraper:

    def __init__(self):
        self.base_url = "https://country-leaders.onrender.com"
        self.country_endpoint = "/countries"
        self.cookies_endpoint = "/cookie/"
        self.leaders_data = {}
        self.countries = []
        self.session = requests.Session()
        self.cookie = self.refresh_cookie()

    def refresh_cookie(self):
        url = self.base_url + self.cookies_endpoint
        response = self.session.get(url)
        if response.status_code == 200:
            return response.cookies
        elif response.status_code == 403:
            print(
                f"Error code: {response.status_code}, Cookie has expired. Refreshing cookie")
        else:
            raise ValueError(f"Error code: {response.status_code}")

    def get_countries(self):
        self.refresh_cookie()
        response = self.session.get(self.base_url + self.country_endpoint)
        if response.ok:
            self.countries = response.json()

    def get_leaders(self):
        for country in self.countries:
            url = self.base_url + '/leaders?country=' + country
            leaders_response = self.session.get(url, cookies=self.cookie)

            if leaders_response.status_code != 200:  # If cookies are expired or invalid
                self.cookie = self.refresh_cookie()  # Fetch new cookie
                leaders_response = self.session.get(url, cookies=self.cookie)

            leaders_data = leaders_response.json() if leaders_response.ok else []

            # Initialize the list for the country
            self.leaders_data[country] = []

            for leader in leaders_data:
                first_paragraph = self.get_first_paragraph(
                    leader['wikipedia_url'])
                self.leaders_data[country].append({
                    'first_name': leader['first_name'],
                    'last_name': leader['last_name'],
                    'wikipedia_url': leader['wikipedia_url'],
                    'first_paragraph': first_paragraph
                })

    def get_first_paragraph(self, wikipedia_url):
        response = self.session.get(wikipedia_url)
        soup = BeautifulSoup(response.text, 'lxml')
        paragraphs = soup.find_all('p')

        for p in paragraphs:
            if p.text.strip():
                first_paragraph = re.sub(
                    r"\(.*?\)|\[.*?\]|[\n\t]|[\xa0]", '', p.text)
                if len(first_paragraph) > 100:
                    return first_paragraph
        return None

    def to_json_file(self, filepath):
        with open(filepath, "w") as json_file:
            json.dump(self.leaders_data, json_file)
