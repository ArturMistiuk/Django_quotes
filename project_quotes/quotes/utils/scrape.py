import json
import os

import requests

from bs4 import BeautifulSoup
from pathlib import Path

base_url = 'http://quotes.toscrape.com/'
PAGES = 3

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

JSON_FOLDER_PATH = os.path.join(os.path.dirname(os.getcwd()), 'utils')
AUTHORS_JSON_PATH = os.path.join(BASE_DIR, 'quotes/utils/authors.json')
QUOTES_JSON_PATH = os.path.join(BASE_DIR, 'quotes/utils/quotes.json')


def save_authors_to_json(authors_info):

    with open(AUTHORS_JSON_PATH, 'w', encoding='utf-8') as file:
        json.dump(authors_info, file, indent=2, ensure_ascii=False)


def save_quotes_to_json(quotes):

    with open(QUOTES_JSON_PATH, 'w', encoding='utf-8') as file:
        json.dump(quotes, file, indent=2, ensure_ascii=False)


def run_parse():
    quotes = []
    authors = []

    for i in range(1, PAGES + 1):
        response = requests.get(f"{base_url}page/{i}/")
        soup = BeautifulSoup(response.text, 'lxml')

        for quote in soup.find_all("div", class_="quote"):
            text = quote.find("span", class_="text").get_text()
            tags = [tag.get_text() for tag in quote.find_all("a", class_="tag")]
            author = quote.find("small", class_="author").get_text().strip()
            author_url = quote.find("a", href=True).get('href').lstrip('/')

            quotes.append({
                "tags": tags,
                "author": author,
                "quote": text
            })

            if author_url not in authors:
                authors.append(author_url)

    save_quotes_to_json(quotes)

    authors_info = []
    for author in authors:
        response = requests.get(f"{base_url}{author}")
        soup = BeautifulSoup(response.text, 'lxml')

        fullname = soup.find("h3", class_="author-title").get_text().strip()
        born_date = soup.find("span", class_="author-born-date").get_text().strip()
        born_location = soup.find("span", class_="author-born-location").get_text().strip()
        description = soup.find("div", class_="author-description").get_text().strip()

        authors_info.append({
            "fullname": fullname,
            "born_date": born_date,
            "born_location": born_location,
            "description": description
        })

    save_authors_to_json(authors_info)


if __name__ == '__main__':
    run_parse()
