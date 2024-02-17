from django.shortcuts import render

def init(request):
    context = {}
    return render(request, 'ex00/init.html', context)
