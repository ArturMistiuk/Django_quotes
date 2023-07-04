from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .forms import AuthorForm, QuoteForm, TagForm

from .models import Quote, Tag, Author


# Create your views here.
def main(request, page=1):
    quotes = Quote.objects.all()
    per_page = 8
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    return render(request, 'quotes/index.html', {"quotes": quotes_on_page})


def author_detail(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    return render(request, 'quotes/author_detail.html', {'author': author})


@login_required
def add_tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.save()
            return redirect(to='quotes:main')
        else:
            return render(request, 'quotes/tag.html', {'form': form})

    return render(request, 'quotes/tag.html', {'form': TagForm()})


@login_required
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            new_author = form.save(commit=False)
            new_author.save()
            return redirect(to='quotes:main')
        else:
            return render(request, 'quotes/author.html', {'form': form})

    return render(request, 'quotes/author.html', {'form': AuthorForm()})


@login_required
def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save(commit=False)
            new_quote.save()
            return redirect(to='quotes:main')
        else:
            return render(request, 'quotes/quote.html', {'form': form})

    return render(request, 'quotes/quote.html', {'form': QuoteForm()})

