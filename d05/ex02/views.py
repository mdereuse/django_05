from django.shortcuts import render
from django.conf import settings
import psycopg2


config = {
    "host": settings.DATABASES['default']['HOST'],
    "port": settings.DATABASES['default']['PORT'],
    "dbname": settings.DATABASES['default']['NAME'],
    "user": settings.DATABASES['default']['USER'],
    "password": settings.DATABASES['default']['PASSWORD'],
}


def init(request):
    sql_request = """
    CREATE TABLE IF NOT EXISTS ex02_movies (
        title           VARCHAR(64) UNIQUE NOT NULL,
        episode_nb      INT PRIMARY KEY,
        opening_crawl   TEXT,
        director        VARCHAR(32) NOT NULL,
        producer        VARCHAR(128) NOT NULL,
        release_date    DATE NOT NULL
    );
    """
    conn = None
    try:
        conn = psycopg2.connect(**config)
        with conn:
            with conn.cursor() as curs:
                curs.execute(sql_request)
    except Exception as e:
        message = e
    else:
        message = "OK"
    finally:
        if conn is not None:
            conn.close()
    context = {"message": message}
    return render(request, 'ex02/init.html', context)


def populate(request):
    sql_request = """
    INSERT INTO ex02_movies (
        episode_nb,
        title,
        director,
        producer,
        release_date
    ) VALUES (
        {episode_nb},
        \'{title}\',
        \'{director}\',
        \'{producer}\',
        \'{release_date}\'
    );
    """
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
    conn = None
    try:
        conn = psycopg2.connect(**config)
        for movie in movies_lst:
            movie_sql_request = sql_request.format(
                **movie
            )
            try:
                with conn:
                    with conn.cursor() as curs:
                        curs.execute(movie_sql_request)
            except Exception as e:
                message_lst.append(movie["title"])
                message_lst.append(str(e))
            else:
                message_lst.append(movie["title"])
                message_lst.append("OK")
    except Exception as e:
        message_lst = [str(e)]
    finally:
        if conn is not None:
            conn.close()
    context = {"message_lst": message_lst}
    return render(request, 'ex02/populate.html', context)

def display(request):
    sql_request = """
    SELECT * FROM ex02_movies;
    """
    conn = None
    try:
        conn = psycopg2.connect(**config)
        with conn:
            with conn.cursor() as curs:
                curs.execute(sql_request)
                movies = curs.fetchall()
        if len(movies) == 0:
            raise Exception
        context = {
            "movies": movies
        }
    except Exception:
        context = {
            "error_message": "No data available"
        }
    finally:
        if conn is not None:
            conn.close()
    return render(request, 'ex02/display.html', context)
