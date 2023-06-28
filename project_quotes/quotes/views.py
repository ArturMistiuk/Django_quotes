from django.shortcuts import render, redirect
from .forms import AuthorForm, QuoteForm, TagForm


# Create your views here.
def main(request):
    return render(request, 'quotes/index.html')


def add_tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotes:main')
        else:
            return render(request, 'quotes/tag.html', {'form': form})

    return render(request, 'quotes/tag.html', {'form': TagForm()})


def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotes:main')
        else:
            return render(request, 'quotes/author.html', {'form': form})

    return render(request, 'quotes/author.html', {'form': AuthorForm()})


def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotes:main')
        else:
            return render(request, 'quotes/quote.html', {'form': form})

    return render(request, 'quotes/quote.html', {'form': QuoteForm()})
