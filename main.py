import argparse
import collections
from datetime import date
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pandas
from jinja2 import Environment, FileSystemLoader, select_autoescape


def count_winery_age():
    foundation_year = 1920
    winery_age = date.today().year - foundation_year
    if winery_age % 10 == 1 and winery_age % 100 != 11:
        year_ending = 'год'
    elif 2 <= winery_age % 10 <= 4 and (winery_age % 100 < 10 or winery_age % 100 >= 20):
        year_ending = 'года'
    else:
        year_ending = 'лет'
    return f'{winery_age} {year_ending}'


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
        winery_age=count_winery_age(),
        wines=get_wines_by_categories(),
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
