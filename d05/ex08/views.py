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
    CREATE TABLE IF NOT EXISTS ex08_planets (
        id              SERIAL PRIMARY KEY,
        name            VARCHAR(64) UNIQUE NOT NULL,
        climate         VARCHAR,
        diameter        INT,
        orbital_period  INT, 
        population      BIGINT,
        rotation_period INT,
        surface_water   REAL,
        terrain         VARCHAR(128)
    );
    CREATE TABLE IF NOT EXISTS ex08_people (
        id          SERIAL PRIMARY KEY,
        name        VARCHAR(64) UNIQUE NOT NULL,
        birth_year  VARCHAR(32),
        gender      VARCHAR(32),
        eye_color   VARCHAR(32),
        hair_color  VARCHAR(32),
        height      INT,
        mass        REAL,
        homeworld   VARCHAR(64),
        CONSTRAINT  fk_planet
            FOREIGN KEY (homeworld)
            REFERENCES ex08_planets(name)
    );
    """
    conn = None
    try:
        conn = psycopg2.connect(**config)
        with conn:
            with conn.cursor() as curs:
                curs.execute(sql_request)
    except Exception as e:
        message = str(e)
    else:
        message = 'OK'
    finally:
        if conn is not None:
            conn.close()
    context = {
        'message': message
    }
    return render(request, 'ex08/init.html', context)


def populate(request):
    populate_lst = [
        {
            "data": "ex08/data/planets.csv",
            "table": "ex08_planets",
            'columns': (
                'name',
                'climate',
                'diameter',
                'orbital_period',
                'population',
                'rotation_period',
                'surface_water',
                'terrain'
            )
        },
        {
            "data": "ex08/data/people.csv",
            "table": "ex08_people",
            'columns': (
                'name',
                'birth_year',
                'gender',
                'eye_color',
                'hair_color',
                'height',
                'mass',
                'homeworld'
            )
        },
    ]
    message_lst = []
    for pop in populate_lst:
        conn = None
        try:
            conn = psycopg2.connect(**config)
            with conn:
                with conn.cursor() as curs:
                    with open(pop["data"], "r") as f:
                        curs.copy_from(f, pop["table"], null='NULL', columns=pop["columns"])
        except Exception as e:
            message_lst.append(pop["table"])
            message_lst.append(str(e))
        else:
            message_lst.append(pop['table'])
            message_lst.append('OK')
        finally:
            if conn is not None:
                conn.close()
    context = {
        'message_lst': message_lst
    }
    return render(request, 'ex08/populate.html', context)


def display(request):
    sql_request = """
    SELECT
        people.name as people_name, 
        planets.name as planet_name,
        planets.climate as planet_climate
    FROM ex08_people as people
    LEFT JOIN ex08_planets as planets
    ON people.homeworld = planets.name
    WHERE planets.climate LIKE '%windy%'
    ORDER BY people.name ASC
    ;
    """
    conn = None
    try:
        conn = psycopg2.connect(**config)
        with conn:
            with conn.cursor() as curs:
                curs.execute(sql_request)
                people = curs.fetchall()
    except Exception:
        context = {
            'error_message': 'No data available'
        }
    else:
        context = {
            'people': people
        }
    finally:
        if conn is not None:
            conn.close()
    return render(request, 'ex08/display.html', context)
