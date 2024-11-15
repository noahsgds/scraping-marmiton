import json
import pandas as pd


json_file_path = "/Users/noahsegonds/Desktop/Python/projet_scraping/Marmiton_site/public/recipe_dessert.json"

# Charger le JSON depuis le fichier
with open(json_file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Extraire tous les ingrédients uniques
all_ingredients = set(ingredient for recipe in data for ingredient in recipe['ingredients'])

# Créer la structure des données avec les colonnes souhaitées
transformed_data = []
for recipe in data:
    recipe_row = {
        'recipe': recipe['recipe_name'],
        'preparation_time': recipe['preparation_time'],
        'difficulty': recipe['difficulty'],
        'average_price': recipe['average_price'],
        'link': recipe['link'],
        'total_ingredients': len(recipe['ingredients'])
    }
    
    # Ajouter les colonnes pour chaque ingrédient unique
    for ingredient in all_ingredients:
        recipe_row[ingredient] = "true" if ingredient in recipe['ingredients'] else "false"
    
    # Ajouter la ligne transformée
    transformed_data.append(recipe_row)

# Convertir en DataFrame et sauvegarder en CSV
df = pd.DataFrame(transformed_data)
df.to_csv("recipes_dessert_transformed.csv", index=False)
