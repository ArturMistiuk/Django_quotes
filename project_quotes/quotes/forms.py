from django.forms import ModelForm, CharField, TextInput, ModelMultipleChoiceField, SelectMultiple, Select, ModelChoiceField
from .models import Tag, Author, Quote


class TagForm(ModelForm):
    name = CharField(min_length=3, max_length=30, required=True, widget=TextInput())

    class Meta:
        model = Tag
        fields = ['name']


class AuthorForm(ModelForm):
    fullname = CharField(min_length=3, max_length=120, required=True, widget=TextInput())
    born_date = CharField(max_length=120, required=True, widget=TextInput())
    born_location = CharField(max_length=30, required=True, widget=TextInput())
    description = CharField(max_length=2000, required=True, widget=TextInput())

    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']


class QuoteForm(ModelForm):
    quote = CharField(max_length=2000, required=True, widget=TextInput())
    author = ModelChoiceField(queryset=Author.objects.all(), widget=Select())
    tags = ModelMultipleChoiceField(queryset=Tag.objects.all(), widget=SelectMultiple())

    class Meta:
        model = Quote
        fields = ['quote', 'author', 'tags']
