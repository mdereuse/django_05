from django.shortcuts import render
from .models import Planets, People


error_message = """
No data available, please use the following command line before use :
    python3 manage.py loaddata ex09/data/ex09_initial_data.json
"""


def display(request):
    try:
        people = (People.objects.filter(homeworld__climate__contains='windy')
                                .values('name', 'homeworld__name', 'homeworld__climate')
                                .order_by('name'))
        if len(people) == 0:
            raise Exception
    except Exception:
        context = {
            'error_message': error_message
        }
    else:
        context = {
            'people': people
        }
    return render(request, 'ex09/display.html', context)
