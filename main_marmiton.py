import requests
from bs4 import BeautifulSoup
import json
from unicodedata import unidata_version

def normalize_text(text):
    """Fonction pour normaliser le texte (enlever les accents et caractères spéciaux)"""
    if text:
        return unidata_version(text)
    return text

def get_all_page_links(total_pages: int) -> list:
    urls = []
    for page in range(1, total_pages + 1):
        url = f"https://www.marmiton.org/recettes/index/categorie/plat-principal/{page}"
        urls.append(url)
    return urls


def get_recipe_links_from(page_link: str) -> list:
    # Suppression de la concaténation avec le domaine
    response = requests.get(page_link)
    links = []
    
    if response.status_code != 200:
        print(f"ERROR - Status code: {response.status_code}")
    else:
        content_html = response.text
        soup = BeautifulSoup(content_html, "html.parser")
        all_tag_div = soup.find_all("a", class_="recipe-card-link")
        
        for tag_div in all_tag_div:
            # Utiliser directement le href car il contient déjà l'URL complète
            link = tag_div.get("href")
            links.append(link)
    
    return links

def convert_to_minute(time_str: str) -> int:
    """Convertit une chaîne de temps en minutes, en traitant les jours, heures, minutes et secondes."""
    total_minutes = 0
    
    # Supprimer les espaces multiples
    time_str = " ".join(time_str.split())
    
    # Gestion des jours (j)
    if "j" in time_str:
        day_part, time_str = time_str.split("j", 1)
        total_minutes += int(day_part.strip()) * 1440  # 1 jour = 1440 minutes
    
    # Gestion des heures (h)
    if "h" in time_str:
        hour_part, time_str = time_str.split("h", 1)
        total_minutes += int(hour_part.strip()) * 60  # Conversion des heures en minutes
    
    # Gestion des minutes (min)
    if "min" in time_str:
        time_str = time_str.split("min")[0].strip()
        if time_str:  # Si des minutes existent après 'min'
            total_minutes += int(time_str)
    
    # Gestion des secondes (sec)
    if "sec" in time_str:
        time_str = time_str.split("sec")[0].strip()
        if time_str:  # Si des secondes existent après 'sec'
            total_minutes += int(time_str) // 60  # Convertir les secondes en minutes (division entière)
    
    # Si la chaîne contient juste des nombres sans unités (comme "27" ou "30 sec")
    if time_str.isdigit():  # Vérifie si la chaîne restante est un nombre
        total_minutes += int(time_str)  # Ajouter directement les minutes

    return total_minutes



    
def get_infos_from(recipe_link: str) -> dict:
    recipe_obj = {
        "recipe_name": None,
        "preparation_time": None,
        "difficulty": None,
        "average_price": None,
        "ingredients": [],  # Initialisé comme une liste vide
        "link": recipe_link
    }
    
    response = requests.get(recipe_link)
    if response.status_code != 200:
        print(f"ERROR - Status code: {response.status_code}")
    else:
        content_html = response.text
        soup = BeautifulSoup(content_html, "html.parser")
        recipe_obj["recipe_name"] = soup.find("h1").get_text()
        recipe_obj["preparation_time"] = soup.find("div", class_="recipe-primary__item")
        if recipe_obj["preparation_time"] and recipe_obj["preparation_time"].find("span"):
            time_str = recipe_obj["preparation_time"].find("span").get_text()
            recipe_obj["preparation_time"] = convert_to_minute(time_str)
        recipe_obj["difficulty"] = soup.find("i", class_="icon-difficulty").find_next("span").get_text()
        recipe_obj["average_price"] = soup.find("i", class_="icon-price").find_next("span").get_text()
        recipe_obj["ingredients"] = [
            ingredient.get("data-name") for ingredient in soup.find_all("div", class_= "card-ingredient")
        ]
        recipe_obj["link"] = recipe_link
        
        print(f"Recette récupéré")
    return recipe_obj

def filter_recipes(recipes, difficulty, max_preparation_time, cost):
    filtered_recipes = []
    for recipe in recipes:
        if (difficulty == "0" or recipe['difficulty'] == difficulty) and \
           (max_preparation_time == "" or recipe['preparation_time'] <= int(max_preparation_time)) and \
           (cost == "0" or recipe['average_price'] == cost):
            filtered_recipes.append(recipe)
    return filtered_recipes

def main():
    # Recupere toutes les pages
    page_links = get_all_page_links(564)
    recipe_links = []

    # On itere sur toutes les pages
    for page_link in page_links:
        print(f"Getting links for page {page_link}")
        # On assemble tous les liens pour chaque page
        recipe_links += get_recipe_links_from(page_link)
    
    # On itere sur chaque lien de plats
    all_data = []
    for recipe_link in recipe_links:
        print(f"Getting data for book: {recipe_link}")
        recipe_obj = get_infos_from(recipe_link)
        all_data.append(recipe_obj)

    with open('recipe_principal.json', 'w') as file:
        json.dump(all_data, file)


if __name__ == "__main__":
    main()