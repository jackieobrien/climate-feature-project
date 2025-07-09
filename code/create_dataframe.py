"""
This script reads all the csv datafiles and combines them into a single dataframe
    which can then be returned to whatever script needs it
"""
import geopandas as gpd
import numpy as np
import pandas as pd


# Get the country dataset from CSV to get long and lat data
def fetch_country_df():
    country_df = pd.read_csv('data/countries.csv').drop(
        [
            'iso2', 'numeric_code', 'phone_code', 'currency',
            'currency_name', 'currency_symbol', 'tld', 'native'],
        axis=1)
    country_df = country_df.rename(columns={'iso3': 'ISO3'})
    country_df = country_df.fillna(0)
    country_df['name'] = country_df['name'].str.casefold()
    return country_df


# Get the world map data from gpd
def fetch_world_df():
    world_df = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
    world_df = world_df.drop(world_df[world_df["continent"].isin(["Antarctica"])].index)
    world_df = world_df.rename(columns={'iso_a3': 'ISO3'})
    world_df = world_df.dropna()
    return world_df


# Get the climate dataset from CSV. This has the warming rate data to be calculated
def fetch_climate_df():
    climate_df = pd.read_csv('data/climate_change_indicators.csv').drop(
        ['ISO2', 'Indicator', 'Unit', 'Source', 'CTS_Code', 'CTS_Name', 'CTS_Full_Descriptor', 'Country'], axis=1)
    climate_df = climate_df.fillna(0)
    return climate_df


# Dataframe used for plotting on the world map.
# This is not a dataframe but a "geoframe", and will be important later
def fetch_mapping_df(climate_df, world_df):
    map_df = climate_df.merge(world_df, on='ISO3')
    map_df.drop(map_df.iloc[:, 2:64], axis=1, inplace=True)
    map_df = gpd.GeoDataFrame(map_df, geometry="geometry")
    return map_df


# Creates a dataframe with the coastline length of all the countries
def fetch_coastline_length():
    coastline_df = pd.read_csv('data/List_of_countries_by_length_of_coastline.csv',
                               header=[0]).drop_duplicates().dropna()
    coastline_df = coastline_df[['Country', 'World Resources Institute[1].1', 'Coast/area ratio (m/km2).1']]
    coastline_dict = {'World Resources Institute[1].1': 'coastline_km',
                      'Country': 'name',
                      'Coast/area ratio (m/km2).1': 'coast_area_ratio'}
    coastline_df.rename(columns=coastline_dict, inplace=True)
    coastline_df['name'] = coastline_df['name'].str.casefold()
    coastline_df['name'] = coastline_df['name'].str.replace(',', '')
    return coastline_df


# Creates a dataframe with all the country areas
def fetch_country_area():
    area_df = pd.read_csv('data/List_of_countries_and_dependencies_by_area.csv').drop(['Unnamed: 0', 'Unnamed: 6'],
                                                                                      axis=1)
    area_dict = {'Country / dependency': 'name',
                 'Total in km2 (mi2)': 'total_area',
                 'Land in km2 (mi2)': 'land_area',
                 'Water in km2 (mi2)': 'water_area',
                 '% water': 'percent_water'}
    area_df.rename(columns=area_dict, inplace=True)
    area_df['total_area'] = area_df['total_area'].str.rstrip('(123,456,7890)').replace(r'\D', '', regex=True)
    area_df['land_area'] = area_df['land_area'].str.rstrip('(123,456,7890)').replace(r'\D', '', regex=True)
    area_df['water_area'] = area_df['water_area'].str.rstrip('(123,456,7890)').replace(r'\D', '', regex=True)
    area_df['water_area'] = area_df['water_area'].replace("", 0)
    area_df['name'] = area_df['name'].str.casefold()
    area_df['name'] = area_df['name'].str.replace(',', '')
    return area_df


# Creates a dataframe of all the country eco footprint
def fetch_eco_footprint():
    ecofootprint_df = pd.read_csv('data/List_of_countries_by_ecological_footprint.csv').iloc[1:, 1:4]
    ecofootprint_df.rename(columns={'Country/region': 'name',
                                    'Ecological footprint': 'eco_footprint',
                                    'Biocapacity': 'biocapacity'}, inplace=True)
    ecofootprint_df['name'] = ecofootprint_df['name'].str.casefold()
    ecofootprint_df['name'] = ecofootprint_df['name'].str.replace(',', '')
    return ecofootprint_df


