# FreeGo
## _Find Recipes Based on What's in Your Fridge_

[![Marmiton](https://www.marmiton.org/reloaded/static/Front/Component/headerLightDesktop/assets/logo.svg)](https://marmiton.org)


Marmiton Recipe Finder is a web application designed to help users find recipes by filtering based on the ingredients they already have. It's an innovative way to combat food waste while discovering delicious dishes. 

- Enter the ingredients you have at home
- Instantly discover matching recipes
- ✨Magic ✨

## Features

- Search recipes using a list of available ingredients
- Detailed recipe pages with instructions and preparation times
- The list of all the recipe in Marmiton
- Clean and responsive user interface built with HTML and CSS

This application uses data scraped from the [Marmiton](https://marmiton.org) website, ensuring a rich variety of recipes to choose from.

## Tech

Marmiton Recipe Finder leverages several open-source technologies:

- [BeautifulSoup] - Library for web scraping
- [Unicodedata] - For normalize the texte

The project is open-source and hosted on GitHub for easy access and collaboration.
# Documentation - Marmiton Scraping Project

### `main_marmiton.py` Explanation

### Step 1: Text Normalization
The `normalize_text` function normalizes text by removing accents and special characters to ensure uniformity in the scraped data.

- **Parameter**: `text` (string) - The text to normalize
- **Return**: Normalized string
```python
from unicodedata import unidata_version

def normalize_text(text):
    """Function to normalize text (remove accents and special characters)."""
    if text:
        return unidata_version(text)
    return text

# Example
title = "Délicieux gâteau au chocolat"
normalized_title = normalize_text(title)
print(normalized_title)  # Output: "Delicieux gateau au chocolat"
```
### Step 2: Generating Page Links
The `get_all_page_links` function generates a list of URLs for all pages within a specific category on Marmiton.

- **Parameter**: `total_pages` (int) - Total number of pages to scrape
- **Return**: List of page URLs
```python
import requests
from bs4 import BeautifulSoup

def get_all_page_links(total_pages: int) -> list:
    """Generates a list of URLs to navigate through Marmiton pages."""
    urls = []
    for page in range(1, total_pages + 1):
        url = f"https://www.marmiton.org/recettes/index/categorie/plat-principal/{page}"
        urls.append(url)
    return urls

def get_recipe_links_from(page_link: str) -> list:
    """Fetches recipe links from a specific page."""
    response = requests.get(page_link)
    links = []
    
    if response.status_code != 200:
        print(f"ERROR - Status code: {response.status_code}")
    else:
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup.find_all("a", class_="recipe-card-link"):
            links.append(tag.get("href"))
    
    return links

# Example usage
page_links = get_all_page_links(2)
for page_link in page_links:
    recipe_links = get_recipe_links_from(page_link)
    print(recipe_links)
```
### Step 3: Extracting Recipe Links
The `get_recipe_links_from` function retrieves all recipe links available on a specific page.

- **Parameter**: `page_link` (string) - URL of the page
- **Return**: List of recipe links

### Step 4: Converting Time to Minutes
The `convert_to_minute` function converts a formatted time string (e.g., days, hours, minutes, seconds) into a total value in minutes.

- **Parameter**: `time_str` (string) - Time string to convert
- **Return**: Total time in minutes (int)

### Step 5: Retrieving Recipe Information
The `get_infos_from` function scrapes detailed information for a recipe, including:
- Name
- Preparation time
- Difficulty level
- Estimated cost
- List of ingredients

- **Parameter**: `recipe_link` (string) - Link to the recipe
- **Return**: Dictionary containing the recipe details

### Step 6: Filtering Recipes
The `filter_recipes` function filters a list of recipes based on:
- Difficulty
- Maximum preparation time
- Cost

- **Parameters**:
  - `recipes` (list) - List of recipe dictionaries
  - `difficulty` (string) - Target difficulty level
  - `max_preparation_time` (int) - Maximum allowed preparation time in minutes
  - `cost` (string) - Target cost level

- **Return**: List of filtered recipes

### Step 7: Main Execution
The `main` function executes the entire scraping workflow:
1. Generate page links
2. Extract recipe links from pages
3. Scrape detailed recipe information
4. Save data to a JSON file

- **Output**: A `recipe_principal.json` file containing all scraped data.



## Transforming Data with `data.py`

### Data Preparation for Analysis
To enable effective data analysis in Power BI, the scraped JSON data from `main_marmiton.py` required transformation. This step was achieved using the `data.py` script, which performs the following tasks:

1. **Loading the JSON**: Reads raw data extracted from the scraping process.
2. **Extracting Unique Ingredients**: Identifies all unique ingredients and creates binary columns for each.
3. **Restructuring Data**: Transforms the recipe information into a structured table with:
   - Recipe name
   - Preparation time
   - Difficulty level
   - Cost
   - Binary columns for each unique ingredient
4. **Exporting to CSV**: Generates a final, cleaned `recipes_dessert_transformed.csv` file.

This structured CSV file is then used for visual analysis and creating insightful dashboards in Power BI.


## Data Visualization

Data visualization played a critical role in analyzing the comprehensive dataset we scraped from the Marmiton website. By leveraging the structured JSON files, we were able to transform raw data into meaningful insights using Power BI. This step allowed us to explore key aspects of the recipes, such as the most common ingredients, distribution of recipe categories, preparation times, and user ratings.

Through these visualizations, we identified trends and patterns within the dataset, which enhanced our understanding of the culinary world presented by Marmiton. For instance, we discovered which ingredients appeared most frequently in recipes, helping users find dishes that match their preferences or available ingredients. Additionally, we examined the diversity of recipe categories to highlight the variety of options available for users. 

To provide further value, we analyzed the average preparation and cooking times across different recipe types, enabling better planning for users based on their time constraints.

Below are some examples of the visualizations created from this analysis:

### Relationship between preparation time and level of difficulty.
![Chart](https://raw.githubusercontent.com/noahsgds/image/refs/heads/main/Capture%20d%E2%80%99e%CC%81cran%202024-11-15%20a%CC%80%2011.21.38.png?token=GHSAT0AAAAAAC2NNGSO7XJLBUMDBRNFO5IYZZXODXA)

### The ingredients most frequently used in recipes
This visual shows the ingredients most frequently used in recipes,
listed in order of frequency of appearance.  
![Chart](https://raw.githubusercontent.com/noahsgds/image/refs/heads/main/Capture%20d%E2%80%99e%CC%81cran%202024-11-15%20a%CC%80%2011.26.03.png?token=GHSAT0AAAAAAC2NNGSOI7PKZ2GNUP76GFGMZZXOGZQ)


Through these visualizations, we effectively transformed raw data into actionable insights, empowering users to make informed decisions when exploring recipes. By combining the power of data scraping and visualization, we provided a seamless and intuitive way to interact with the culinary data.



# Web Interface Overview

This project includes a web interface, **FreeGo**, that enables users to explore recipes based on specific criteria. The interface connects with the data scraped and processed from Marmiton, offering an interactive experience for recipe discovery. Below is a breakdown of the functionalities provided by the interface.

### Features of the Interface

1. **Ingredient-based Filtering**:
   - Users can input one or more ingredients in a search bar to filter recipes that include those ingredients.
   - Selected ingredients are displayed in a list with an option to remove any ingredient.

2. **Advanced Filters**:
   - Filters are available for:
     - Recipe type (e.g., starters, main courses, desserts)
     - Difficulty level (Very Easy, Easy, Moderate, Hard)
     - Preparation time (e.g., less than 15, 30, or 60 minutes)
     - Cost (Low, Medium, High)
   - Users can apply multiple filters simultaneously to refine their search.

3. **Dynamic Recipe Display**:
   - Recipes matching the criteria are fetched from pre-processed JSON files.
   - The results include:
     - Recipe name
     - Preparation time (formatted in hours and minutes)
     - A link to the full recipe on Marmiton

4. **Ingredient List Management**:
   - The interface includes functionality to add or remove ingredients dynamically.
   - Ingredient management ensures only valid selections are considered during filtering.

5. **No Results Handling**:
   - If no recipes match the filters, a message is displayed to inform the user.

### Workflow

- **Input Selection**:
  - Users start by entering ingredients and selecting filters (type, difficulty, time, cost).
- **Data Fetching**:
  - The system fetches the appropriate JSON file based on the selected recipe type.
- **Filtering Logic**:
  - Recipes are filtered based on:
    - Presence of all selected ingredients
    - Match with difficulty level
    - Preparation time within the specified range
    - Cost level
- **Results Display**:
  - Filtered recipes are displayed with essential details and a link to the full recipe.

### How It Works with Scraped Data

The web application integrates the scraped data from Marmiton (processed using `main_marmiton.py`) with transformations applied in `data.py`. These transformations ensure that:
- Ingredients are normalized and easy to filter.
- Recipes are tagged with metadata (difficulty, preparation time, cost) for advanced filtering.

### Adding Visual Content

![FreeGo Web Interface](https://raw.githubusercontent.com/noahsgds/image/refs/heads/main/Capture%20d%E2%80%99e%CC%81cran%202024-11-15%20a%CC%80%2010.53.24.png?token=GHSAT0AAAAAAC2NNGSO75W67VNQAO62VFEWZZXOAVA)



## Installation

### Requirements

- **Python 3.x**
- **pip** for managing Python packages


