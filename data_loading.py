import pandas as pd

def convert_to_float(coord):
    """
    Converts coordinates like '13.14E' or '13.14S' to float values.
    'E' and 'N' are positive, 'W' and 'S' are negative.
    """
    if 'E' in coord or 'N' in coord:
        return float(coord[:-1])
    elif 'W' in coord or 'S' in coord:
        return -float(coord[:-1])
    else:
        raise ValueError(f"Unexpected coordinate format: {coord}")

def load_data(filepath):
    data = pd.read_csv(filepath)
    
    # Ensure 'Year' is extracted from date
    data['Year'] = pd.to_datetime(data['dt'], errors='coerce').dt.year
    
    # Convert 'AverageTemperature' to numeric, handling errors by setting non-numeric values to NaN
    data['AverageTemperature'] = pd.to_numeric(data['AverageTemperature'], errors='coerce')
    
    # Drop rows where 'AverageTemperature' or 'Year' is NaN
    data.dropna(subset=['AverageTemperature', 'Year'], inplace=True)
    
    # Apply the conversion function to latitude and longitude
    data['Latitude'] = data['Latitude'].apply(convert_to_float)
    data['Longitude'] = data['Longitude'].apply(convert_to_float)
    
    return data

def filter_data_by_year(data, year):
    return data[data['Year'] == year]