# Creates a database that details all the carbon intensity
def fetch_carbon_intensity():
    carbon_df = pd.read_csv('data/List_of_countries_by_carbon_intensity_of_GDP.csv').iloc[:, 1:3]
    carbon_dict = {'Country': 'name',
                   'CO₂ kg/$': 'carbon_intensity_2018'}
    carbon_df.rename(columns=carbon_dict, inplace=True)
    carbon_df['name'] = carbon_df['name'].str.casefold()
    carbon_df['name'] = carbon_df['name'].str.replace(',', '')
    return carbon_df


# Creates a database with all country populations
def fetch_population():
    population_df = pd.read_csv('data/List_of_countries_and_dependencies_by_population.csv').iloc[:, 1:3]
    population_dict = {'Location': 'name',
                       'Population': 'population'}
    population_df.rename(columns=population_dict, inplace=True)
    population_df['name'] = population_df['name'].str.casefold()
    population_df['name'] = population_df['name'].str.replace(',', '')
    return population_df


# Creates a database with country population densities
def fetch_pop_density():
    pop_density_df = pd.read_csv('data/List_of_countries_and_dependencies_by_population_density.csv').loc[:,
                     ['Location', 'Density /km2']]
    pop_density_dict = {'Location': 'name',
                        'Density /km2': 'pop_density_km'}
    pop_density_df.rename(columns=pop_density_dict, inplace=True)
    pop_density_df['name'] = pop_density_df['name'].str.casefold()
    pop_density_df['name'] = pop_density_df['name'].str.replace(',', '')
    return pop_density_df


# Creates a database with country elevation avgs
def fetch_avg_elevation():
    elevation_df = pd.read_csv('data/List_of_countries_by_average_elevation.csv')
    elevation_dict = {'Country': 'name',
                      'Elevation': 'avg_elevation_km'}
    elevation_df.rename(columns=elevation_dict, inplace=True)
    elevation_df['avg_elevation_km'] = elevation_df['avg_elevation_km'].str.split(' ').str[0]
    elevation_df['avg_elevation_km'] = (elevation_df['avg_elevation_km'].
                                       str.rstrip('(123,456,7890)').replace(r'\D', '', regex=True))
    elevation_df['avg_elevation_km'] = pd.to_numeric(elevation_df['avg_elevation_km']).div(1000)
    elevation_df['name'] = elevation_df['name'].str.casefold()
    elevation_df['name'] = elevation_df['name'].str.replace(',', '')
    return elevation_df


# TODO: Convert avg_elevation, max_elevation, and min_elevation into numeric
# Creates a database with country elevation minimums and maximums
def fetch_elevation_extremes():
    elevation_extremes_df = pd.read_csv('data/List_of_elevation_extremes_by_country.csv').loc[:,
                            ['Country_or_region', 'Maximum_elevation', 'Minimum_elevation']]
    elevation_extremes_dict = {'Country_or_region': 'name',
                               'Maximum_elevation': 'max_elevation_km',
                               'Minimum_elevation': 'min_elevation_km'}
    elevation_extremes_df.rename(columns=elevation_extremes_dict, inplace=True)

    elevation_extremes_df['max_elevation_km'] = elevation_extremes_df['max_elevation_km'].str.split('m').str[0]
    elevation_extremes_df['max_elevation_km'] = elevation_extremes_df['max_elevation_km'].str.rstrip()
    elevation_extremes_df['max_elevation_km'] = pd.to_numeric(elevation_extremes_df['max_elevation_km']).div(1000)

    elevation_extremes_df['min_elevation_km'] = elevation_extremes_df['min_elevation_km'].str.split('m').str[0]
    elevation_extremes_df['min_elevation_km'] = elevation_extremes_df['min_elevation_km'].str.rstrip()
    elevation_extremes_df['min_elevation_km'] = elevation_extremes_df['min_elevation_km'].replace('sea level', 0)
    elevation_extremes_df['min_elevation_km'] = elevation_extremes_df['min_elevation_km'].str.replace('−', '-').astype(
        float)
    elevation_extremes_df['min_elevation_km'] = elevation_extremes_df['min_elevation_km'].fillna(0)
    elevation_extremes_df['min_elevation_km'] = elevation_extremes_df['min_elevation_km'].div(1000)
    elevation_extremes_df['name'] = elevation_extremes_df['name'].str.casefold()
    elevation_extremes_df['name'] = elevation_extremes_df['name'].str.replace(',', '')
    return elevation_extremes_df


