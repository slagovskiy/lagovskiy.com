from django.shortcuts import render


def index(request):
    content = {
    }
    return render(request, 'oadmin/index.html', content)