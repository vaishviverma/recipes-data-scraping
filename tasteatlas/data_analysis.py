import pandas as pd
from ast import literal_eval

# This script makes changes to the ingredient list
# removing unnecessary capitalized words which are not ingredients.

df = pd.read_csv('tasteatlas.csv')

for index, row in df.iterrows():

        ingred = literal_eval(row['ingredient_list'])
        for item in ingred:
                if (item.upper() == item):
                        ingred.remove(item)
                        
        row['ingredient_list'] = ingred

df.to_csv('processed_tasteatlas.csv')