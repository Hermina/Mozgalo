from django.shortcuts import render

def index(request):
    context = {}
    return render(request, 'dokumentacija/index.html', context)

def wiki(request):
    context = {}
    return render(request, 'dokumentacija/wiki.html', context)
