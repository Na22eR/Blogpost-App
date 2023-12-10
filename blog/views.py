from django.shortcuts import render
from django.http import HttpResponse

posts = [
    {
        'author': 'Nasser Yacine',
        'title': 'First Blog Post',
        'content': 'Hello Blogpost-App!',
        'date_posted': 'Dezember 03, 2023'
    },
    {
        'author': 'J. K. Rowling',
        'title': 'Second Blog Post',
        'content': 'Beeing an author is boring.',
        'date_posted': 'Dezember 03, 2023'
    }
]


def home(request ):
    context = {
        'posts': posts
    }
    return render(request, 'home.html', context)

def about (request):
    return render(request, 'about.html', {'title': 'About'})
