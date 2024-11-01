import streamlit as st
import geopandas as gpd 
import pandas as pd
import matplotlib.pyplot as plt 

def load_data():
    data = pd.read_csv(r"C:\Users\greta\OneDrive\Desktop\GlobalLandTemperaturesByMajorCity.csv")
    data['Year'] = pd.to_datetime(data['dt']).dt.year  # Extract year for filtering
    data['Temperature'] = data['AverageTemperature']
    return data

# Function to filter data by selected year
def filter_data_by_year(data, year):
    return data[data['Year'] == year]

# Main Streamlit app
def main():
    # Load data
    data = load_data()

    # Sidebar - Year selection with a slider
    st.sidebar.title("Temperature Timeline")
    selected_year = st.sidebar.slider("Select a year", min_value=int(data['Year'].min()), max_value=int(data['Year'].max()), step=1)
    filtered_data = filter_data_by_year(data, selected_year)

    # Create GeoDataFrame from filtered data using Latitude and Longitude
    geo_df = gpd.GeoDataFrame(filtered_data, geometry=gpd.points_from_xy(filtered_data['Longitude'], filtered_data['Latitude']))

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))
    world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
    world.plot(ax=ax, color="lightgrey")

    # Plot cities with temperature color scale
    geo_df.plot(column='Temperature', cmap='coolwarm', markersize=50, ax=ax, legend=True)
    ax.set_title(f"Global Temperatures in {selected_year}")
    st.pyplot(fig)

if __name__ == "__main__":
    main()
