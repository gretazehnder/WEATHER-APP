import streamlit as st
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from data_loading import load_data  # Assuming you have this function in the first file
import numpy as np

# Load data
data = load_data(r"C:\Users\greta\OneDrive\Desktop\GlobalLandTemperaturesByMajorCity.csv")

# Calculate temperature range for each city
temp_ranges = data.groupby('City')['AverageTemperature'].agg(lambda x: x.max() - x.min())
high_variance_cities = temp_ranges[temp_ranges > 15].index  # Adjust threshold as needed

# Title and instructions
st.title("Global Temperature Change Visualization Over Time")
st.write("Explore the change in temperatures over time and identify cities with large temperature ranges.")

# Year slider
year = st.slider("Select Year", int(data['Year'].min()), int(data['Year'].max()), step=1)

# Filter data for selected year
year_data = data[data['Year'] == year]

# Convert to GeoDataFrame
gdf = gpd.GeoDataFrame(year_data, geometry=gpd.points_from_xy(year_data.Longitude, year_data.Latitude))

# Load shapefile for world map
file_p = r"C:\Users\greta\OneDrive\Desktop\nat.earth\ne_110m_admin_0_countries.shp"
world = gpd.read_file(file_p)

# Plot map with enhancements
fig, ax = plt.subplots(figsize=(12, 8))
world.plot(ax=ax, color='lightgrey', edgecolor='black')  # World map with borders

# Plot all cities in blue with different sizes for better visibility
gdf.plot(ax=ax, color='blue', markersize=20, alpha=0.5, edgecolor='black', label="Other Cities")

# Highlight high variance cities in red with larger markers
high_variance_data = gdf[gdf['City'].isin(high_variance_cities)]
high_variance_data.plot(ax=ax, color='red', markersize=50, alpha=0.7, edgecolor='black', label="High Temp Range Cities")

# Add title and improve aesthetics
plt.title(f"Temperature Distribution in Major Cities - {year}", fontsize=18, fontweight='bold', color='darkblue')
plt.xlabel("Longitude", fontsize=14)
plt.ylabel("Latitude", fontsize=14)

# Customize ticks
ax.tick_params(axis='both', which='major', labelsize=12)
ax.set_xticks(np.arange(-180, 181, 30))  # Set x-ticks every 30 degrees
ax.set_yticks(np.arange(-90, 91, 30))    # Set y-ticks every 30 degrees
ax.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.5)  # Add a grid for better readability

# Add legend
plt.legend()

# Display map
st.pyplot(fig)



# Select a city to display time-series
selected_city = st.selectbox("Select a city to view historical temperature data:", data['City'].unique())

if selected_city:
    city_data = data[data['City'] == selected_city]

    if not city_data.empty:
        # Ensure 'Date' is a datetime object
        city_data['Date'] = pd.to_datetime(city_data['dt'], errors='coerce')
        
        # Extract year from the date and create a new column
        city_data['Year'] = city_data['Date'].dt.year
        
        # Group by year and calculate the average temperature
        yearly_data = city_data.groupby('Year', as_index=False)['AverageTemperature'].mean()

        fig, ax = plt.subplots(figsize=(10, 6))

        # Plot with enhancements
        ax.plot(yearly_data['Year'], yearly_data['AverageTemperature'], 
                color='purple', marker='o', linestyle='-', linewidth=2, markersize=5)
        ax.set_title(f"Average Temperature Change Over Time in {selected_city}", 
                     fontsize=16, fontweight='bold', color='darkblue')
        ax.set_xlabel("Year", fontsize=14, color='darkgreen')
        ax.set_ylabel("Average Temperature (°C)", fontsize=14, color='darkgreen')

        # Add grid and customize tick parameters
        ax.grid(True, linestyle='--', color='gray', alpha=0.7)
        ax.tick_params(axis='both', which='major', labelsize=12)

        # Show the plot in Streamlit
        st.pyplot(fig)
    else:
        st.write(f"No data available for {selected_city}")
