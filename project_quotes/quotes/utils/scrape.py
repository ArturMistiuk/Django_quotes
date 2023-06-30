import json
import os

import requests

from bs4 import BeautifulSoup


JSON_FOLDER_PATH = os.path.join(os.path.dirname(os.getcwd()), 'utils')
AUTHORS_JSON_PATH = os.path.join(JSON_FOLDER_PATH, 'authors.json')
QUOTES_JSON_PATH = os.path.join(JSON_FOLDER_PATH, 'quotes.json')


def save_authors_to_json(names, born_dates, born_locations, descriptions):

    authors_list = []
    for name, b_date, b_location, description in zip(names, born_dates, born_locations, descriptions):
        author_dict = {
            'fullname': name.text,
            'born_date': str(b_date),
            'born_location': str(b_location),
            'description': str(description).replace('\n', '').strip()
        }
        authors_list.append(author_dict)

    with open(AUTHORS_JSON_PATH, 'r', encoding='utf-8') as file:
        history = json.load(file)
        history.extend(authors_list)

    with open(AUTHORS_JSON_PATH, 'w', encoding='utf-8') as file:
        json.dump(history, file, indent=2, ensure_ascii=False)


def save_quotes_to_json(authors_list, quotes_list, tags_list):
    quotes_json_list = []

    for i in range(len(quotes_list)):
        tags_for_quote = tags_list[i].find_all('a', class_='tag')
        quote_dict = {
            'tags': [tag_for_quote.text for tag_for_quote in tags_for_quote],
            'author': authors_list[i].text,
            'quote': quotes_list[i].text
        }
        quotes_json_list.append(quote_dict)

    with open(QUOTES_JSON_PATH, 'r', encoding='utf-8') as file:
        history = json.load(file)
        history.extend(quotes_json_list)

    with open(QUOTES_JSON_PATH, 'w', encoding='utf-8') as file:
        json.dump(history, file, indent=2, ensure_ascii=False)


def run_parse():

    authors_born_dates = []
    authors_born_locations = []
    authors_description = []

    for page in range(1, 3):
        base_url = 'https://quotes.toscrape.com/'
        paginate_url = f"http://quotes.toscrape.com/page/{page}/"
        print(paginate_url)
        response = requests.get(paginate_url)
        soup = BeautifulSoup(response.text, 'lxml')
        quotes = soup.select('span.text')
        authors = soup.select('small.author')
        tags = soup.find_all('div', class_='tags')
        links_to_authors = soup.select('span a:not(.tag)')

        # Get list with links to every author about page
        for link in links_to_authors:
            link.attrs['href'] = base_url + link.attrs['href']
            response = requests.get(link.attrs['href'])
            soup = BeautifulSoup(response.text, 'lxml')
            authors_born_dates.append(soup.select('span.author-born-date')[0].text)
            authors_born_locations.append(soup.select('span.author-born-location')[0].text)
            authors_description.append(soup.select('div.author-description')[0].text)

        save_authors_to_json(authors, authors_born_dates, authors_born_locations, authors_description)
        save_quotes_to_json(authors, quotes, tags)


if __name__ == '__main__':
    run_parse()
