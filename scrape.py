import requests
import re
from bs4 import BeautifulSoup


def open_html(path):
    with open(path, 'rb') as f:
        return f.read()


def save_html(html, path):
    with open(path, 'wb') as f:
        f.write(html)


def get_soup_local(url):
    with open('site/' + url) as r:
        return BeautifulSoup(r.read(), 'html.parser')


def get_soup(url):
    r = requests.get(url)
    return BeautifulSoup(r.content, 'html.parser')


def crawl(next_url):
    recipe_links = []
    while next_url:
        cur_recipe_links = get_recipe_links(next_url)
        recipe_links += cur_recipe_links
        next_url = get_next_page_url(next_url)
        crawl(next_url)

    write_recipe_links(recipe_links)


def get_next_page_url(current_page_url):
    soup = get_soup_local(current_page_url)
    next_page_row = soup.select_one(
        'div.ui-pagination-outer-wrap > a.ui-pagination-btn__next')
    if not next_page_row:
        return None
    if next_page_row:
        return next_page_row.get('href')


def get_recipe_links(url):
    soup = get_soup_local(url)

    articles_section = soup.select_one(
        'section.c-category-flex__header-right')

    recipe_link_rows = articles_section.select('article > a.c-card__image-container')
    recipe_links = []

    for link_row in recipe_link_rows:
        link = link_row.get('href')
        if not link:
            continue
        if 'seriouseats.com/recipes' in link:
            recipe_links.append(link)

    return recipe_links


def write_recipe_links(recipe_links):
    f = open('recipe_links.txt', 'w')
    for link in recipe_links:
        f.write(link + '\n')


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
    #url = "https://www.seriouseats.com/recipes/topics/cuisine/american"
    url = 'https _www.seriouseats.com_recipes_topics_cuisine_american.html'
    crawl(url)


if __name__ == "__main__":
    main()
