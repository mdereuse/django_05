from django.shortcuts import render
from .models import Movies


def populate(request):
    movies_lst = [
        {
            "episode_nb": 1,
            "title": "The Phantom Menace",
            "director": "George Lucas",
            "producer": "Rick McCallum",
            "release_date": "1999-05-19"
        },
        {
            "episode_nb": 2,
            "title": "Attack of the Clones",
            "director": "George Lucas",
            "producer": "Rick McCallum",
            "release_date": "2002-05-16"
        },
        {
            "episode_nb": 3,
            "title": "Revenge of the Sith",
            "director": "George Lucas",
            "producer": "Rick McCallum",
            "release_date": "2005-05-19"
        },
        {
            "episode_nb": 4,
            "title": "A New Hope",
            "director": "George Lucas",
            "producer": "Gary Kurtz, Rick McCallum",
            "release_date": "1977-05-25"
        },
        {
            "episode_nb": 5,
            "title": "The Empire Strikes Back",
            "director": "Irvin Kershner",
            "producer": "Gary Kurtz, Rick McCallum",
            "release_date": "1980-05-17"
        },
        {
            "episode_nb": 6,
            "title": "Return of the Jedi",
            "director": "Richard Marquand",
            "producer": "Howard G. Kazanjian, George Lucas, Rick McCallum",
            "release_date": "1983-05-25"
        },
        {
            "episode_nb": 7,
            "title": "The Force Awakens",
            "director": "J.J. Abrams",
            "producer": "Kathleen Kennedy, J.J. Abrams, Bryan Burk",
            "release_date": "2015-12-11"
        },
    ]
    message_lst = []
    for movie_features in movies_lst:
        try:
            movie = Movies.objects.create(
                **movie_features
            )
            movie.save()
        except Exception as e:
            message_lst.append(movie_features["title"])
            message_lst.append(str(e))
        else:
            message_lst.append(movie_features["title"])
            message_lst.append("OK")
    context = {
        "message_lst": message_lst
    }
    return render(request, 'ex03/populate.html', context)


def display(request):
    context = {}
    try:
        movies = Movies.objects.all()
        if len(movies) == 0:
            raise Exception
        context = {
            "movies": movies
        }
    except Exception:
        context = {
            "error_message": "No data available"
        }
    return render(request, 'ex03/display.html', context)


