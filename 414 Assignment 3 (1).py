import pandas as pd
from scipy.spatial.distance import cdist
import numpy as np
from tabulate import tabulate
import matplotlib.pyplot as plt

spotify_data = pd.read_csv('spotify-2023.csv', encoding='ISO-8859-1')

feature_columns = [
    'bpm', 'danceability_%', 'valence_%', 'energy_%', 
    'acousticness_%', 'instrumentalness_%', 'liveness_%', 'speechiness_%'
]

# Normalize track names and artist(s) names for matching
spotify_data['normalized_track_name'] = spotify_data['track_name'].str.lower().str.replace(' ', '')
spotify_data['normalized_artists'] = spotify_data['artist(s)_name'].str.lower().str.replace(' ', '')

# Convert 'mode' to binary numerical values (1 for Major, 0 for Minor)
spotify_data['mode'] = spotify_data['mode'].apply(lambda x: 1 if x == 'Major' else 0)

# Extract the numeric features for similarity comparison and ensure they are numeric
features = spotify_data[feature_columns].apply(pd.to_numeric, errors='coerce').fillna(0)

# Normalize the features
normalized_features = (features - features.mean()) / features.std()

# Define query tracks by their normalized names
query_tracks = {
    "blindinglights": "theweeknd",
    "shapeofyou": "edsheeran",
    "someoneyouloved": "lewiscapaldi"
}

query_indices = {}
for query_track, query_artist in query_tracks.items():
    condition = (
        spotify_data['normalized_track_name'].str.contains(query_track) & 
        spotify_data['normalized_artists'].str.contains(query_artist)
    )
    query_indices[query_track] = spotify_data[condition].index[0]

# Compute the distances from the query tracks to all other tracks
distance_matrix = cdist(normalized_features.loc[query_indices.values()], normalized_features, 'euclidean')

# Get the top 10 closest tracks for each query track
top_tracks = {}
for i, (query_track, query_index) in enumerate(query_indices.items()):
    sorted_indices = np.argsort(distance_matrix[i])
    closest_indices = [index for index in sorted_indices if index != query_index][:10]
    closest_distances = distance_matrix[i, closest_indices]  
    top_tracks[query_track] = spotify_data.loc[closest_indices, ['track_name', 'artist(s)_name']].reset_index(drop=True)
    top_tracks[query_track]['distance'] = closest_distances  

for query, tracks in top_tracks.items():
    print(f"Top 10 similar tracks to '{query}':")
    print(tabulate(tracks, headers='keys', showindex=False, tablefmt='pretty'))
    print("\n")
    
    
#Graphs
np.random.seed(0)
distances = {
    'blindinglights': np.random.rand(100),
    'shapeofyou': np.random.rand(100),
    'someoneyouloved': np.random.rand(100)
}

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

for i, (track, dist) in enumerate(distances.items()):
    axes[i].plot(dist)
    axes[i].set_title(f"Euclidean Distances for '{track}'")
    axes[i].set_xlabel('Track Index')
    axes[i].set_ylabel('Distance')
    axes[i].grid(True)

plt.tight_layout()
plt.show()