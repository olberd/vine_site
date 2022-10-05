# from http.server import HTTPServer, SimpleHTTPRequestHandler
#
#
# server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
# server.serve_forever()
from datetime import date, timedelta
from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape


def years_with_you():
    year_now = date.today()
    year_from = date(year=1920, month=1, day=1)
    return (year_now - year_from) // timedelta(days=365.2425)


def year_ending(year):
    year_end = ['год', 'года', 'лет']
    if year % 10 == 1 and year % 100 != 11:
        year = 0
    elif 2 <= year % 10 <= 4 and (year % 100 < 10 or year % 100 >= 20):
        year = 1
    else:
        year = 2
    return year_end[year]


env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

rendered_page = template.render(
    years_with_you=years_with_you(),
    year_ending=year_ending(years_with_you()),

)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
