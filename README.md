# Wikipedia Scraper Project

## Overview

The Wikipedia Scraper Project is designed to automate the collection of information about political leaders from various countries, as listed on a custom API endpoint. It fetches data including names and Wikipedia links, scrapes the first paragraph of their Wikipedia page for a summary, and compiles this information into a structured JSON file.

## Features

- Retrieves a list of countries from the custom API.
- Fetches details about political leaders for each country.
- Scrapes Wikipedia for the first paragraph of each leader's profile.
- Stores the collected data in a JSON file for easy access and analysis.

## Prerequisites

- Python 3.x
- Libraries: `requests`, `bs4` (BeautifulSoup), `json`, `re`
- Internet access for API and Wikipedia page requests

## Installation

1. Ensure Python 3.x is installed on your system.
2. Clone this repository or download the source code.
3. Install required Python libraries: pip install requests beautifulsoup4

## Usage

1. Navigate to the project directory.
2. Run the main script: python main.py

3. The script will automatically fetch data and store it in `leaders_data.json` in the project directory.

## Structure

- `main.py`: The entry point of the script that orchestrates the scraping process.
- `src/scraper.py`: Contains the `WikipediaScraper` class responsible for all scraping operations.
- `leaders_data.json`: Output file containing the scraped data.

## How It Works

1. **Initialization**: The `WikipediaScraper` class initializes with the base URLs for the API and sets up a session.
2. **Cookie Management**: Manages session cookies for authenticated API requests.
3. **Country Retrieval**: Fetches a list of countries for which leader information is available.
4. **Leader Information Retrieval**: For each country, the script fetches details of political leaders.
5. **Wikipedia Scraping**: Accesses Wikipedia pages of each leader to scrape the introductory paragraph.
6. **Data Compilation**: Compiles all fetched information into a structured format and saves it as a JSON file.

## Contributions

Contributions to this project are welcome. Please fork the repository and submit a pull request with your enhancements.

## Contact

For questions and feedback, please reach out to [https://www.linkedin.com/in/yanina-andriienko-7a2984287/].
