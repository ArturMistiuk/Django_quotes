from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import AuthorForm, QuoteForm, TagForm

from .models import Quote, Tag, Author


# Create your views here.
def main(request):
    quotes = Quote.objects.filter(user=request.user).all() if request.user.is_authenticated else []
    return render(request, 'quotes/index.html', {"quotes": quotes})


@login_required
def add_tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.user = request.user
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
            new_author.user = request.user
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
            new_quote.user = request.user
            new_quote.save()
            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'), user=request.user)
            choice_author = Author.objects.filter(name__in=request.POST.getlist('author'), user=request.user)
            return redirect(to='quotes:main')
        else:
            return render(request, 'quotes/quote.html', {'form': form})

    return render(request, 'quotes/quote.html', {'form': QuoteForm()})

