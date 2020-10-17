import json
import collections

import numpy as np

from helper import get_json, write_json

def get_ranked_ingreds(ingreds, recipe_matrix, all_ingreds):
    """Return ingreds from recipes in order of occurence with input ingreds."""

    ingred_to_ix = {k: v for v, k in enumerate(all_ingreds)}
    ix_to_ingred = {v: k for v, k in enumerate(all_ingreds)}

    if isinstance(ingreds, str):
        ingreds = [ingreds]
    ixs = [ingred_to_ix[ingred] for ingred in ingreds]

    # Get only rows for our ingreds
    ingred_rows = recipe_matrix[ixs]
    # for each recipe, sum occurences of each ingred.
    ingred_sum = np.sum(ingred_rows, 0)
    # check where this sum equals the len of our ingred list.
    # This ensures we only get recipes that contain all our ingreds.
    match_recipe_ixs = np.argwhere(ingred_sum == len(ixs))
    match_recipes_m = recipe_matrix[:, match_recipe_ixs.flatten()]

    # Then sum total occurences of each ingredient for each recipe.
    match_ingred_sum = np.sum(match_recipes_m, 1)

    ranked_ixs = np.flip(np.argsort(match_ingred_sum))

    ranked_ingreds = {}
    for ranked_ix in ranked_ixs:
        cooccurrences = match_ingred_sum[ranked_ix]
        if cooccurrences == 0:
            break
        ranked_ingreds[ix_to_ingred[ranked_ix]] = cooccurrences

    return ranked_ingreds

# TODO: Duplicates in recipes in recipe_data_filtered causes recipe matrix to
# have elements that equal 2, causing ranking functions to misbehave.
def make_recipe_matrix():
    '''2D matrix whose rows are ingredients and cols are recipes titles.
    A 1 denotes the occurence of an ingredient in a given recipe.'''
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

    return df.to_numpy()


def get_cooc(df):
    df = make_recipe_matrix()

    m = df.to_numpy()
    m = m.dot(m.transpose())
    np.fill_diagonal(m, 0)
    return m


def get_ranked_ingreds_from_cooc(ingred):
    ingreds = get_json('all_ingreds_filtered.json')
    ingred_to_ix = {k: v for v, k in enumerate(ingreds)}
    ix_to_ingred = {v: k for v, k in enumerate(ingreds)}

    cooc = np.array(get_json('cooc.json'))

    ingred_ix = ingred_to_ix[ingred]
    ranked_ixs = np.argsort(cooc[ingred_ix])
    ranked_ixs = np.flip(ranked_ixs)

    ranked_ingreds = {}
    for ranked_ix in ranked_ixs:
        cooccurrences = cooc[ingred_ix, ranked_ix]
        if cooccurrences == 0:
            break
        ranked_ingreds[ix_to_ingred[ranked_ix]] = cooccurrences

    return ranked_ingreds


def main():
    ingreds = 'onion'
    recipe_matrix = np.array(get_json('recipe_matrix.json'))
    all_ingreds = get_json('all_ingreds_filtered.json')
    get_ranked_ingreds_naive(ingreds,recipe_matrix,all_ingreds)


if __name__ == "__main__":
    main()

