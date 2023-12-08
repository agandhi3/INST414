import requests
from operator import itemgetter
import pandas as pd
import matplotlib.pyplot as plt

# Endpoint for Disney API to get characters
character_endpoint = "https://api.disneyapi.dev/character"

def get_characters_appearances():
    response = requests.get(character_endpoint)
    response.raise_for_status()
    
    data = response.json()
    
    characters = data.get('data') if 'data' in data else data
    
    character_appearances = {}

    for character in characters:
        if isinstance(character, dict):
            films = character.get('films', [])
            tv_shows = character.get('tvShows', [])
            total_appearances = len(films) + len(tv_shows)
            character_appearances[character.get('name', 'Unknown')] = total_appearances
        else:
            print(f"Expected a dictionary but got a {type(character)}.")
            continue  

    return character_appearances

try:
    character_appearances = get_characters_appearances()

    # Create DataFrame from the characters data
    characters_df = pd.DataFrame(character_appearances.items(), columns=['Character', 'Appearances'])

    # Bar Graph
    TOP_N = 10
    top_characters_df = characters_df.nlargest(TOP_N, 'Appearances')
    plt.figure(figsize=(10, 6))
    plt.bar(top_characters_df['Character'], top_characters_df['Appearances'], color='skyblue')
    plt.xlabel('Characters')
    plt.ylabel('Number of Appearances')
    plt.title(f'Top {TOP_N} Characters by Appearances')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Histogram 
    plt.figure(figsize=(10, 6))
    plt.hist(characters_df['Appearances'], bins=30, color='lightcoral')
    plt.xlabel('Number of Appearances')
    plt.ylabel('Frequency')
    plt.title('Distribution of Appearances Among Characters')
    plt.tight_layout()
    plt.show()

    # Box Plot 
    plt.figure(figsize=(8, 6))
    plt.boxplot(characters_df['Appearances'], vert=False)
    plt.xlabel('Number of Appearances')
    plt.title('Box Plot of Character Appearances')
    plt.tight_layout()
    plt.show()

except requests.exceptions.HTTPError as e:
    print(f"HTTP Error: {e}")
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
except ValueError as e:
    print(f"JSON Decode Error: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
