from os import path
import requests
import re
from bs4 import BeautifulSoup


def get_soup_local(url):
    with open('site/' + url) as r:
        return BeautifulSoup(r.read(), 'html.parser')


def get_soup(url):
    r = requests.get(url)
    return BeautifulSoup(r.content, 'html.parser')


def crawl(next_url):
    if next_url:
        recipe_urls = request_recipe_urls(next_url)
        write_recipe_urls(recipe_urls)
        next_url = get_next_page_url(next_url)
        return crawl(next_url)


def get_next_page_url(current_page_url):
    soup = get_soup(current_page_url)
    next_page_row = soup.select_one(
        'div.ui-pagination-outer-wrap > a.ui-pagination-btn__next')
    if not next_page_row:
        return None
    if next_page_row:
        return next_page_row.get('href')


def request_recipe_urls(url):
    soup = get_soup(url)

    recipes_section = soup.select_one('#recipes')

    recipe_link_rows = recipes_section.select(
        'a.module__image-container.module__link')
    recipe_urls = []

    for link_row in recipe_link_rows:
        link = link_row.get('href')
        if not link:
            continue
        #if 'seriouseats.com/recipes' in link:
        recipe_urls.append(link)

    return recipe_urls


def write_recipe_urls(recipe_urls):
    f = open('recipe_urls.txt', 'a')
    for url in recipe_urls:
        f.write(url + '\n')


def open_html(path):
    with open(path, 'rb') as f:
        return f.read()


def save_html(html, pathname):
    with open(pathname, 'wb') as f:
        f.write(html)


def extract_recipe_urls(filename):
    with open(filename) as f:
        urls = f.read().splitlines()
        return urls


def request_recipes_html(urls):
    path_base = 'html/serious'
    path_index = 0
    for url in urls:
        full_path = '{}{}.html'.format(path_base, str(path_index))

        if not path.exists(full_path):
            html = requests.get(url).content
            save_html(html, full_path)

        path_index += 1

def save_recipe_html_from_urls(filename):
    urls = extract_recipe_urls(filename)
    request_recipes_html(urls)

def scrape(url):
    soup = get_soup(url)

    recipe_row = soup.select_one('.recipe-title')
    recipe = recipe_row.text

    ingredient_rows = soup.select('.ingredient')
    ingredients = [ingredient_row.text for ingredient_row in ingredient_rows]

    prog = re.compile(
        '[-]?[0-9]+[,.]?[0-9]*([\/][0-9]+[,.]?[0-9]*)* (?:cups?|(table|tea)spoons?)?')
    ingred_stripped = []
    for ingred in ingredients:
        ingred_stripped.append(prog.sub('', ingred).strip())


def main():
    save_recipe_html_from_urls('recipe_urls.txt')


if __name__ == "__main__":
    main()
