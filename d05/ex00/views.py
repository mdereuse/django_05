from django.shortcuts import render
from django.conf import settings
import psycopg2


def init(request):
    sql_request = """
    CREATE TABLE IF NOT EXISTS ex00_movies (
        title           VARCHAR(64) UNIQUE NOT NULL,
        episode_nb      INT PRIMARY KEY,
        opening_crawl   TEXT,
        director        VARCHAR(32) NOT NULL,
        producer        VARCHAR(128) NOT NULL,
        release_date    DATE NOT NULL
    );
    """
    config = {
        "host": settings.DATABASES['default']['HOST'],
        "port": settings.DATABASES['default']['PORT'],
        "dbname": settings.DATABASES['default']['NAME'],
        "user": settings.DATABASES['default']['USER'],
        "password": settings.DATABASES['default']['PASSWORD'],
    }
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
    return render(request, 'ex00/init.html', context)
