import argparse
import collections
from datetime import date, timedelta
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pandas
from jinja2 import Environment, FileSystemLoader, select_autoescape


def years_with_you():
    year_from = date(year=1920, month=1, day=1)
    return (date.today() - year_from) // timedelta(days=365.2425)


def year_ending(year):
    year_end = ['год', 'года', 'лет']
    if year % 10 == 1 and year % 100 != 11:
        year = 0
    elif 2 <= year % 10 <= 4 and (year % 100 < 10 or year % 100 >= 20):
        year = 1
    else:
        year = 2
    return year_end[year]


def get_wines_by_categories():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', '-f', default='wine.xlsx', help='Выберите файл excel с данными')
    wine_file = parser.parse_args()
    exel_data_df = pandas.read_excel(wine_file.file, sheet_name='Лист1', na_values=['N/A', 'NA'], keep_default_na=False)
    wines = exel_data_df.to_dict(orient='records')

    wines_by_categories = collections.defaultdict(list)
    for wine in wines:
        wines_by_categories[wine['Категория']].append(wine)
    return wines_by_categories.items()


def main():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    rendered_page = template.render(
        years_with_you=years_with_you(),
        year_ending=year_ending(years_with_you()),
        wines=get_wines_by_categories(),

    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
