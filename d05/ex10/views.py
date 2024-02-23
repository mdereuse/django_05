from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from .forms import SearchPersonForm
from .models import People, Planets, Movies
from django.db.models import FilteredRelation, Q


def index(request):
    def get_choices():
        try:
            gender_qlst = list(People.objects.order_by().values_list('gender').distinct())
            gender_lst = [g[0] for g in gender_qlst]
        except Exception as e:
            print(e)
            raise
        else:
            choices = ((g, g) for g in gender_lst)
            return choices

    def get_results(min_date, max_date, min_diameter, gender):
        results_characters = (People.objects.filter(gender=gender)
                                            .filter(homeworld__diameter__gt=min_diameter))
        results = (Movies.objects.filter(characters__in=results_characters)
                                 .exclude(release_date__lt=min_date)
                                 .exclude(release_date__gt=max_date)
                                 .values('title',
                                         'characters__gender',
                                         'characters__name',
                                         'characters__homeworld__name',
                                         'characters__homeworld__diameter'))
        print(results)
        return results
    
    try:
        choices = get_choices()
        context = {}
        context['results'] = None
        if request.method == 'POST':
            form = SearchPersonForm(choices, request.POST)
            if form.is_valid():
                results = get_results(
                    min_date=form.cleaned_data['min_movie_release_date'],
                    max_date=form.cleaned_data['max_movie_release_date'],
                    min_diameter=form.cleaned_data['min_planet_diameter'],
                    gender=form.cleaned_data['gender']
                )
                context['results'] = results
        form = SearchPersonForm(choices)
        context['form'] = form
    except Exception as e:
        print(e)
        context = {
            'error_message': 'Oups'
        }
    return render(request, 'ex10/index.html', context)