# Creates a database with country annual average precipitation amount (mm)
def fetch_avg_precipitation():
    precipitation_df = pd.read_csv('data/List_of_countries_by_average_annual_precipitation.csv').loc[:,
                       ['Country', 'mm/ year)']]
    precipitation_dict = {'Country': 'name',
                          'mm/ year)': 'annual_precipitation_avg_mm'}
    precipitation_df.rename(columns=precipitation_dict, inplace=True)
    precipitation_df['name'] = precipitation_df['name'].str.casefold()
    precipitation_df['name'] = precipitation_df['name'].str.replace(',', '')
    return precipitation_df


# Creates a database with country renewable water resources
def fetch_water_resources():
    water_resources_df = pd.read_csv('data/List_of_countries_by_total_renewable_water_resources.csv')
    water_resources_dict = {'Country/Territory/Region/Group': 'name',
                            'Total renewable water resources (bln m3/year)': 'tarwr'}
    water_resources_df.rename(columns=water_resources_dict, inplace=True)
    water_resources_df['name'] = water_resources_df['name'].str.casefold()
    water_resources_df['name'] = water_resources_df['name'].str.replace(',', '')
    return water_resources_df


# Creates global dataframe. Has all the details of country and climate
def create_global_df(country_df, climate_df):
    # Create the global dataset by merging the two dataframes, putting the Country column first so it is easier to read
    # The "WLD" column is dropped here
    global_df = country_df.merge(climate_df, on='ISO3').drop(['ObjectId', 'id'], axis=1)
    global_df = global_df.dropna()
    global_df['name'] = global_df['name'].str.casefold()

    # create warming rate dataframe
    # find warming rate
    global_df['avg_indicator'] = global_df.iloc[:, 10:71].mean(axis=1)

    # Create column that has a numerical value to the region ID
    global_df['region_id'] = [np.where(pd.unique(global_df['region']) == i)[0][0] for i in global_df['region']]
    return global_df


def find_dropped_rows(df1, df2):
    df = pd.merge(df1, df2, on='name', indicator=True, how='outer')
    return df[df['_merge'] != 'both']


# Create warming dataset
def create_warming_df():
    """
    This is the warming dataset that we will be using for K means program.
        Create the global dataframe, then select the interesting indicators. Then merge with other points of data
        from coastline length, country area, eco footprint, and carbon intensity.
    """
    country_df = fetch_country_df()
    climate_df = fetch_climate_df()
    global_df = create_global_df(country_df, climate_df)

    warming_df = global_df.loc[:, ['name', 'ISO3', 'region', 'region_id', 'latitude', 'longitude', 'avg_indicator']]
    warming_df = warming_df.merge(fetch_coastline_length(), on='name', how='left').fillna(0)
    warming_df = warming_df.merge(fetch_country_area(), on='name', how='left').fillna(0)
    warming_df = warming_df.merge(fetch_eco_footprint(), on='name', how='left').fillna(0)
    warming_df = warming_df.merge(fetch_carbon_intensity(), on='name', how='left').fillna(0)
    warming_df = warming_df.merge(fetch_population(), on='name')
    warming_df = warming_df.merge(fetch_pop_density(), on='name', how='left').fillna(0)
    warming_df = warming_df.merge(fetch_avg_elevation(), on='name', how='left').fillna(0)
    warming_df = warming_df.merge(fetch_elevation_extremes(), on='name', how='left').fillna(0)
    warming_df = warming_df.merge(fetch_avg_precipitation(), on='name', how='left').fillna(0)

    # Commenting out because not sure how to use the data
    # warming_df = warming_df.merge(fetch_water_resources(), on='name')

    return warming_df
