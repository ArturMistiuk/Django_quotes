import json
import os
import django
from django.core.exceptions import MultipleObjectsReturned
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_quotes.settings')
django.setup()

from .models import Author, Tag, Quote
from .utils.scrape import AUTHORS_JSON_PATH, QUOTES_JSON_PATH


def add_authors():
    with open(AUTHORS_JSON_PATH, 'r', encoding='utf-8') as file:
        authors = json.load(file)
        for author in authors:
            author_object, created = Author.objects.get_or_create(
                fullname=author.get('fullname'),
                born_date=author.get('born_date'),
                born_location=author.get('born_location'),
                description=author.get('description')
                )
            if not created:
                author_object.save()


def add_quotes():
    with open(QUOTES_JSON_PATH, 'r', encoding='utf-8') as file:
        quotes = json.load(file)
    for quote in quotes:
        tags = []
        for tag in quote['tags']:
            t, *_ = Tag.objects.get_or_create(name=tag)
            tags.append(t)

        exist_quote = bool(len(Quote.objects.filter(quote=quote['quote'])))
        if not exist_quote:

            a = Author.objects.get(fullname=quote['author'])
            q = Quote.objects.create(
                quote=quote['quote'],
                author=a
            )
            for tag in tags:
                q.tags.add(tag)


if __name__ == '__main__':
    add_authors()
    add_quotes()
