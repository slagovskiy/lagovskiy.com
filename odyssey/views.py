from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    ids = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    context = {'ids': ids}
    return render(request, 'index.html', context)