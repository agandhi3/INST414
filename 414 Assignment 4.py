import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

df = pd.read_csv('earthquake data.csv')

# Clean the data by dropping rows with missing values in the specified columns
df_cleaned = df.dropna(subset=['Latitude', 'Longitude', 'Magnitude'])

# Standardize the features
scaler = StandardScaler()
features = scaler.fit_transform(df_cleaned[['Latitude', 'Longitude', 'Depth', 'Magnitude']])

# Perform K-Means clustering 
optimal_k = 5  #Value based on the Elbow plot
kmeans = KMeans(n_clusters=optimal_k, n_init=10, random_state=0)
df_cleaned['cluster'] = kmeans.fit_predict(features)

# Send output to separate CSV file
output_file_path = 'earthquake_clusters.csv'
df_cleaned.to_csv(output_file_path, index=False)

# Plot clusters
plt.figure(figsize=(12, 8))
plt.scatter(df_cleaned['Longitude'], df_cleaned['Latitude'], c=df_cleaned['cluster'], cmap='viridis', marker='.')
plt.title('Clustered Earthquake Data')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.colorbar(label='Cluster Label')
plt.show()

# Plot histogram 
plt.figure(figsize=(10, 6))
df_cleaned['cluster'].plot(kind='hist', bins=optimal_k, color='skyblue')
plt.title('Histogram of Earthquake Clusters')
plt.xlabel('Cluster')
plt.ylabel('Number of Earthquakes')
plt.show()

# Plot a boxplot 
plt.figure(figsize=(10, 6))
df_cleaned.boxplot(column='Magnitude', by='cluster')
plt.title('Boxplot of Magnitudes by Cluster')
plt.xlabel('Cluster')
plt.ylabel('Magnitude')
plt.show()

output_file_path

