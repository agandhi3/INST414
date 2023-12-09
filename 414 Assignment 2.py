import requests
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from operator import itemgetter

# Get Data from Data USA API
api_endpoint = "https://datausa.io/api/data?drilldowns=Nation&measures=Population"
response = requests.get(api_endpoint)

if response.status_code == 200:
    data = response.json()
    df = pd.DataFrame(data['data'])
else:
    print("Failed to retrieve data:", response.status_code)
    exit()

# Create graph, each node representing a year and edges connecting consecutive years
G = nx.Graph()

years = df['Year'].unique()
for year in years:
    G.add_node(year)

sorted_years = sorted(years)
for i in range(len(sorted_years) - 1):
    G.add_edge(sorted_years[i], sorted_years[i + 1])

# Important nodes are those with the highest degree centrality
degree_centrality = nx.degree_centrality(G)
important_nodes = sorted(degree_centrality.items(), key=itemgetter(1), reverse=True)[:3]
important_nodes = [node[0] for node in important_nodes]  

print(f"The graph has {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")
print(f"Important nodes based on degree centrality: {important_nodes}")

plt.figure(figsize=(12, 8))
pos = nx.circular_layout(G)
nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500)
nx.draw_networkx_nodes(G, pos, nodelist=important_nodes, node_color='red', node_size=700)
plt.title('Network Graph of Years with Population Data')
plt.show()

# Important nodes in red.

