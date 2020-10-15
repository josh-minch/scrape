import json

import numpy as np
import pandas as pd

from helper import get_json, write_json
from scrape import create_ingred_filters


def get_cooc():
    ingreds = get_json('all_ingreds_filtered.json')
    recipes = get_json('recipe_data_filtered.json')

    titles = []
    for recipe in recipes:
        titles.append(recipe['title'])

    df = pd.DataFrame(0, ingreds, titles)

    ingreds = set(ingreds)
    for recipe in recipes:
        recipe_ingreds = set(recipe['ingreds'])
        matches = recipe_ingreds & ingreds
        if len(matches) > 0:
            df.loc[list(matches), recipe['title']] += 1

    m = df.to_numpy()
    m = m.dot(m.transpose())
    np.fill_diagonal(m, 0)
    return m

def get_similar_ingreds(ingred):
    df = pd.read_json(get_json('df.json'))
    df = df[ingred].sort_values(ascending=False)
    return df


def get_similar_ingreds_np(ingred):
    ingreds = get_json('all_ingreds_filtered.json')
    ingred_to_ix = {k: v for v, k in enumerate(ingreds)}
    ix_to_ingred = {v: k for v, k in enumerate(ingreds)}

    cooc = np.array(get_json('cooc.json'))

    ix = ingred_to_ix[ingred]
    ranked_ixs = np.argsort(cooc[ix])
    ranked_ixs = np.flip(ranked_ixs)

    ingreds = [ix_to_ingred[ix] for ix in ranked_ixs]

    return ingreds

def main():
    print(get_similar_ingreds_np('bacon'))




if __name__ == "__main__":
    main()


""" def get_all_ingreds():
    filters = create_ingred_filters()
    ingreds = filters['general'] + filters['special']
    ingreds.sort()
    ingreds = [ingred.lower for ingred in ingreds]
    return ingreds


def init_cooc_matrix():
    ingreds = get_all_ingreds()

    matrix = {}
    for ingred in ingreds:
        matrix[ingred] = {}
        for nested_ingred in ingreds:
            matrix[ingred][nested_ingred] = 0

    return matrix


def fill_cooc_matrix(matrix, recipe_filename):
    recipes = get_json(recipe_filename)

    for key in matrix.keys():
        for recipe in recipes:
            ingreds = recipe['ingreds']
            for ingred in ingreds:
                matrix[key][ingred] += 1

    return matrix


def create_cooc_matrix(recipe_filename):
    matrix = init_cooc_matrix()
    matrix = fill_cooc_matrix(matrix, recipe_filename)
    return matrix
 """
