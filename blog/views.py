from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Post


@login_required()
def home(request ):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'home.html', context)

@login_required()
def about (request):
    return render(request, 'about.html')
