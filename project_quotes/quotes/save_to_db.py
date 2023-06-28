import json
import os
import django
from django.core.exceptions import MultipleObjectsReturned
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_quotes.settings')
django.setup()


from .models import Author, Tag, Quote
from .utils.scrape import JSON_FOLDER_PATH, AUTHORS_JSON_PATH, QUOTES_JSON_PATH


def add_authors():
    with open(r'C:\GHProjects\Django_quotes\project_quotes\quotes\utils\authors.json', 'r', encoding='utf-8') as file:
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
    with open(r'C:\GHProjects\Django_quotes\project_quotes\quotes\utils\quotes.json', 'r', encoding='utf-8') as file:
        quotes = json.load(file)
    for quote in quotes:
        try:
            author_obj = Author.objects.get(fullname=quote.get('author'))
        except MultipleObjectsReturned as error:
            print(error)
            author_obj = None
        tags_objects = []
        for tag in quote.get('tags'):
            tag_obj, created = Tag.objects.get_or_create(name=tag)
            if not created:
                tag_obj.save()
                tags_objects.append(tag_obj)
        if author_obj:
            quote_obj, created = Quote.objects.get_or_create(quote=quote.get('quote'), author=author_obj)
            if not created:
                for tag in tags_objects:
                    quote_obj.tags.add(tag)
                quote_obj.save()


if __name__ == '__main__':
    # add_authors()
    add_quotes()
